import uuid
import time
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="URL Shortener with Analytics")
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

# In-memory storage (no external DB required)
# Structure: { short_code: { "original_url": str, "created_at": float, "clicks": int, "last_clicked_at": Optional[float] } }
urls_db: dict[str, dict] = {}

class CreateURLRequest(BaseModel):
    original_url: str = Field(..., description="The long URL to shorten")
    custom_code: Optional[str] = Field(None, description="Optional custom short code")

class ShortenedURLResponse(BaseModel):
    short_code: str
    short_url: str
    original_url: str
    created_at: float

class URLAnalyticsResponse(BaseModel):
    short_code: str
    original_url: str
    clicks: int
    created_at: float
    last_clicked_at: Optional[float]

class ListURLsResponse(BaseModel):
    urls: List[dict]

@app.get('/')
def root():
    return {'status': 'online', 'service': 'URL Shortener with Analytics'}

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.post('/shorten', response_model=ShortenedURLResponse)
def shorten_url(request: CreateURLRequest):
    """Create a new shortened URL."""
    original_url = request.original_url.strip()
    if not original_url:
        raise HTTPException(status_code=400, detail="Original URL cannot be empty")
    
    # Basic URL validation (simple check)
    if not (original_url.startswith('http://') or original_url.startswith('https://')):
        raise HTTPException(status_code=400, detail="URL must start with http:// or https://")
    
    # Determine short code
    if request.custom_code:
        short_code = request.custom_code.strip().lower()
        if not short_code:
            raise HTTPException(status_code=400, detail="Custom code cannot be empty")
        if short_code in urls_db:
            raise HTTPException(status_code=409, detail="Custom code already exists")
    else:
        # Generate unique short code
        short_code = uuid.uuid4().hex[:8]
        while short_code in urls_db:
            short_code = uuid.uuid4().hex[:8]
    
    created_at = time.time()
    urls_db[short_code] = {
        "original_url": original_url,
        "created_at": created_at,
        "clicks": 0,
        "last_clicked_at": None
    }
    
    return ShortenedURLResponse(
        short_code=short_code,
        short_url=f"http://localhost:8000/{short_code}",
        original_url=original_url,
        created_at=created_at
    )

@app.get('/{short_code}')
def redirect_url(short_code: str):
    """Redirect to original URL and record click."""
    if short_code not in urls_db:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    url_data = urls_db[short_code]
    
    # Record click
    url_data["clicks"] += 1
    url_data["last_clicked_at"] = time.time()
    
    # Return redirect response
    return {
        "redirect": url_data["original_url"],
        "short_code": short_code,
        "clicks": url_data["clicks"]
    }

@app.get('/analytics/{short_code}', response_model=URLAnalyticsResponse)
def get_analytics(short_code: str):
    """Get analytics for a specific short URL."""
    if short_code not in urls_db:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    url_data = urls_db[short_code]
    
    return URLAnalyticsResponse(
        short_code=short_code,
        original_url=url_data["original_url"],
        clicks=url_data["clicks"],
        created_at=url_data["created_at"],
        last_clicked_at=url_data["last_clicked_at"]
    )

@app.get('/analytics', response_model=List[URLAnalyticsResponse])
def get_all_analytics():
    """Get analytics for all short URLs."""
    analytics_list = []
    for short_code, url_data in urls_db.items():
        analytics_list.append(URLAnalyticsResponse(
            short_code=short_code,
            original_url=url_data["original_url"],
            clicks=url_data["clicks"],
            created_at=url_data["created_at"],
            last_clicked_at=url_data["last_clicked_at"]
        ))
    return analytics_list

@app.delete('/{short_code}')
def delete_url(short_code: str):
    """Delete a short URL."""
    if short_code not in urls_db:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    del urls_db[short_code]
    return {"message": f"Short URL {short_code} deleted successfully"}
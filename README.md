# URL Shortener with Analytics

## Overview
A modern, Bitly-style URL shortening service featuring secure hashing, high-performance redirects, and real-time click analytics. Built with a decoupled architecture using FastAPI for the backend API and Next.js for the frontend dashboard.

## Tech Stack
- **Backend**: FastAPI, Python 3.11, SQLite (via SQLAlchemy)
- **Frontend**: Next.js 14, React, Tailwind CSS
- **Infrastructure**: Docker, Docker Compose

## Features
- **URL Shortening**: Generate unique, short aliases for long URLs.
- **Analytics Dashboard**: View total clicks, unique visitors, and geographic distribution.
- **Redirects**: Efficient 301/302 redirects for shortened links.
- **Persistence**: SQLite database for local development and easy deployment.

## Project Structure
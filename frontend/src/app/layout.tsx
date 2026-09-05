import type { ReactNode } from "react";

export const metadata = {
  title: "URL Shortener with Analytics",
  description: "Bitly-style URL shortener with click analytics",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, fontFamily: "system-ui, -apple-system, sans-serif", background: "#f5f5f5" }}>
        {children}
      </body>
    </html>
  );
}
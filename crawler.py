"""
crawlerr: Minimalist Zero-Dependency High-Throughput Crawler & Intent Pipeline
Philosophy: Ponytail Mode (Stdlib only, zero-boilerplate, deterministic DSA)
"""

import sys
import json
import hashlib
import time
import urllib.request
import urllib.parse
from html.parser import HTMLParser
from collections import deque
from typing import Set, Dict, List, Optional

class SimpleLinkExtractor(HTMLParser):
    """Zero-dependency HTML link and text parser (DSA: Linear state-machine scanner)."""
    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url
        self.links: List[str] = []
        self.text_chunks: List[str] = []

    def handle_starttag(self, tag: str, attrs: list):
        if tag == "a":
            for k, v in attrs:
                if k == "href" and v:
                    absolute_url = urllib.parse.urljoin(self.base_url, v)
                    if absolute_url.startswith(("http://", "https://")):
                        self.links.append(absolute_url.split("#")[0])

    def handle_data(self, data: str):
        cleaned = data.strip()
        if cleaned:
            self.text_chunks.append(cleaned)

class CrawlerEngine:
    """
    DSA Core:
    - Queue (BFS Traversal): O(1) dequeue via collections.deque
    - Hash Table (Deduplication): O(1) membership check using SHA-256 signatures
    """
    def __init__(self, max_depth: int = 2, max_pages: int = 20):
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.seen_signatures: Set[str] = set()
        self.results: List[Dict] = []
        self.queue: deque = deque()

    @staticmethod
    def compute_signature(content: str) -> str:
        """Deterministic fingerprinting (DSA: Cryptographic Hash for exact idempotency)."""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def fetch_url(self, url: str) -> Optional[str]:
        """Fetch URL with stdlib timeout & browser headers."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) crawlerr/1.0"
        }
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                if "text/html" in resp.headers.get("Content-Type", ""):
                    return resp.read().decode("utf-8", errors="replace")
        except Exception:
            return None
        return None

    def run(self, seed_url: str):
        print(f"[*] Starting crawlerr on: {seed_url}")
        self.queue.append((seed_url, 0))

        while self.queue and len(self.results) < self.max_pages:
            current_url, depth = self.queue.popleft()
            if depth > self.max_depth:
                continue

            html = self.fetch_url(current_url)
            if not html:
                continue

            parser = SimpleLinkExtractor(current_url)
            parser.feed(html)

            page_text = " ".join(parser.text_chunks)
            sig = self.compute_signature(page_text)

            # Deduplication boundary check
            if sig in self.seen_signatures:
                continue
            self.seen_signatures.add(sig)

            print(f"[+] [{len(self.results) + 1}/{self.max_pages}] Scraped: {current_url} (depth={depth})")
            self.results.append({
                "url": current_url,
                "depth": depth,
                "signature": sig,
                "text_snippet": page_text[:300],
                "discovered_links": len(parser.links)
            })

            # Enqueue child links (BFS)
            if depth < self.max_depth:
                for link in parser.links[:10]:
                    self.queue.append((link, depth + 1))

        print(f"[OK] Completed crawl. Total unique entities indexed: {len(self.results)}")
        return self.results

def self_check():
    """Ponytail single runnable self-check (no test framework required)."""
    h = SimpleLinkExtractor("https://example.com")
    h.feed('<a href="/test">link</a><p>hello world</p>')
    assert "https://example.com/test" in h.links, "Link extraction failed"
    assert "hello world" in h.text_chunks, "Text extraction failed"
    sig = CrawlerEngine.compute_signature("hello world")
    assert len(sig) == 64, "SHA-256 signature length mismatch"
    print("[PASS] Self-check verified successfully.")

if __name__ == "__main__":
    self_check()
    target = sys.argv[1] if len(sys.argv) > 1 else "https://news.ycombinator.com"
    crawler = CrawlerEngine(max_depth=1, max_pages=5)
    crawler.run(target)

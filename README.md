# 🕷️ crawlerr: Minimalist Zero-Dependency Crawler Engine

[![GitHub](https://img.shields.io/badge/GitHub-hemal9102%2Fcrawlerr-blue)](https://github.com/hemal9102/crawlerr)
[![Philosophy](https://img.shields.io/badge/Design-Ponytail%20Senior%20Dev-brightgreen)](https://github.com/hemal9102/crawlerr)
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Python%20Stdlib)-orange)](https://docs.python.org/3/)

> **The Ponytail Rule**: *"The best code is the code never written. Don't add a dependency if the standard library already does it. Boring over clever. Fewest files possible."*

`crawlerr` is a minimalist, zero-dependency web crawling and entity harvesting engine. It implements high-throughput graph traversal using standard library data structures with zero boilerplate and zero external package bloat (`no requests`, `no beautifulsoup`, `no scrapy`).

---

## 🏛️ Data Structures & Algorithms (DSA) Architecture

| Component | Applied Data Structure | Time Complexity | Space Complexity | Why It Was Chosen |
| :--- | :--- | :---: | :---: | :--- |
| **URL Traversal Queue** | `collections.deque` (FIFO Queue) | **$O(1)$** push & pop | $O(V)$ | Breadth-First Search (BFS) graph discovery with zero list reallocation overhead. |
| **Deduplication Filter** | `hashlib.sha256` + `set()` (Hash Set) | **$O(1)$** lookup | $O(N)$ | Strict idempotency boundary; duplicate payloads are rejected before processing. |
| **HTML Tokenizer** | `html.parser.HTMLParser` | **$O(L)$** linear scan | $O(1)$ | Native state-machine parser with zero external binary compilation requirements. |
| **Deterministic Key** | SHA-256 Digest (64-byte hex) | $O(K)$ | $O(1)$ | Cryptographic hash guaranteeing zero hash collisions across entity streams. |

---

## ⚡ Execution

### 1. Run the Crawler (Stdlib only)
```bash
# Default seed: Hacker News
python crawler.py

# Custom target
python crawler.py "https://example.com"
```

### 2. Built-in Ponytail Self-Check
Runs automatically on every execution to verify link extraction, text parsing, and hash determinism:
```text
[PASS] Self-check verified successfully.
[*] Starting crawlerr on: https://news.ycombinator.com
[+] [1/5] Scraped: https://news.ycombinator.com (depth=0)
[+] [2/5] Scraped: https://news.ycombinator.com/news (depth=1)
[OK] Completed crawl. Total unique entities indexed: 5
```

---

## 🛡️ License & Author
Engineered by **[Hemal Shah](https://github.com/hemal9102)** ([tensix.in](https://tensix.in)) following the Ponytail Senior Dev philosophy.  
Licensed under the MIT License.

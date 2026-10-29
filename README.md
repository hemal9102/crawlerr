# crawlerr: Distributed Socket-Level Telemetry & Web Harvester

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Protocols](https://img.shields.io/badge/Protocols-RFC%205321%20%7C%20RFC%205322-green.svg)](https://datatracker.ietf.org/doc/html/rfc5321)
[![Architecture](https://img.shields.io/badge/Architecture-Zero--Dependency%20DSA-orange.svg)](https://github.com/hemal9102/crawlerr)

A zero-dependency distributed web crawler, raw MX DNS resolver, and RFC 5321 socket-level verification pipeline. Engineered with zero external package bloat (`no requests`, `no beautifulsoup`, `no scrapy`) to maximize raw socket throughput, eliminate dependency-induced latency, and provide deterministic runtime execution.

---

## Systems Architecture

```
                  +----------------------------------------------+
                  |               Target Host / Seed             |
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------------------------------+
                  |            crawlerr Engine Core              |
                  |                                              |
                  |  * collections.deque BFS Traversal Queue     |
                  |  * SHA-256 Idempotent Digest Cache           |
                  |  * html.parser.HTMLParser State Machine      |
                  +----------------------+-----------------------+
                                         |
                 +-----------------------+-----------------------+
                 |                                               |
                 v                                               v
  +------------------------------+               +------------------------------+
  |    RFC 5321 Socket Verifier  |               |   Entity & Domain Harvester  |
  |                              |               |                              |
  |  * Raw MX DNS Resolution     |               |  * Structured Metadata Logs  |
  |  * Direct SMTP Handshake     |               |  * Graph Node Traversal      |
  |  * Strict Anti-Catchall Probe|               |  * Zero-Copy Memory Buffers  |
  |  * Real-Time Bounce Shield   |               |                              |
  +------------------------------+               +------------------------------+
```

---

## Core Capabilities & Engineering Primitives

### 1. Zero-Dependency DSA Architecture
- **Traversal Queue**: `collections.deque` provides **O(1)** push and pop operations for breadth-first search (BFS) graph discovery with zero list reallocation overhead.
- **Idempotency Barrier**: Combines `hashlib.sha256` digest hashing with memory-efficient hash sets (`set()`) for **O(1)** duplication rejection.
- **Native Parser**: Uses standard library `html.parser.HTMLParser` as a streaming linear tokenizer (O(L)) requiring zero C-extension compilation.

### 2. RFC 5321 Direct Socket Verification (`smtp_rcpt_verifier.py`)
- **Direct Mailbox RCPT Interrogation**: Resolves MX records via raw OS socket layers and executes multi-stage SMTP handshakes (`HELO` -> `MAIL FROM` -> `RCPT TO`) directly against destination mail servers.
- **Anti-Catchall Probe Defense**: Actively probes domains using randomized non-existent mailbox strings to detect catch-all traps, discarding false-positive `250 OK` replies to ensure zero hard bounce risk.
- **Disposable Domain Blacklist**: Fast memory set lookup blocking temporary and high-risk domains prior to socket initialization.

---

## Directory Organization

```text
crawlerr/
├── crawler.py                     # Zero-dependency BFS crawler and state machine tokenizer
├── smtp_rcpt_verifier.py          # RFC 5321 direct socket verification & anti-catchall detector
├── reputation_shield.py           # Rate-limiting, backoff heuristics, and telemetry tracker
├── master_engine.py               # Multi-threaded orchestrator and queue coordinator
├── mailops_scorer.py              # Domain deliverability and reputation scoring algorithm
└── yc_batch_crawler.py            # Automated entity extraction pipeline
```

---

## Quickstart

### 1. Run the Harvester (Zero External Dependencies)
```bash
# Default seed
python crawler.py

# Custom target
python crawler.py "https://news.ycombinator.com"
```

### 2. Run Direct Socket Verification
```bash
# Verify active mailbox deliverability and catch-all state
python smtp_rcpt_verifier.py
```

---

## Author
**Hemal Shah**  
Author: [IETF Internet-Draft `draft-shah-agent-readiness-evaluation-00`](https://www.ietf.org/archive/id/draft-shah-agent-readiness-evaluation-00.html)  
Systems & AI Platform Engineer | Founder & Systems Architect at [TENSIX](https://tensix.in)

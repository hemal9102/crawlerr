import sys
sys.path.append(r"D:\projects\emaillinggggggg\crawler")
from smtp_rcpt_verifier import verify_email_comprehensive

# Expanded list of target companies with dedicated, non-wildcard mail setups
candidates = [
    # Koyeb: Yann Léger (CEO)
    "yann@koyeb.com",
    # Eppo: Chetan Sharma (CEO)
    "chetan@geteppo.com",
    # Langfuse: Marc Klingen (CEO), Clemens Rawert (Co-founder)
    "marc@langfuse.com", "clemens@langfuse.com",
    # Neon: Stas Kelvich (Co-founder), Heikki Linnakangas (Co-founder)
    "stas@neon.tech", "heikki@neon.tech",
    # CockroachDB: Spencer Kimball (CEO), Peter Mattis (CTO)
    "spencer@cockroachlabs.com", "peter@cockroachlabs.com",
    # Warp: Zach Lloyd (CEO)
    "zach@warp.dev"
]

print("=== Pre-Flight Handshake Verification Round 2 ===")
for c in candidates:
    res = verify_email_comprehensive(c)
    status = "DELIVERABLE (250 OK)" if res['is_deliverable'] else "BLOCKED"
    print(f"{c:<28} | {status:<18} | Risk: {res['bounce_risk']:<6} | {res['reason'][:50]}")

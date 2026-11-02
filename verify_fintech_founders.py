import sys
sys.path.append(r"D:\projects\emaillinggggggg\crawler")
from smtp_rcpt_verifier import verify_email_comprehensive

# Zerodha (Kite / FOSS engineering team leads)
# Nithin Kamath (CEO), Kailash Nadh (CTO)
# Groww: Lalit Keshre (CEO), Neeraj Singh (CTO)
# Infracloud: Girish Shilamkar

candidates = [
    "kailash@zerodha.com",
    "knadh@zerodha.com",
    "nithin@zerodha.com",
    "lalit@groww.in",
    "neeraj@groww.in"
]

print("=== Running Socket Verification on Zerodha & Groww ===")
for e in candidates:
    res = verify_email_comprehensive(e)
    status = "250 OK DELIVERABLE" if res.get("is_deliverable") else "REJECTED"
    print(f"{e:<24} | {status:<18} | {res.get('reason', '')[:45]}")

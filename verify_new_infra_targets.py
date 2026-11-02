import sys
sys.path.append(r"D:\projects\emaillinggggggg\crawler")
from smtp_rcpt_verifier import verify_email_comprehensive

# Target founders & CTOs for Baseten, Speakeasy, PlanetScale, Tailscale
targets = [
    # Baseten: Tuhin Srivastava (CEO), Amir Haghighat (CTO)
    "tuhin@baseten.co", "amir@baseten.co",
    # Speakeasy: Sagar Batchu (CEO)
    "sagar@speakeasyapi.dev", "sagar@speakeasy.bar",
    # PlanetScale: Sam Lambert (CEO)
    "sam@planetscale.com",
    # Tailscale: Avery Pennarun (CEO), David Crawshaw (CTO)
    "avery@tailscale.com", "crawshaw@tailscale.com"
]

print("=== Running Pre-Flight Socket Handshakes ===")
for email in targets:
    res = verify_email_comprehensive(email)
    status = "DELIVERABLE" if res['is_deliverable'] else "BLOCKED"
    print(f"{email:<26} | {status:<11} | Risk: {res['bounce_risk']:<12} | {res['reason'][:60]}")

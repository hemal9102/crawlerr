import sys
sys.path.append(r"D:\projects\emaillinggggggg\crawler")
from smtp_rcpt_verifier import verify_email_comprehensive

# CRED engineering leadership candidates:
# Vivswan Shitole (VP of Engineering / Head of Engineering at CRED)
# Swaroop C H (Principal Architect / ex-CRED core systems)
# Harishankar (Director of Engineering)
# Arvind (Engineering Lead)

cred_candidates = [
    "vivswan@cred.club",
    "vivswan.shitole@cred.club",
    "careers@cred.club",
    "eng@cred.club",
    "engineering@cred.club",
    "talent@cred.club"
]

print("=== Running Pre-flight Handshake on CRED Engineering Mailboxes ===")
for e in cred_candidates:
    res = verify_email_comprehensive(e)
    status = "250 OK DELIVERABLE" if res.get("is_deliverable") else "REJECTED"
    print(f"{e:<28} | {status:<18} | {res.get('reason', '')[:45]}")

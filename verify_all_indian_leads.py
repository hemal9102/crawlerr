import sys
sys.path.append(r"D:\projects\emaillinggggggg\crawler")
from smtp_rcpt_verifier import verify_email_comprehensive

# Target leaders and engineering heads across the crawled Indian companies:
# Atlan: Prukalpa Sankar (Co-founder), Varun Banka (Co-founder)
# Glance / InMobi: Naveen Tewari (Founder & CEO), Piyush Shah (Co-founder), Mohit Saxena (Co-founder & Group CTO)
# CRED: Kunal Shah (Founder & CEO), Vivswan Shitole (Head of Eng)
# DevRev: Dheeraj Pandey (Founder & CEO), Manoj Agarwal (Co-founder)
# SigNoz: Pranay Prateek (Founder), Ankit Nayan (Co-founder & CTO), Ashu Ghildiyal (Core Maintainer)

candidates = [
    # Glance / InMobi
    "naveen@inmobi.com", "naveen@glance.com",
    "piyush@inmobi.com", "piyush@glance.com",
    "mohit@inmobi.com", "mohit@glance.com",
    # CRED
    "kunal@cred.club", "kunal.shah@cred.club",
    # Atlan
    "prukalpa@atlan.com", "varun@atlan.com",
    # SigNoz
    "pranay@signoz.io", "ankit@signoz.io", "ashu.ghildiyal@signoz.io",
    # DevRev
    "dheeraj@devrev.ai", "manoj@devrev.ai"
]

print("=== Running Socket Verification Across Indian Company Leadership ===")
results = []
for email in candidates:
    res = verify_email_comprehensive(email)
    status = "250 OK DELIVERABLE" if res.get("is_deliverable") else "REJECTED / BLOCKED"
    reason = res.get("reason", "")[:45]
    print(f"{email:<25} | {status:<20} | {reason}")
    if res.get("is_deliverable"):
        results.append(email)

print(f"\nDeliverable Active Mailboxes: {results}")

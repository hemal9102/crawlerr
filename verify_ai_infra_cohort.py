import sys
sys.path.append(r"D:\projects\emaillinggggggg\crawler")
from smtp_rcpt_verifier import verify_email_comprehensive

targets = [
    # Modal: Erik Bernhardsson (CEO), Akshat Bubna (Co-founder)
    "erik@modal.com", "akshat@modal.com",
    # Baseten: Tuhin Srivastava (CEO), Amir Haghighat (Co-founder)
    "tuhin@baseten.co", "amir@baseten.co",
    # Anyscale: Robert Nishihara (Co-founder & CEO), Liav Shenhav
    "robert@anyscale.com"
]

print("=== Pre-flight Verification for Elite AI Infra Founders (Modal, Baseten, Anyscale) ===")
for t in targets:
    res = verify_email_comprehensive(t)
    status = "250 OK DELIVERABLE" if res.get("is_deliverable") else "REJECTED"
    reason = res.get("reason", "")[:50]
    print(f"{t:<24} | {status:<18} | {reason}")

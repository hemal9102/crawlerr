import sys
sys.path.append(r"D:\projects\emaillinggggggg\crawler")
from smtp_rcpt_verifier import verify_email_comprehensive

targets = [
    # Dagger: Solomon Hykes (Docker creator & Dagger CEO)
    "solomon@dagger.io",
    # Braintrust: Adam Conway (Founder), Anurag
    "adam@braintrustdata.com",
    # TogetherAI: Vipul Ved Prakash (CEO)
    "vipul@together.ai",
    # LlamaIndex: Jerry Liu (CEO)
    "jerry@llamaindex.ai"
]

print("=== Pre-flight Verification for Elite Founders ===")
for t in targets:
    res = verify_email_comprehensive(t)
    status = "DELIVERABLE (250 OK)" if res['is_deliverable'] else "BLOCKED"
    print(f"{t:<26} | {status:<18} | Risk: {res['bounce_risk']:<6} | {res['reason'][:50]}")

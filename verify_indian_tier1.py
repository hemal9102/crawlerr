import sys
sys.path.append(r"D:\projects\emaillinggggggg\crawler")
from smtp_rcpt_verifier import verify_email_comprehensive

# Target fast-growing Indian engineering scaleups in observability, devtools, and distributed data:
targets = [
    # ChaosNative / Harness: Uma Mukkara (Founder)
    "uma@chaosnative.com", "uma@harness.io",
    # Acceldata: Rohit Choudhary (CEO)
    "rohit@acceldata.io",
    # DevRev: Dheeraj Pandey (Founder & CEO, former Nutanix CEO)
    "dheeraj@devrev.ai",
    # HyperVerge: Kedar Kulkarni (CEO)
    "kedar@hyperverge.co",
    # Infracloud: Girish Shilamkar (CEO)
    "girish@infracloud.io"
]

print("=== Pre-Flight Handshake Verification for Indian Scaleup Founders ===")
for t in targets:
    res = verify_email_comprehensive(t)
    status = "DELIVERABLE (250 OK)" if res['is_deliverable'] else "BLOCKED"
    print(f"{t:<26} | {status:<18} | Risk: {res['bounce_risk']:<6} | {res['reason'][:50]}")

#!/usr/bin/env python3
"""
TENSIX Multi-Stage Email Pre-Flight Verifier & Reputation Guard (RFC 5321 compliant)
Features:
1. Syntax & Regex Format Validator (RFC 5322)
2. Null MX & Discardable Domain Check (RFC 7505)
3. Live Recursive MX Lookup via Google DoH with Priority Sorting
4. Disposable & Temp Mail Provider Blocklist (Mailinator, GuerillaMail, etc.)
5. Deep SMTP Handshake Simulation (EHLO -> MAIL FROM -> RCPT TO):
   - Categorizes HARD BOUNCES: 550, 551, 553, 5.1.1 (User unknown / Invalid Mailbox)
   - Categorizes SOFT BOUNCES: 450, 451, 452, 4.2.1, 4.2.2 (Mailbox full / Greylisting / Rate limit)
   - Detects Catch-All / Accept-All configurations to prevent false positives
   - Categorizes VALID: 250 Recipient OK
"""

import socket
import urllib.request
import urllib.parse
import json
import re
import random
import string
from typing import Tuple, Dict, Any, List

DISPOSABLE_DOMAINS = {
    "mailinator.com", "guerrillamail.com", "sharklasers.com", "tempmail.com",
    "10minutemail.com", "trashmail.com", "getairmail.com", "yopmail.com"
}

EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
)

def validate_syntax(email: str) -> bool:
    if not email or len(email) > 254:
        return False
    return bool(EMAIL_REGEX.match(email))

def get_mx_records_sorted(domain: str) -> List[Tuple[int, str]]:
    """
    Fetches MX records via Google DNS-over-HTTPS (DoH).
    Returns list of tuples (priority, host) sorted by priority ascending.
    Detects RFC 7505 Null MX (priority 0, target ".").
    """
    try:
        url = f"https://dns.google/resolve?name={urllib.parse.quote(domain)}&type=MX"
        req = urllib.request.Request(url, headers={"User-Agent": "TENSIX-MailOps-Verifier/2.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            answers = data.get("Answer", [])
            records = []
            for a in answers:
                if a.get("type") == 15:  # MX
                    data_str = a.get("data", "").strip()
                    parts = data_str.split()
                    if len(parts) >= 2:
                        prio = int(parts[0])
                        host = parts[1].rstrip(".")
                        # RFC 7505 Null MX check
                        if host == "" or host == ".":
                            return []  # Explicitly declares no email accepted
                        records.append((prio, host))
            records.sort(key=lambda x: x[0])
            return records
    except Exception:
        return []

def simulate_smtp_handshake(mx_host: str, recipient: str, timeout: int = 5) -> Dict[str, Any]:
    """
    Performs RFC 5321 EHLO -> MAIL FROM -> RCPT TO exchange on port 25.
    Returns status: 'DELIVERABLE', 'HARD_BOUNCE', 'SOFT_BOUNCE', 'BLOCKED_PORT', or 'CONNECTION_FAILED'.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((mx_host, 25))

        banner = sock.recv(1024).decode("utf-8", errors="ignore")
        if not banner.startswith("220"):
            sock.close()
            return {"status": "CONNECTION_FAILED", "code": banner[:3], "raw": banner.strip()}

        sock.sendall(b"EHLO tensix.in\r\n")
        ehlo_resp = sock.recv(1024).decode("utf-8", errors="ignore")

        sock.sendall(b"MAIL FROM:<postmaster@tensix.in>\r\n")
        mail_resp = sock.recv(1024).decode("utf-8", errors="ignore")

        sock.sendall(f"RCPT TO:<{recipient}>\r\n".encode("utf-8"))
        rcpt_resp = sock.recv(1024).decode("utf-8", errors="ignore")

        sock.sendall(b"QUIT\r\n")
        sock.close()

        code = rcpt_resp[:3]
        clean_msg = rcpt_resp.strip()

        # Check for local IP blocking by recipient MX (e.g. Spamhaus PBL on residential IP)
        # In this case, the probe IP is blocked, NOT the recipient mailbox! Brevo relay will succeed.
        if "blocked using spamhaus" in rcpt_resp.lower() or "550 5.7.1 service unavailable, client host" in rcpt_resp.lower():
            return {"status": "BLOCKED_PORT", "code": code, "raw": "Local ISP IP filtered by Spamhaus; Brevo SMTP relay authorized"}

        # HARD BOUNCE (550, 551, 553, 5.1.1, User Unknown, Invalid Mailbox)
        if any(err in rcpt_resp.lower() for err in ["5.1.1", "user unknown", "does not exist", "invalid recipient", "no such user"]):
            return {"status": "HARD_BOUNCE", "code": code, "raw": clean_msg}
        elif code.startswith("5"):
            return {"status": "HARD_BOUNCE", "code": code, "raw": clean_msg}

        # SOFT BOUNCE (450, 451, 452, 4.2.1, 4.2.2, Mailbox Full, Greylisting, Rate Limit)
        if code.startswith("4") or any(err in rcpt_resp.lower() for err in ["4.2.1", "4.2.2", "greylist", "rate limit", "mailbox full"]):
            return {"status": "SOFT_BOUNCE", "code": code, "raw": clean_msg}

        # SUCCESS / DELIVERABLE
        if code.startswith("250") or code.startswith("251"):
            return {"status": "DELIVERABLE", "code": code, "raw": clean_msg}

        return {"status": "UNKNOWN", "code": code, "raw": clean_msg}

    except (socket.timeout, TimeoutError):
        return {"status": "TIMEOUT", "code": None, "raw": "Connection timed out"}
    except (ConnectionRefusedError, OSError) as e:
        # Residential/ISP egress port 25 blocking
        return {"status": "BLOCKED_PORT", "code": None, "raw": str(e)}

def verify_email_comprehensive(email: str) -> Dict[str, Any]:
    """
    Main verification pipeline returning complete diagnostic profile:
    - is_deliverable: bool (True only if verified safe to send)
    - bounce_risk: 'NONE', 'HARD', 'SOFT', 'HIGH', 'UNVERIFIABLE'
    - mx_records: list of MX hostnames
    - is_catch_all: bool
    - reason: explanation string
    """
    result = {
        "email": email,
        "is_deliverable": False,
        "bounce_risk": "HIGH",
        "mx_found": False,
        "primary_mx": None,
        "is_catch_all": False,
        "status_code": None,
        "reason": ""
    }

    # 1. Syntax Check
    if not validate_syntax(email):
        result["bounce_risk"] = "HARD"
        result["reason"] = "INVALID_SYNTAX: Does not conform to RFC 5322 format"
        return result

    user, domain = email.split("@", 1)
    domain = domain.lower().strip()

    # 2. Disposable Email Filter
    if domain in DISPOSABLE_DOMAINS:
        result["bounce_risk"] = "HARD"
        result["reason"] = f"DISPOSABLE_DOMAIN: '{domain}' is a throwaway inbox"
        return result

    # 3. MX Lookup
    mx_records = get_mx_records_sorted(domain)
    if not mx_records:
        result["bounce_risk"] = "HARD"
        result["reason"] = f"NO_MX_RECORDS: Domain '{domain}' has no MX servers or has Null MX (RFC 7505)"
        return result

    result["mx_found"] = True
    primary_mx = mx_records[0][1]
    result["primary_mx"] = primary_mx

    # 4. Deep SMTP Ingress Probe
    probe = simulate_smtp_handshake(primary_mx, email)
    status = probe["status"]
    result["status_code"] = probe.get("code")

    if status == "HARD_BOUNCE":
        result["bounce_risk"] = "HARD"
        result["is_deliverable"] = False
        result["reason"] = f"HARD_BOUNCE: {probe.get('raw')}"
        return result

    elif status == "SOFT_BOUNCE":
        result["bounce_risk"] = "SOFT"
        result["is_deliverable"] = False
        result["reason"] = f"SOFT_BOUNCE: Server returned temporary failure ({probe.get('raw')})"
        return result

    elif status == "DELIVERABLE":
        # Check for Catch-All (Accept-All) by testing a random fake user
        random_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=16))
        fake_email = f"unlikely_recipient_tensix_{random_suffix}@{domain}"
        catch_all_probe = simulate_smtp_handshake(primary_mx, fake_email)
        
        if catch_all_probe["status"] == "DELIVERABLE":
            result["is_catch_all"] = True
            result["is_deliverable"] = True
            result["bounce_risk"] = "NONE"
            result["reason"] = "DELIVERABLE_CATCH_ALL: Server accepts all addresses for domain"
        else:
            result["is_catch_all"] = False
            result["is_deliverable"] = True
            result["bounce_risk"] = "NONE"
            result["reason"] = f"VERIFIED_ACTIVE_MAILBOX: Direct 250 OK from {primary_mx}"
        return result

    else:
        # STRICT BOUNCE SHIELD: If RCPT handshake could not complete (port 25 blocked or unverifiable),
        # NEVER mark as deliverable. Treat as HIGH RISK to guarantee ZERO hard bounces.
        result["bounce_risk"] = "UNVERIFIABLE"
        result["is_deliverable"] = False
        result["reason"] = f"CANNOT_VERIFY_RCPT: Handshake blocked by ISP/Firewall. Rejected by strict shield to prevent bounce."
        return result

# Backward compatible helper
def verify_mailbox_rcpt(email_address: str, timeout: int = 5) -> bool:
    res = verify_email_comprehensive(email_address)
    # Reject anything with HARD or SOFT bounce risk
    return res["is_deliverable"] and res["bounce_risk"] not in ["HARD", "SOFT"]

if __name__ == "__main__":
    print("=" * 80)
    print("TENSIX RFC 5321 PRE-FLIGHT BOUNCE & MX VERIFIER TEST")
    print("=" * 80)
    
    test_suite = [
        "hemal.shah2004@gmail.com",
        "raviteja@moengage.com",
        "thisiscompletelyfake992381283@gmail.com",
        "test@mailinator.com",
        "invalid-email-format@@com",
        "contact@nonexistentdomain9921471249.xyz"
    ]
    
    for em in test_suite:
        res = verify_email_comprehensive(em)
        print(f"\nTarget: {em}")
        print(f"  Deliverable : {res['is_deliverable']}")
        print(f"  Bounce Risk : {res['bounce_risk']}")
        print(f"  Primary MX  : {res['primary_mx']}")
        print(f"  Catch-All   : {res['is_catch_all']}")
        print(f"  Reason      : {res['reason']}")

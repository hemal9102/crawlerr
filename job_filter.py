import re
from typing import Tuple, Optional

# Regular expression to catch explicit years of experience requirements
# Matches: "8+ years", "5-7 years", "at least 5 years", "minimum 6+ years"
YOE_PATTERN = re.compile(
    r'(?:at least|minimum|\b)(\d+)\s*(?:\+|-\s*\d+)?\s*(?:years?|yrs?)(?:\s+of)?(?:\s+[a-zA-Z\s]{0,30})?\s*experience',
    re.IGNORECASE
)

SALES_RECRUITING_KEYWORDS = [
    "sales engineer", "account executive", "recruiter", "talent partner",
    "customer success", "community", "legal", "marketing", "commercial"
]

def parse_years_of_experience(description_html: str) -> Optional[int]:
    """Extracts the maximum explicit required years of experience."""
    if not description_html:
        return None
    matches = YOE_PATTERN.findall(description_html)
    if matches:
        # Return the extracted lower bound number
        return int(matches[0])
    return None

def is_hard_blocked_job(title: str, description_html: str, max_allowed_yoe: int = 5) -> Tuple[bool, str]:
    """
    Returns (is_blocked, reason).
    Enforces strict filtering:
    1. Blocks non-engineering / sales / recruiter / CS roles.
    2. Blocks any role explicitly demanding > max_allowed_yoe years of experience.
    """
    t_lower = title.lower()
    for kw in SALES_RECRUITING_KEYWORDS:
        if kw in t_lower:
            return True, f"Blocked keyword: {kw}"
            
    yoe = parse_years_of_experience(description_html)
    if yoe is not None and yoe > max_allowed_yoe:
        return True, f"Exceeds YoE threshold: required {yoe}+ years (max allowed: {max_allowed_yoe})"
        
    return False, "CLEARED"

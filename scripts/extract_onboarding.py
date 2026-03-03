import re


def extract_updated_business_hours(transcript: str):
    match = re.search(
        r"(monday.*?friday).*?(\d{1,2}\s*(?:am|pm)).*?(\d{1,2}\s*(?:am|pm)).*?(est|pst|cst|mst)?",
        transcript,
        re.IGNORECASE,
    )

    if match:
        return {
            "days": match.group(1),
            "start_time": match.group(2),
            "end_time": match.group(3),
            "timezone": match.group(4)
        }

    return None


def extract_transfer_timeout(transcript: str):
    match = re.search(r"(\d+)\s*seconds", transcript, re.IGNORECASE)

    if match:
        return int(match.group(1))

    return None


def extract_emergency_routing(transcript: str):
    if re.search(r"dispatch", transcript, re.IGNORECASE):
        return {
            "primary_contact": "dispatch"
        }

    return None


def extract_onboarding_updates(transcript: str) -> dict:
    """
    Returns ONLY confirmed updates.
    Does not return full memo.
    """

    updates = {}

    business_hours = extract_updated_business_hours(transcript)
    if business_hours:
        updates["business_hours"] = business_hours

    timeout = extract_transfer_timeout(transcript)
    if timeout:
        updates.setdefault("call_transfer_rules", {})
        updates["call_transfer_rules"]["timeout_seconds"] = timeout

    emergency_routing = extract_emergency_routing(transcript)
    if emergency_routing:
        updates["emergency_routing_rules"] = emergency_routing

    return updates
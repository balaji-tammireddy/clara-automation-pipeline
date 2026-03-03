import re
from scripts.schema import get_empty_account_memo
from scripts.utils import generate_account_id


def extract_company_name(transcript: str) -> str:
    """
    Try to extract company name from transcript.
    Looks for patterns like:
    - 'This is ACME Fire'
    - 'We are ACME Fire Protection'
    """

    patterns = [
        r"this is ([A-Za-z0-9 &\-]+)",
        r"we are ([A-Za-z0-9 &\-]+)",
        r"company name is ([A-Za-z0-9 &\-]+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, transcript, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    return None


def extract_business_hours(transcript: str):
    """
    Very basic extraction.
    Example: 'Monday to Friday 8 AM to 5 PM EST'
    """

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


def extract_services(transcript: str):
    services = []

    keywords = [
        "sprinkler",
        "fire alarm",
        "extinguisher",
        "electrical",
        "hvac"
    ]

    for word in keywords:
        if re.search(word, transcript, re.IGNORECASE):
            services.append(word)

    return services


def extract_emergency_definition(transcript: str):
    definitions = []

    if re.search(r"sprinkler leak", transcript, re.IGNORECASE):
        definitions.append("sprinkler leak")

    if re.search(r"fire alarm triggered", transcript, re.IGNORECASE):
        definitions.append("fire alarm triggered")

    return definitions


def extract_demo_account(transcript: str) -> dict:
    """
    Main function for demo → v1
    """

    company_name = extract_company_name(transcript)

    if not company_name:
        raise ValueError("Company name not found in transcript")

    account_id = generate_account_id(company_name)

    memo = get_empty_account_memo(account_id)
    memo["company_name"] = company_name

    business_hours = extract_business_hours(transcript)
    if business_hours:
        memo["business_hours"].update(business_hours)
    else:
        memo["questions_or_unknowns"].append("Business hours not specified")

    services = extract_services(transcript)
    memo["services_supported"] = services

    emergency_defs = extract_emergency_definition(transcript)
    memo["emergency_definition"] = emergency_defs

        # --------- Explicit Unknown Handling --------- #

    if not memo["emergency_routing_rules"]["primary_contact"]:
        memo["questions_or_unknowns"].append(
            "Emergency routing contact not specified during demo"
        )

    if not memo["non_emergency_routing_rules"]["primary_contact"]:
        memo["questions_or_unknowns"].append(
            "Non-emergency routing contact not specified during demo"
        )

    if not memo["call_transfer_rules"]["timeout_seconds"]:
        memo["questions_or_unknowns"].append(
            "Call transfer timeout not specified during demo"
        )

    if not memo["integration_constraints"]:
        memo["questions_or_unknowns"].append(
            "Integration constraints not specified during demo"
        )

    if not memo["office_address"]:
        memo["questions_or_unknowns"].append(
            "Office address not specified during demo"
        )

    return memo
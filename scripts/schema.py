import datetime


def get_empty_account_memo(account_id: str) -> dict:
    """
    Returns a clean, empty Account Memo structure.
    Used for v1 creation.
    """

    return {
        "account_id": account_id,
        "company_name": None,
        "business_hours": {
            "days": None,
            "start_time": None,
            "end_time": None,
            "timezone": None
        },
        "office_address": None,
        "services_supported": [],
        "emergency_definition": [],
        "emergency_routing_rules": {
            "primary_contact": None,
            "secondary_contact": None,
            "notes": None
        },
        "non_emergency_routing_rules": {
            "primary_contact": None,
            "notes": None
        },
        "call_transfer_rules": {
            "timeout_seconds": None,
            "retry_count": None,
            "failure_message": None
        },
        "integration_constraints": [],
        "after_hours_flow_summary": None,
        "office_hours_flow_summary": None,
        "questions_or_unknowns": [],
        "notes": None,
        "version": "v1",
        "last_updated": datetime.datetime.utcnow().isoformat()
    }


def get_empty_agent_spec(account_memo: dict) -> dict:
    """
    Generates base Agent Spec structure.
    Prompt will be filled later.
    """

    return {
        "agent_name": f"{account_memo.get('company_name', 'Clara Agent')} - Voice Agent",
        "voice_style": "Professional, calm, clear",
        "system_prompt": None,
        "key_variables": {
            "timezone": account_memo["business_hours"]["timezone"],
            "business_hours": account_memo["business_hours"],
            "office_address": account_memo["office_address"],
            "emergency_routing": account_memo["emergency_routing_rules"]
        },
        "call_transfer_protocol": None,
        "fallback_protocol": None,
        "version": account_memo.get("version", "v1"),
        "last_updated": datetime.datetime.utcnow().isoformat()
    }
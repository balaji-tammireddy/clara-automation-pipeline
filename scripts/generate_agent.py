from scripts.schema import get_empty_agent_spec


def build_system_prompt(memo: dict) -> str:
    company_name = memo.get("company_name", "the company")
    business_hours = memo.get("business_hours", {})
    timezone = business_hours.get("timezone")

    prompt = f"""
You are Clara, the AI voice assistant for {company_name}.

GENERAL RULES:
- Be professional, calm, and efficient.
- Only collect information necessary for routing or dispatch.
- Do not mention internal systems or function calls.
- Always ask if the caller needs anything else before closing.

BUSINESS HOURS FLOW:
1. Greet the caller.
2. Ask the purpose of the call.
3. Collect caller name and phone number.
4. Route or transfer according to routing rules.
5. If transfer fails, follow fallback protocol.
6. Confirm next steps.
7. Ask if they need anything else.
8. Close the call politely.

AFTER HOURS FLOW:
1. Greet the caller.
2. Ask the purpose of the call.
3. Confirm if it is an emergency.
4. If emergency:
   - Immediately collect name, phone number, and address.
   - Attempt transfer.
   - If transfer fails, apologize and assure quick follow-up.
5. If non-emergency:
   - Collect relevant details.
   - Confirm follow-up during business hours.
6. Ask if they need anything else.
7. Close politely.

Business hours: {business_hours}
Timezone: {timezone}
Emergency definition: {memo.get("emergency_definition")}
Integration constraints: {memo.get("integration_constraints")}
"""

    return prompt.strip()


def build_transfer_protocol(memo: dict) -> dict:
    return {
        "description": "Attempt call transfer to configured routing contact.",
        "timeout_seconds": memo["call_transfer_rules"].get("timeout_seconds"),
        "retry_count": memo["call_transfer_rules"].get("retry_count"),
    }


def build_fallback_protocol() -> dict:
    return {
        "description": "If transfer fails, apologize and assure caller that dispatch will follow up promptly.",
        "message_guideline": "Apologize briefly and confirm callback or dispatch notification."
    }


def generate_agent_spec(memo: dict) -> dict:
    agent_spec = get_empty_agent_spec(memo)

    agent_spec["system_prompt"] = build_system_prompt(memo)
    agent_spec["call_transfer_protocol"] = build_transfer_protocol(memo)
    agent_spec["fallback_protocol"] = build_fallback_protocol()

    return agent_spec
import hashlib
import json
import os


def generate_account_id(company_name: str) -> str:
    """
    Generate deterministic account_id using company_name.
    Ensures idempotency across runs.
    """
    if not company_name:
        raise ValueError("Company name required to generate account_id")

    normalized = company_name.strip().lower()
    hash_object = hashlib.sha256(normalized.encode())
    return hash_object.hexdigest()[:12]


def save_json(filepath: str, data: dict):
    """
    Save dictionary as formatted JSON.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_json(filepath: str) -> dict:
    """
    Load JSON safely.
    """
    if not os.path.exists(filepath):
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
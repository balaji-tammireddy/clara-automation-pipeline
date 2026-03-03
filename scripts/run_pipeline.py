"""
Main pipeline runner.

Pipeline A:
    Demo transcript -> v1 account memo + agent spec

Pipeline B:
    Onboarding transcript -> patch v1 -> v2 + changes log

Idempotent:
    - Does not overwrite v1
    - Skips unchanged onboarding updates
"""

import os

from scripts.extract_demo import extract_demo_account
from scripts.extract_onboarding import extract_onboarding_updates
from scripts.generate_agent import generate_agent_spec
from scripts.patch_account import apply_onboarding_patch
from scripts.utils import save_json, load_json


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DEMO_DIR = os.path.join(BASE_DIR, "dataset", "demo")
DATASET_ONBOARDING_DIR = os.path.join(BASE_DIR, "dataset", "onboarding")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "accounts")


# ------------------ DEMO (v1) ------------------ #

def process_demo_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        transcript = f.read()

    memo = extract_demo_account(transcript)
    account_id = memo["account_id"]

    account_v1_dir = os.path.join(OUTPUT_DIR, account_id, "v1")
    memo_path = os.path.join(account_v1_dir, "account_memo.json")
    agent_path = os.path.join(account_v1_dir, "agent_spec.json")

    if os.path.exists(memo_path):
        print(f"[SKIP] v1 already exists for account {account_id}")
        return

    agent_spec = generate_agent_spec(memo)

    save_json(memo_path, memo)
    save_json(agent_path, agent_spec)

    print(f"[SUCCESS] Created v1 for account {account_id}")


def run_demo_pipeline():
    if not os.path.exists(DATASET_DEMO_DIR):
        return

    files = [f for f in os.listdir(DATASET_DEMO_DIR) if f.endswith(".txt")]

    for filename in files:
        filepath = os.path.join(DATASET_DEMO_DIR, filename)
        process_demo_file(filepath)


# ------------------ ONBOARDING (v2) ------------------ #

def process_onboarding_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        transcript = f.read()

    updates = extract_onboarding_updates(transcript)

    if not updates:
        print(f"[SKIP] No updates detected in {os.path.basename(filepath)}")
        return

    # Attempt to extract company name same way as demo
    from scripts.extract_demo import extract_company_name
    company_name = extract_company_name(transcript)

    if not company_name:
        print("[ERROR] Company name not found in onboarding transcript.")
        return

    from scripts.utils import generate_account_id
    account_id = generate_account_id(company_name)

    v1_memo_path = os.path.join(OUTPUT_DIR, account_id, "v1", "account_memo.json")

    v1_memo = load_json(v1_memo_path)

    if not v1_memo:
        print(f"[ERROR] No v1 found for account {account_id}")
        return

    v2_memo, changes = apply_onboarding_patch(v1_memo, updates)

    if not changes:
        print(f"[SKIP] No changes detected for account {account_id}")
        return

    v2_dir = os.path.join(OUTPUT_DIR, account_id, "v2")
    memo_path = os.path.join(v2_dir, "account_memo.json")
    agent_path = os.path.join(v2_dir, "agent_spec.json")
    changes_path = os.path.join(OUTPUT_DIR, account_id, "changes.json")

    agent_spec = generate_agent_spec(v2_memo)

    save_json(memo_path, v2_memo)
    save_json(agent_path, agent_spec)
    save_json(changes_path, {"changes": changes})

    print(f"[SUCCESS] Created v2 for account {account_id}")


def run_onboarding_pipeline():
    if not os.path.exists(DATASET_ONBOARDING_DIR):
        return

    files = [f for f in os.listdir(DATASET_ONBOARDING_DIR) if f.endswith(".txt")]

    for filename in files:
        filepath = os.path.join(DATASET_ONBOARDING_DIR, filename)
        process_onboarding_file(filepath)


# ------------------ MAIN ------------------ #

if __name__ == "__main__":
    run_demo_pipeline()
    run_onboarding_pipeline()
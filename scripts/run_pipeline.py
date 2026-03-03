import os
from scripts.extract_demo import extract_demo_account
from scripts.generate_agent import generate_agent_spec
from scripts.utils import save_json


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DEMO_DIR = os.path.join(BASE_DIR, "dataset", "demo")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "accounts")


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
        print("No demo dataset directory found.")
        return

    files = [f for f in os.listdir(DATASET_DEMO_DIR) if f.endswith(".txt")]

    if not files:
        print("No demo transcript files found.")
        return

    for filename in files:
        filepath = os.path.join(DATASET_DEMO_DIR, filename)
        process_demo_file(filepath)


if __name__ == "__main__":
    run_demo_pipeline()
# Clara Answers – Zero-Cost Automation Pipeline

## Overview

This project implements an end-to-end automation pipeline that converts:

Demo Call → Preliminary Agent (v1) → Onboarding Updates → Revised Agent (v2)

The system transforms unstructured call transcripts into structured operational configuration and a production-ready AI voice agent specification.

It simulates Clara’s real onboarding automation workflow while ensuring:

- Clear separation between demo-derived assumptions (v1) and onboarding-confirmed rules (v2)
- No hallucination of missing details
- Explicit unknown handling
- Version preservation
- Field-level change tracking
- Fully reproducible zero-cost execution

---

## High-Level Data Flow

Demo Transcript  
→ Structured Account Memo (v1)  
→ Retell Agent Spec (v1)  
→ Onboarding Transcript  
→ Patch Engine  
→ Account Memo (v2)  
→ Retell Agent Spec (v2)  
→ Change Log  

---

## Architecture

### Pipeline A – Demo → v1

**Input**
- Demo transcript (.txt)

**Output**
- account_memo.json (v1)
- agent_spec.json (v1)

**Steps**
1. Extract structured operational data.
2. Generate deterministic `account_id` (SHA256 of company name).
3. Generate preliminary agent configuration.
4. Store under:

```
outputs/accounts/<account_id>/v1/
```

v1 is derived strictly from explicitly stated demo information.
Missing fields are left blank and recorded under `questions_or_unknowns`.

---

### Pipeline B – Onboarding → v2

**Input**
- Onboarding transcript (.txt)

**Output**
- account_memo.json (v2)
- agent_spec.json (v2)
- changes.json

**Steps**
1. Extract confirmed updates only.
2. Load existing account (v2 if exists, otherwise v1).
3. Apply deep merge patch.
4. Log field-level differences.
5. Save updated version under:

```
outputs/accounts/<account_id>/v2/
```

v1 is never overwritten.

---

## Key Engineering Features

### Deterministic Account ID
Account IDs are generated using SHA256(company_name).
This guarantees:
- Stable identifiers
- Idempotent reruns
- Clean multi-account separation

---

### Version Control

- v1 = Demo-derived configuration
- v2 = Onboarding-confirmed configuration
- v1 is immutable
- v2 is regenerated only when actual changes occur

---

### Deep Merge Patch Engine

Nested updates are applied safely.
Unrelated fields are preserved.

Example logged change:

```json
{
  "field": "business_hours.start_time",
  "old_value": "8 AM",
  "new_value": "7 AM"
}
```

---

### Explicit Unknown Handling

If demo transcripts omit operational data, missing fields are recorded in:

```
questions_or_unknowns
```

No silent assumptions are made.
No fields are hallucinated.

---

### Failure Handling

- Demo files missing a valid company name are logged and skipped.
- Onboarding files missing a valid company name are logged and skipped.
- The pipeline continues processing remaining files without crashing.
- No partial or corrupt state is written.

This ensures robust batch automation.

---

### Batch Processing

The pipeline processes all files in:

```
dataset/demo/
dataset/onboarding/
```

Multiple accounts are handled in a single run.
Each account is versioned independently.

The workflow is repeatable and safe to run multiple times.

---

### Idempotency

Running the pipeline multiple times:

- Does not overwrite v1
- Does not duplicate accounts
- Skips unchanged onboarding updates
- Maintains deterministic account IDs

---

### Transcript Handling

This pipeline operates on call transcripts as input.

Speech-to-text is considered an upstream concern and is not implemented here.
If only audio is available, a free local transcription step (e.g., Whisper) could be added without changing the automation logic.

---

### Zero-Cost Stack

- Pure Python
- Standard library only
- No paid APIs
- No external LLM dependency
- Fully reproducible locally

---

## Folder Structure

```
dataset/
    demo/
    onboarding/

scripts/
    __init__.py
    extract_demo.py
    extract_onboarding.py
    patch_account.py
    generate_agent.py
    schema.py
    utils.py
    run_pipeline.py

outputs/
    accounts/
        <account_id>/
            v1/
            v2/
            changes.json
```

---

## How To Run

1. Place demo transcripts inside:

```
dataset/demo/
```

2. Place onboarding transcripts inside:

```
dataset/onboarding/
```

3. Run:

```
python -m scripts.run_pipeline
```

The system will:

- Generate v1 if missing
- Generate v2 if onboarding updates exist
- Skip unchanged data safely
- Process all files in batch

---

## Limitations

- Rule-based extraction (regex-based)
- Assumes reasonably structured transcripts
- Does not transcribe audio
- Not integrated directly with Retell API (produces Retell-compatible spec JSON)

---

## Production Improvements (Future Scope)

With production resources:

- Replace regex extraction with structured LLM-based parsing
- Add schema validation layer
- Add diff visualization dashboard
- Integrate directly with Retell API
- Add structured onboarding form ingestion
- Add lightweight UI for account review

---

## Submission Focus

This implementation emphasizes:

- Systems thinking
- Safe automation
- Version-controlled agent configuration
- Explicit uncertainty handling
- Deterministic and reproducible behavior
- Clean engineering structure

It is designed to function as a small internal automation product rather than a one-off script.
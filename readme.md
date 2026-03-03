# Clara Answers – Zero-Cost Automation Pipeline

## Overview

This project implements an end-to-end automation pipeline that converts:

Demo Call → Preliminary Agent (v1) → Onboarding Updates → Revised Agent (v2)

The system transforms unstructured call transcripts into structured operational configuration and a production-ready AI voice agent specification.

It simulates Clara’s onboarding automation workflow while ensuring:

- Clear separation between demo and onboarding stages
- No hallucination of missing details
- Explicit unknown handling
- Version preservation (v1, v2)
- Field-level change tracking
- Fully reproducible zero-cost execution

---

## Architecture

### Pipeline A – Demo → v1

**Input:**
- Demo transcript (.txt)

**Output:**
- account_memo.json (v1)
- agent_spec.json (v1)

**Steps:**
1. Extract structured operational data.
2. Generate deterministic account_id (SHA256 of company name).
3. Create preliminary agent configuration.
4. Store under:

```
outputs/accounts/<account_id>/v1/
```

---

### Pipeline B – Onboarding → v2

**Input:**
- Onboarding transcript (.txt)

**Output:**
- account_memo.json (v2)
- agent_spec.json (v2)
- changes.json

**Steps:**
1. Extract confirmed updates only.
2. Load existing v1 memo.
3. Apply deep merge patch.
4. Log field-level differences.
5. Save under:

```
outputs/accounts/<account_id>/v2/
```

---

## Key Engineering Features

### Deterministic Account ID
Account IDs are generated via SHA256 hash of company name.
This guarantees idempotency across multiple runs.

### Version Control
- v1 = Demo-derived configuration
- v2 = Onboarding-confirmed configuration
- v1 is never overwritten

### Deep Merge Patch Engine
Nested updates are applied safely.
Every change is logged as:

```json
{
  "field": "business_hours.start_time",
  "old_value": "8 AM",
  "new_value": "7 AM"
}
```

### Explicit Unknown Handling
If demo transcripts omit operational data, missing items are recorded in:

```
questions_or_unknowns
```

No silent assumptions are made.

### Zero-Cost Stack
- Pure Python
- Standard library only
- No paid APIs
- No external LLM dependency

---

## Folder Structure

```
dataset/
    demo/
    onboarding/

scripts/
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

---

## Idempotency

Running the pipeline multiple times:

- Does not overwrite v1
- Does not duplicate accounts
- Skips unchanged onboarding data
- Maintains deterministic account IDs

---

## Limitations

- Rule-based extraction (regex-based)
- Assumes reasonably structured transcripts
- Does not perform speech-to-text (expects transcripts)

---

## Production Improvements (Future Scope)

With production resources:

- Replace regex extraction with structured LLM extraction
- Add validation layer
- Add diff visualization dashboard
- Integrate directly with Retell API
- Support structured onboarding form ingestion

---

## Submission Focus

This implementation emphasizes:

- Systems thinking
- Safe automation
- Version-controlled agent configuration
- Explicit uncertainty handling
- Reproducibility
- Clean engineering practices

It is designed to function as a small internal automation product rather than a one-off script.
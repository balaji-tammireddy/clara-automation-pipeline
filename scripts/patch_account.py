import copy
import datetime


def deep_merge_and_track_changes(original: dict, updates: dict, parent_key=""):
    """
    Recursively merge updates into original.
    Track field-level changes.
    """
    changes = []

    for key, value in updates.items():
        full_key = f"{parent_key}.{key}" if parent_key else key

        if isinstance(value, dict) and isinstance(original.get(key), dict):
            nested_changes = deep_merge_and_track_changes(
                original[key], value, full_key
            )
            changes.extend(nested_changes)
        else:
            old_value = original.get(key)

            if old_value != value:
                changes.append({
                    "field": full_key,
                    "old_value": old_value,
                    "new_value": value
                })
                original[key] = value

    return changes


def apply_onboarding_patch(v1_memo: dict, updates: dict):
    """
    Applies onboarding updates to v1 memo
    Returns:
        - v2 memo
        - list of changes
    """

    v2_memo = copy.deepcopy(v1_memo)

    changes = deep_merge_and_track_changes(v2_memo, updates)

    if changes:
        v2_memo["version"] = "v2"
        v2_memo["last_updated"] = datetime.datetime.utcnow().isoformat()

    return v2_memo, changes
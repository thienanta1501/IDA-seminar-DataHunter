def removeUnnecessaryFieldFromDict(data: dict, no_need_fields: list[str]) -> dict:
    """Remove unnecessary fields from a dictionary."""
    for field in no_need_fields:
        if field in data:
            del data[field]
    return data
def check_permission(role: str, sql: str) -> bool:
    if role == "admin":
        return True

    # basic restriction
    if sql.lower().startswith(("delete", "update", "insert")):
        return False

    return True
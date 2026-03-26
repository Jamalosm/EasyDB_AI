from app.core.database import cursor, conn
from app.services.ai_service import generate_response, auto_fix_sql, extract_name


# ✅ validation
def validate_prompt(prompt: str):
    prompt = prompt.lower()

    if "add user" in prompt:
        if "age" not in prompt:
            return "Age is required to add user."

    return None


def execute_query(prompt: str):

    # 🔍 validation first
    error = validate_prompt(prompt)
    if error:
        return {"error": error}

    output, mode = generate_response(prompt)

    # 💬 chat mode
    if mode == "chat":
        return {"message": output}

    sql = output.lower()

    # ❌ AI error
    if "error" in sql:
        return {"error": output}

    try:
        print("Generated SQL:", output)

        cursor.execute(output)
        conn.commit()

        rows = cursor.rowcount

        # 📊 SELECT
        if sql.startswith("select"):
            data = cursor.fetchall()
            return {"type": "select", "data": data}

        # ➕ INSERT
        elif sql.startswith("insert"):
            if rows == 0:
                return {"error": "Insert failed."}

            name = extract_name(prompt)
            return {
                "type": "message",
                "message": f"User {name} added successfully."
            }

        # ✏️ UPDATE
        elif sql.startswith("update"):
            if rows == 0:
                return {"error": "No matching user found to update."}

            return {
                "type": "message",
                "message": "User updated successfully."
            }

        # ❌ DELETE
        elif sql.startswith("delete"):
            if rows == 0:
                return {"error": "User not found."}

            name = extract_name(prompt)
            return {
                "type": "message",
                "message": f"User {name} deleted successfully."
            }

        return {"message": "Operation completed successfully."}

    except Exception as e:

        # 🔁 auto fix
        try:
            fixed_sql = auto_fix_sql(prompt, output, str(e))
            cursor.execute(fixed_sql)
            conn.commit()
            return {"message": "Fixed and executed successfully."}
        except:
            return {"error": str(e)}
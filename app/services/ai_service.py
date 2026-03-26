import requests
import re
from app.core.config import OLLAMA_URL, MODEL_NAME


# 🔍 detect DB query
def is_db_query(prompt: str) -> bool:
    keywords = ["add", "insert", "delete", "update", "show", "list", "get"]
    return any(k in prompt.lower() for k in keywords)


# ✅ main router
def generate_response(prompt: str):
    if is_db_query(prompt):
        sql = generate_sql(prompt)
        return sql, "sql"
    else:
        chat = generate_chat(prompt)
        return chat, "chat"


# 🧠 SQL generator
def generate_sql(prompt: str):
    full_prompt = f"""
You are an expert SQL generator.

STRICT RULES:
- Output ONLY SQL
- NO explanation
- NO markdown
- If input incomplete return: SELECT 'ERROR: Missing fields';

SCHEMA:
users(id, name, age)

User: {prompt}
SQL:
"""

    res = requests.post(OLLAMA_URL, json={
        "model": MODEL_NAME,
        "prompt": full_prompt,
        "stream": False
    }).json()

    sql = res.get("response", "").strip().replace("```", "")
    return sql


# 💬 chat mode
def generate_chat(prompt: str):
    res = requests.post(OLLAMA_URL, json={
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }).json()

    return res.get("response", "").strip()


# 🔧 FIX SQL
def auto_fix_sql(prompt, bad_sql, error):
    fix_prompt = f"""
Fix this SQL error.

ERROR: {error}
BAD SQL: {bad_sql}

Return ONLY SQL.
"""
    return generate_sql(fix_prompt)


# 🔍 extract name
def extract_name(prompt: str):
    match = re.search(r"user\s+(\w+)", prompt.lower())
    return match.group(1) if match else ""
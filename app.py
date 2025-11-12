# app.py
import streamlit as st
import speech_recognition as sr
from gemini_client import generate_sql, init_genai
from db_utils import (
    get_schema_snippet,
    detect_sql_type,
    is_safe_select,
    run_select,
    execute_sql,
    ensure_sample_db,
    ensure_hospital_db
)

# ===== CONFIGURATION =====
DB_URL = "sqlite:///sample.db"
GEMINI_MODEL = "models/gemini-2.5-flash"
MAX_TOKENS = 512
# =========================

# ----- Initialize -----
ensure_sample_db()
ensure_hospital_db()

st.set_page_config(page_title="Voice2SQL (Gemini)", layout="wide")
st.title("🎙️ Voice2SQL — Gemini 2.5 with Auto Table Creation 🧠")

try:
    init_genai()
    st.success("✅ Gemini initialized successfully.")
except Exception as e:
    st.error(f"Gemini init failed: {e}")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    st.write("**Database:**", DB_URL)
    st.write("**Model:**", GEMINI_MODEL)

# Show schema
st.subheader("📊 Current Database Schema")
schema_snippet = get_schema_snippet(DB_URL)
st.code(schema_snippet)

# Input mode
mode = st.radio("Choose Input Mode", ["📝 Text", "🎤 Voice"])

user_request = ""
if mode == "📝 Text":
    user_request = st.text_area("Enter your natural language request:", height=100)
else:
    st.info("Click 'Record' and speak your request.")
    if st.button("🎙️ Record"):
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                st.info("Listening... please speak clearly.")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
                user_request = recognizer.recognize_google(audio)
                st.success(f"You said: {user_request}")
        except Exception as e:
            st.error(f"Voice error: {e}")
            user_request = ""

# Generate SQL
if user_request and st.button("🚀 Generate SQL"):
    prompt = f"""
You are an expert SQL assistant.

DATABASE SCHEMA:
{schema_snippet}

USER REQUEST:
{user_request}

INSTRUCTIONS:
- Generate ONE valid SQL statement.
- If the user wants a new table or to add data, output a proper CREATE TABLE or INSERT statement.
- For queries, generate a SELECT.
- Use only valid SQLite syntax.
- Do not add explanations.
- End with a semicolon.
    """

    try:
        sql_query = generate_sql(prompt, model=GEMINI_MODEL, max_output_tokens=MAX_TOKENS)
    except Exception as e:
        st.error(f"Gemini error: {e}")
        sql_query = ""

    if sql_query:
        st.subheader("🧩 Generated SQL")
        st.code(sql_query, language="sql")

        sql_type = detect_sql_type(sql_query)
        st.write(f"🧠 Detected SQL Type: **{sql_type}**")

        # Handle SQL execution
        try:
            if sql_type == "SELECT":
                if is_safe_select(sql_query):
                    rows = run_select(DB_URL, sql_query)
                    st.success("✅ Query executed successfully.")
                    st.dataframe(rows if rows else [])
                else:
                    st.error("❌ Unsafe SELECT blocked.")
            elif sql_type in ["CREATE", "INSERT", "UPDATE", "DELETE"]:
                execute_sql(DB_URL, sql_query)
                st.success(f"✅ {sql_type} executed successfully.")
                st.info("🔁 Schema updated below:")
                schema_snippet = get_schema_snippet(DB_URL)
                st.code(schema_snippet)
            else:
                st.warning("⚠️ Unrecognized SQL type. Please review manually.")
        except Exception as e:
            st.error(f"SQL Execution Error: {e}")

import re
import google.generativeai as genai

# ✅ Hardcoded Gemini API key (replace with your own)
GEMINI_API_KEY = "AIzaSyA1-xnP5IBS1Socx8lMFiFubkGlCNoNdO4"

# ✅ Use stable model from your account
GEMINI_MODEL = "models/gemini-2.5-flash"

def init_genai():
    """Initialize Gemini configuration."""
    genai.configure(api_key=GEMINI_API_KEY)


def clean_output(text: str) -> str:
    """
    Clean Gemini output to extract pure SQL safely.
    Handles markdown fences, commentary, and empty responses.
    """
    if not text:
        return ""

    # Remove markdown or code fences
    text = text.strip()
    text = re.sub(r"^```(sql|SQL)?", "", text)
    text = re.sub(r"```$", "", text)
    text = text.replace("```", "").strip()

    # Look for first SQL keyword
    match = re.search(r"\b(select|create|insert|update|delete|drop|alter)\b", text.lower())

    if match:
        text = text[match.start():].strip()
    else:
        # No SQL keyword found — return text safely
        return text.strip()

    # Remove any trailing explanations after semicolon
    semicolon_index = text.find(";")
    if semicolon_index != -1:
        text = text[:semicolon_index + 1]

    return text.strip()


def generate_sql(prompt, model=GEMINI_MODEL, max_output_tokens=256, temperature=0.0):
    """
    Generate SQL query using Gemini with safe cleaning and error handling.
    """
    try:
        model_instance = genai.GenerativeModel(model)
        response = model_instance.generate_content(prompt)
        sql = (response.text or "").strip()
        return clean_output(sql)
    except Exception as e:
        print(f"[ERROR] Gemini generation failed: {e}")
        return ""

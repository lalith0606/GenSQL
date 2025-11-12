# 🧠 GenSQL — Gemini-Powered Natural Language to SQL Query Generator

GenSQL is an AI-powered web application that converts **natural language (text or voice)** into **executable SQL queries** using **Google Gemini 2.5**.  
It enables users to *talk to databases conversationally* — automatically generating, validating, and executing queries on a live database through an intuitive Streamlit interface.

---

## 🚀 Features

- 🎙️ **Voice & Text Input** — Converts spoken or written requests into SQL queries.
- 🧩 **Gemini 2.5 Integration** — Uses Google’s cutting-edge GenAI model for natural language understanding.
- 🗃️ **Automatic SQL Generation** — Supports `SELECT`, `CREATE`, and `INSERT` statements.
- 🧱 **Auto Table Creation** — Dynamically builds new tables based on user input.
- 🛡️ **SQL Safety Validation** — Blocks destructive queries (`DROP`, `ALTER`, `TRUNCATE`).
- 💾 **Real-Time Execution** — Runs queries instantly and displays results in Streamlit.
- 🧠 **Schema Awareness** — Keeps Gemini grounded with your live database schema.
- 🌐 **Streamlit Frontend** — Simple, responsive, and interactive web UI.

---

## 🧰 Tech Stack

| Component | Technology |
|------------|-------------|
| **Frontend** | Streamlit |
| **Backend** | Python 3.x |
| **AI Model** | Google Gemini 2.5 Flash |
| **Database** | SQLite |
| **Voice Input** | SoundDevice / SpeechRecognition |
| **Environment** | Virtualenv (venv) |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/GenSQL.git
cd GenSQL

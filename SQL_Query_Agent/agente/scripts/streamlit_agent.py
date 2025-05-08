import streamlit as st
import mysql.connector
import openai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- STREAMLIT PAGE CONFIGURATION ---
st.set_page_config(page_title="Brainiac Query Assistant", page_icon="🏛️")
st.title("🏛️ Brainiac Query Assistant")

# --- SIDEBAR CONFIGURATION (CREDENTIALS INPUT) ---
st.sidebar.header("🔐 Settings")
openai_api_key = st.sidebar.text_input("🔑 OpenAI API Key", type="password")
mysql_host = st.sidebar.text_input("🏠 MySQL Host", value="localhost")
mysql_user = st.sidebar.text_input("👤 MySQL User", value="root")
mysql_password = st.sidebar.text_input("🔒 MySQL Password", type="password")
mysql_db = st.sidebar.text_input("📂 Database Name", value="Your_database")

# --- MAIN AREA: USER INTERACTION AND QUESTION INPUT ---
if "question" not in st.session_state:
    st.session_state.question = ""

st.markdown("### 💬 Suggested Questions")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📋 Clients"):
        st.session_state.question = "Show me all clients"
with col2:
    if st.button("💸 Payments"):
        st.session_state.question = "Show me all payments"
with col3:
    if st.button("🏠 Addresses"):
        st.session_state.question = "Show me all addresses"
with col4:
    if st.button("📈 Transactions"):
        st.session_state.question = "Show me all transactions"

st.markdown("### ✍️ Custom Question")
question = st.text_input("Enter your question in natural language:",
                         value=st.session_state.question,
                         key="input_question")

# --- HELPER FUNCTIONS ---
def get_table_structures():
    """Retrieve the structure of all tables in the MySQL database."""
    try:
        conn = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_db
        )
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()

        columns = {}
        for table in tables:
            cursor.execute(f"DESCRIBE {table[0]};")
            table_columns = cursor.fetchall()
            columns[table[0]] = [column[0] for column in table_columns]

        cursor.close()
        conn.close()
        return columns
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return {}

def load_prompt():
    """Load prompt configuration from the JSON file."""
    try:
        with open("protocolos/prompt.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading prompt context: {e}")
        return {}

def generate_sql_query(question, columns):
    """Generate SQL query using OpenAI based on user question and DB schema."""
    openai.api_key = openai_api_key
    prompt = load_prompt()

    additional_instructions = "\n- " + "\n- ".join(prompt.get("instrucoes_sql", []))

    context = f"""
System: {prompt.get('system_name', 'Unknown')}
Model Role: {prompt.get('model_role', '')}
User Profile: {prompt.get('user_profile', {})}
Restrictions: {'; '.join(prompt.get('restricoes', []))}

Additional instructions for generating correct SQL:
{additional_instructions}

Database:
{json.dumps(columns, indent=2, ensure_ascii=False)}

User Question:
{question}

Generate a corresponding SQL query:
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt.get('model_role', "You are an SQL assistant.")},
                {"role": "user", "content": context}
            ],
            max_tokens=300,
            temperature=0
        )
        query = response.choices[0].message.content.strip()
        return query.replace("```sql", "").replace("```", "").strip()
    except Exception as e:
        st.error(f"Error generating SQL query: {e}")
        return ""

def execute_query(query):
    """Execute an SQL query and return columns and results."""
    if not query:
        st.warning("\u26a0\ufe0f The SQL query is empty. Check your question or the context.")
        return [], []

    try:
        conn = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_db
        )
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()
        return columns, results
    except Exception as e:
        st.error(f"Error executing SQL query: {e}")
        return [], []

def save_history(question, query, result):
    """Save the query and result into the interaction history table."""
    try:
        conn = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_db
        )
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historico_interacoes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                pergunta TEXT,
                query_gerada TEXT,
                resultado LONGTEXT,
                feedback VARCHAR(10),
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cursor.execute("""
            INSERT INTO historico_interacoes (pergunta, query_gerada, resultado)
            VALUES (%s, %s, %s)
        """, (question, query, str(result)))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Error saving history: {e}")

def save_feedback(question, feedback):
    """Save feedback to the latest corresponding query."""
    try:
        conn = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_db
        )
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE historico_interacoes
            SET feedback = %s
            WHERE pergunta = %s
            ORDER BY data DESC LIMIT 1;
        """, (feedback, question))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        st.error(f"Error saving feedback: {e}")

# --- MAIN EXECUTION LOGIC ---
if question:
    structure = get_table_structures()
    if structure:
        query = generate_sql_query(question, structure)

        show_sql = st.toggle("👁️ Show SQL query")
        if show_sql:
            st.code(query, language="sql")

        columns, results = execute_query(query)

        if results:
            st.success("✅ Query executed successfully!")
            st.dataframe([dict(zip(columns, row)) for row in results])
            save_history(question, query, results)
        else:
            st.warning("No results found.")

        feedback = st.radio("Was this answer helpful?", ("👍 Yes", "👎 No"), key="feedback")
        save_feedback(question, feedback)

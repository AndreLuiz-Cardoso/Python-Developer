

# 🧠 Brainiac Query Assistant

Turn natural language into powerful SQL queries using AI.  
A streamlined assistant for analysts and business professionals, built with OpenAI GPT-4, MySQL, and Streamlit.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-ff69b4)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-orange)
![MySQL](https://img.shields.io/badge/Database-MySQL-blue)
![AI Copilot](https://img.shields.io/badge/AI-Copilot-brightgreen)

---

## 📌 Overview

**Brainiac Query Assistant** is an intelligent SQL copilot that allows users to ask questions in natural language and receive optimized SQL queries in return.

Whether you're a data analyst, product manager, or BI specialist, this tool lets you:
- Query a relational MySQL database without writing SQL
- Understand complex schemas automatically
- Get fast insights using language you already know

This project was built as part of a practical AI course and is structured to simulate real-world banking data and queries.

---

## 🏗️ Project Architecture

![Architecture](img/arquitetura.png)

---

## ⚙️ Features

- 🔍 Understands natural language and maps to SQL
- 🗃️ Connects to a MySQL relational database
- 🧠 Uses OpenAI's GPT-4 for query generation
- 📊 Displays query results instantly
- 🧾 Keeps history of interactions and feedback
- ❌ Prevents dangerous commands like `DROP`, `DELETE`, and `INSERT`

---

## 🧠 Prompt Capabilities

The underlying prompt used by the AI agent includes instructions to support:

- Conditional logic with `CASE WHEN`
- Filtering groups with `HAVING`
- Combining results with `UNION` / `UNION ALL`
- Using subqueries in `SELECT`, `WHERE`, or `FROM`
- Date operations using `DATE_FORMAT`, `DATEDIFF`, `NOW()`, etc.

---

## 📂 Folder Structure

```
├── agente/
│   ├── scripts/
│   │   ├── streamlit_agent.py    # Main GUI app
│   │   └── terminal_agent.py     # CLI version
│
├── banco_de_dados/
│   ├── scripts/
│   │   └── create_table.py       # Populates DB with fake data
│   └── datasets/                 # Generated CSV exports
│
├── protocolos/
│   └── prompt.json               # Prompt config for AI agent
│
├── .env                          # Environment config (API key, DB access)
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up your environment

Create a `.env` file in the root directory with the following:

```
OPENAI_API_KEY=your_openai_key
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_DB=dioBank
MYSQL_PORT=3306
```

### 3. Populate the database

```bash
python banco_de_dados/scripts/create_table.py
```

This script creates and fills the MySQL database with realistic dummy data using Faker.

### 4. Launch the app

```bash
streamlit run agente/scripts/streamlit_agent.py
```

Or use the terminal version:

```bash
python agente/scripts/terminal_agent.py
```

## 🖼️ Interface Previews & Examples

### 🔐 App Home with Settings Panel
> Configure your API and database connection through a secure sidebar.
![Home](assets/01-Home.png)

---

### 🧾 Basic Natural Language Query
> Example: **"Show all names with letter A"**  
> Returns filtered SQL using `LIKE`.
![Consulta 1](assets/02-Name-A.png)

---

### 🧠 Advanced Query with JOIN and Aggregation
> Example: **"Top 5 clients who made the largest deposits"**  
> Demonstrates `JOIN`, `GROUP BY`, `SUM`, and `LIMIT`.
![Consulta 2](assets/03-TopDeposits.png)

---

### 👁️ SQL Visibility Option
> Toggle to inspect the generated SQL query.
![Consulta 3](assets/04-ShowSQLToggle.png)

---

### 🧬 Architecture
> Diagram showing how the system integrates OpenAI, Streamlit, and MySQL.
![Architecture](assets/Architecture.png)

---

## 💬 Sample Questions

- "Show me the clients with the highest number of transactions"
- "What is the total payment value by city?"
- "List all withdrawals made in the last 30 days"
- "Which client had the largest transaction this year?"

---

## 🛡️ Safety & Restrictions

- No support for `INSERT`, `DELETE`, `DROP DATABASE`
- `UPDATE` only if there's a clear `WHERE` clause
- Responses return only SQL (no extra explanation)
- Prompt is structured for context, compliance, and reuse

---

## 🛠️ Built With

- [Python 3.10+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [OpenAI API](https://platform.openai.com/)
- [MySQL](https://www.mysql.com/)
- [Faker](https://faker.readthedocs.io/en/master/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## 💼 Ideal For

- Data Analysts and BI professionals
- Developers building AI copilots
- Teams modernizing their SQL workflows
- Portfolio demonstrations and technical case studies

---

## 📈 Status

> ✅ Completed and ready to demo.  
> 🔒 Safe for testing on local or mock databases.  
> 🧠 Designed for further extensions (PostgreSQL, dashboards, visualizations, etc).

---

## ✨ Author

Created by **André Luiz Cardoso** as part of an AI agent development challenge with real-world applications in SQL analysis.

---

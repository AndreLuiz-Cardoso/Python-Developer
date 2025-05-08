import openai
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Function to call the OpenAI API and generate the SQL query
def generate_sql_query(question: str, columns: dict) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")  # Your OpenAI API key
    
    # Create the prompt for OpenAI, including the database columns
    prompt = f"""
You are an SQL assistant operating for a fictional database called Dio Bank.
You must generate queries based on the following database structure:
{columns}

Question: {question}
SQL Response:
"""
    
    # Using the latest OpenAI Chat API
    response = openai.ChatCompletion.create(
        model="gpt-4.1",  # Use the most recent model
        messages=[
            {"role": "system", "content": "You are an SQL assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0
    )

    # Extract the generated response
    query = response['choices'][0]['message']['content'].strip()
    
    # Remove any code formatting (```sql or ``` at the end)
    query = query.replace("```sql", "").replace("```", "").strip()
    
    return query

# Function to retrieve the table and column structures from the database
def get_table_structures() -> dict:
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DB")
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
        return f"Error retrieving table structure: {e}"

# Simple function to execute an SQL query
def execute_query(query: str) -> str:
    """Executes an actual SQL query in MySQL and returns the results."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", "admin123"),
            database=os.getenv("MYSQL_DB", "dioBank")
        )
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()  # Retrieves all results from a previously executed query
        cursor.close()
        conn.close()

        return results
    except:
        print('Error')

# Example interaction with the agent
question = input("Ask your question to our agent: ")

# Generate the query based on the columns
generated_query = generate_sql_query(question, get_table_structures())

print(f"\nGENERATED QUERY: `{generated_query}`")
print(f"\nRESULT")

# Execute the query on the database
print(execute_query(generated_query))
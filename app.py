from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure GenAI Key
api_key = os.getenv("GOOGLE_API_KEY", "your api key here")
genai.configure(api_key=api_key)

# Function to load Google Gemini Model and convert natural language question to SQL query
def get_sql_from_natural_language(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    # Use AI to convert the natural language question to SQL
    response = model.generate_content([prompt[0], question])
    sql_query = response.text.strip()

    # Clean the SQL query (remove backticks or unnecessary formatting)
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
    
    return sql_query

# Function to execute SQL query and fetch results from the database
def execute_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
    except sqlite3.Error as e:
        return str(e)
    conn.commit()
    conn.close()
    return rows

# Function to convert SQL query results back to natural language
def convert_results_to_natural_language(sql_results, question):
    if not sql_results:
        return f"Sorry, no results found for the query related to '{question}'."
    
    if isinstance(sql_results, str):  # If there's an error message
        return f"An error occurred: {sql_results}"
    
    # Generate a human-readable response from SQL result
    answer = "Here are the results: \n"
    for row in sql_results:
        answer += ', '.join(map(str, row)) + "\n"
    return answer

# Define Your Prompt for guiding the AI on SQL conversions
prompt = [
    """
   You are an expert in converting English questions to SQL query! The SQL database has the name university and has the following tables - STUDENT, EMPLOYEE, and FACULTY.

Each table has the following columns:

STUDENT: STUDENT_ID, NAME, CLASS, SECTION, MARKS, FACULTY_ID
EMPLOYEE: EMPLOYEE_ID, NAME, POSITION, SALARY, FACULTY_ID
FACULTY: FACULTY_ID, NAME, DEPARTMENT, SALARY

For example:
Example 1 - How many students are present? The SQL command will be something like this: SELECT COUNT(*) FROM STUDENT;

Example 2 - Tell me all the employees who work in the Biology department? The SQL command will be something like this: SELECT * FROM EMPLOYEE WHERE FACULTY_ID = (SELECT FACULTY_ID FROM FACULTY WHERE DEPARTMENT = 'Biology');

Example 3 - How many faculty members have a salary greater than 80,000? The SQL command will be something like this: SELECT COUNT(*) FROM FACULTY WHERE SALARY > 80000;

Make sure to provide the corresponding SQL queries for any English questions related to the STUDENT, EMPLOYEE, or FACULTY tables!
    """
]

# Streamlit App UI
st.title("University Database Query Tool")
st.write("Ask a question about students, employees, or faculty in natural language.")

# Get user input in natural language
question = st.text_input("Enter your question")

if question:
    # Convert natural language question to SQL
    sql_query = get_sql_from_natural_language(question, prompt)
    st.write(f"Generated SQL Query: {sql_query}")

    # Execute SQL query
    sql_results = execute_sql_query(sql_query, "university.db")
    
    # Convert SQL results to natural language
    response = convert_results_to_natural_language(sql_results, question)
    
    # Display the natural language response
    st.write(response)

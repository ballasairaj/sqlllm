import sqlite3

# Connect to SQLite database
connection = sqlite3.connect("university.db")

# Enable foreign key constraint support in SQLite
connection.execute("PRAGMA foreign_keys = ON")

# Create a cursor object
cursor = connection.cursor()

# Create FACULTY table with FACULTY_ID as primary key and SALARY column
faculty_table = """
CREATE TABLE IF NOT EXISTS FACULTY (
    FACULTY_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME VARCHAR(25),
    DEPARTMENT VARCHAR(25),
    SALARY INT
);
"""
cursor.execute(faculty_table)

# Create EMPLOYEE table with EMPLOYEE_ID as primary key and FACULTY_ID as a foreign key
employee_table = """
CREATE TABLE IF NOT EXISTS EMPLOYEE (
    EMPLOYEE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME VARCHAR(25),
    POSITION VARCHAR(25),
    SALARY INT,
    FACULTY_ID INTEGER,
    FOREIGN KEY (FACULTY_ID) REFERENCES FACULTY(FACULTY_ID)
);
"""
cursor.execute(employee_table)

# Create STUDENT table with STUDENT_ID as primary key and FACULTY_ID as a foreign key
student_table = """
CREATE TABLE IF NOT EXISTS STUDENT (
    STUDENT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT,
    FACULTY_ID INTEGER,
    FOREIGN KEY (FACULTY_ID) REFERENCES FACULTY(FACULTY_ID)
);
"""
cursor.execute(student_table)

# Insert records into FACULTY table with SALARY
cursor.execute("INSERT INTO FACULTY (NAME, DEPARTMENT, SALARY) VALUES ('Dr. Smith', 'Computer Science', 90000)")
cursor.execute("INSERT INTO FACULTY (NAME, DEPARTMENT, SALARY) VALUES ('Dr. Brown', 'Mathematics', 85000)")
cursor.execute("INSERT INTO FACULTY (NAME, DEPARTMENT, SALARY) VALUES ('Dr. Johnson', 'Physics', 87000)")
cursor.execute("INSERT INTO FACULTY (NAME, DEPARTMENT, SALARY) VALUES ('Dr. Adams', 'Biology', 82000)")
cursor.execute("INSERT INTO FACULTY (NAME, DEPARTMENT, SALARY) VALUES ('Dr. Turner', 'Chemistry', 83000)")

# Insert records into EMPLOYEE table, linking to FACULTY
cursor.execute("INSERT INTO EMPLOYEE (NAME, POSITION, SALARY, FACULTY_ID) VALUES ('Alice', 'Admin Assistant', 35000, 1)")
cursor.execute("INSERT INTO EMPLOYEE (NAME, POSITION, SALARY, FACULTY_ID) VALUES ('Bob', 'Researcher', 50000, 2)")
cursor.execute("INSERT INTO EMPLOYEE (NAME, POSITION, SALARY, FACULTY_ID) VALUES ('Charlie', 'Lab Technician', 45000, 3)")
cursor.execute("INSERT INTO EMPLOYEE (NAME, POSITION, SALARY, FACULTY_ID) VALUES ('David', 'Office Manager', 40000, 4)")
cursor.execute("INSERT INTO EMPLOYEE (NAME, POSITION, SALARY, FACULTY_ID) VALUES ('Eve', 'Coordinator', 38000, 5)")

# Insert records into STUDENT table, linking to FACULTY
cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS, FACULTY_ID) VALUES ('John Doe', 'Data Science', 'A', 85, 1)")
cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS, FACULTY_ID) VALUES ('Jane Roe', 'Mathematics', 'B', 90, 2)")
cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS, FACULTY_ID) VALUES ('Richard Roe', 'Physics', 'C', 75, 3)")
cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS, FACULTY_ID) VALUES ('Sara Lee', 'Biology', 'D', 80, 4)")
cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS, FACULTY_ID) VALUES ('Tom White', 'Chemistry', 'E', 95, 5)")

# Commit the changes
connection.commit()

# Display the records from each table

# Display records from FACULTY table
print("Records from FACULTY table:")
faculty_data = cursor.execute("SELECT * FROM FACULTY")
for row in faculty_data:
    print(row)

# Display records from EMPLOYEE table
print("\nRecords from EMPLOYEE table:")
employee_data = cursor.execute("SELECT * FROM EMPLOYEE")
for row in employee_data:
    print(row)

# Display records from STUDENT table
print("\nRecords from STUDENT table:")
student_data = cursor.execute("SELECT * FROM STUDENT")
for row in student_data:
    print(row)

# Close the connection
connection.close()

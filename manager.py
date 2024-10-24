import streamlit as st
import sqlite3
from PIL import Image
from io import BytesIO
from gemini_solution import get_solution_from_gemini  # Your AI function


def manager_page():
    st.header("Manager Dashboard")

    # Show two options: Show Current Issues and Show Accepted Issues
    option = st.radio("Select an option", ["Show Current Issues", "Show Accepted Issues"])

    if option == "Show Current Issues":
        show_current_issues()
    elif option == "Show Accepted Issues":
        show_accepted_issues()

# Function to display current issues
def show_current_issues():
    st.subheader("Current Issues")

    # Fetch complaints from the database, including the employee who raised them
    issues = get_issues()

    # Check if there are any issues to display
    if issues:
        for issue_id, issue_type, image, description, raised_by in issues:  # Include raised_by in the loop
            with st.container():
                st.subheader(f"Issue Type: {issue_type}")
                st.image(Image.open(BytesIO(image)), caption="Uploaded Image", use_column_width=True)
                st.write(f"Description: {description}")
                st.write(f"**Raised by:** {raised_by}")  # Display which user raised this issue

                # Clear and Accept Issue Buttons
                col1, col2 = st.columns(2)

                with col1:
                    clear_button = st.button(f"Clear Issue {issue_id}", key=f"clear_{issue_id}")

                with col2:
                    accept_button = st.button(f"Accept Issue {issue_id}", key=f"accept_{issue_id}")

                # If the clear button is clicked, clear the issue
                if clear_button:
                    clear_issue(issue_id)
                    st.success(f"Issue {issue_id} cleared!")
                    st.rerun()

                # If the accept button is clicked, move the issue to the accepted_issues table
                if accept_button:
                    accept_issue(issue_id, issue_type, image, description, raised_by)
                    st.success(f"Issue {issue_id} accepted!")
                    st.rerun()

                # Show AI suggestion only if the issue hasn't been cleared
                with st.spinner("AI Analyzing the issue, please wait..."):
                    solution = get_solution_from_gemini(image)  # Call AI model

                if solution:
                    st.write(f"AI Suggested Solution: {solution}")
                else:
                    st.write("Failed to get AI suggested solution.")
    else:
        st.write("No issues have been raised yet.")

# Function to display accepted issues
def show_accepted_issues():
    st.subheader("Accepted Issues")

    # Fetch accepted issues from the database
    issues = get_accepted_issues()

    # Check if there are any accepted issues to display
    if issues:
        for issue_id, issue_type, image, description, raised_by in issues:
            with st.container():
                st.subheader(f"Issue Type: {issue_type}")
                st.image(Image.open(BytesIO(image)), caption="Uploaded Image", use_column_width=True)
                st.write(f"Description: {description}")
                st.write(f"**Raised by:** {raised_by}")  # Display which user raised this issue

    else:
        st.write("No accepted issues yet.")

# Function to fetch issues from the database, including the employee who raised them
def get_issues():
    conn = sqlite3.connect('auditing.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, issue_type, image, description, raised_by FROM issues")  # Fetch raised_by as well
    return cursor.fetchall()

# Function to fetch accepted issues from the database
def get_accepted_issues():
    conn = sqlite3.connect('auditing.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, issue_type, image, description, raised_by FROM accepted_issues")  # Fetch accepted issues
    return cursor.fetchall()

# Function to clear issues from the database
def clear_issue(issue_id):
    conn = sqlite3.connect('auditing.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM issues WHERE id = ?", (issue_id,))
    conn.commit()
    conn.close()

# Function to move an issue to the accepted_issues table and remove it from the issues table
def accept_issue(issue_id, issue_type, image, description, raised_by):
    conn = sqlite3.connect('auditing.db')
    cursor = conn.cursor()

    # Insert the issue into the accepted_issues table without specifying the ID (it will auto-increment)
    cursor.execute('''
        INSERT INTO accepted_issues (issue_type, image, description, raised_by)
        VALUES (?, ?, ?, ?)
    ''', (issue_type, image, description, raised_by))

    # Delete the issue from the issues table
    cursor.execute("DELETE FROM issues WHERE id = ?", (issue_id,))
    
    conn.commit()
    conn.close()

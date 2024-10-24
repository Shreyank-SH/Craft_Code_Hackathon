import streamlit as st
import sqlite3
from PIL import Image
from io import BytesIO
from gemini_solution import get_solution_from_gemini


def manager_page():
    st.header("Manager Dashboard")
    
    option = st.radio("Select an option", ["Show Current Issues", "Show Accepted Issues"])

    if option == "Show Current Issues":
        show_current_issues()
    elif option == "Show Accepted Issues":
        show_accepted_issues()

def show_current_issues():
    st.subheader("Current Issues")

    issues = get_issues()

    if issues:
        for issue_id, issue_type, image, description, raised_by in issues:
            with st.container():
                st.subheader(f"Issue Type: {issue_type}")
                st.image(Image.open(BytesIO(image)), caption="Uploaded Image", use_column_width=True)
                st.write(f"Description: {description}")
                st.write(f"**Raised by:** {raised_by}")

                col1, col2 = st.columns(2)

                with col1:
                    clear_button = st.button(f"Clear Issue {issue_id}", key=f"clear_{issue_id}")

                with col2:
                    accept_button = st.button(f"Accept Issue {issue_id}", key=f"accept_{issue_id}")

                if clear_button:
                    clear_issue(issue_id)
                    st.success(f"Issue {issue_id} cleared!")
                    st.rerun()

                if accept_button:
                    accept_issue(issue_id, issue_type, image, description, raised_by)
                    st.success(f"Issue {issue_id} accepted!")
                    st.rerun()

                with st.spinner("AI Analyzing the issue, please wait..."):
                    solution = get_solution_from_gemini(image)

                if solution:
                    st.write(f"AI Suggested Solution: {solution}")
                else:
                    st.write("Failed to get AI suggested solution.")
    else:
        st.write("No issues have been raised yet.")

def show_accepted_issues():
    st.subheader("Accepted Issues")

    issues = get_accepted_issues()

    if issues:
        for issue_id, issue_type, image, description, raised_by in issues:
            with st.container():
                st.subheader(f"Issue Type: {issue_type}")
                st.image(Image.open(BytesIO(image)), caption="Uploaded Image", use_column_width=True)
                st.write(f"Description: {description}")
                st.write(f"**Raised by:** {raised_by}")

    else:
        st.write("No accepted issues yet.")

def get_issues():
    conn = sqlite3.connect('auditing.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, issue_type, image, description, raised_by FROM issues")
    return cursor.fetchall()

def get_accepted_issues():
    conn = sqlite3.connect('auditing.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, issue_type, image, description, raised_by FROM accepted_issues")
    return cursor.fetchall()

def clear_issue(issue_id):
    conn = sqlite3.connect('auditing.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM issues WHERE id = ?", (issue_id,))
    conn.commit()
    conn.close()

def accept_issue(issue_id, issue_type, image, description, raised_by):
    conn = sqlite3.connect('auditing.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO accepted_issues (issue_type, image, description, raised_by)
        VALUES (?, ?, ?, ?)
    ''', (issue_type, image, description, raised_by))

    cursor.execute("DELETE FROM issues WHERE id = ?", (issue_id,))
    
    conn.commit()
    conn.close()

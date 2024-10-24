import streamlit as st
import sqlite3

def get_employee_points(username):
    conn = sqlite3.connect('auditing.db')
    cursor = conn.cursor()

    cursor.execute("SELECT points FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    
    conn.close()
    if result:
        return result[0]
    else:
        return 0

def employee_page():
    st.markdown(
        """
        <style>
        .dashboard-container {
            display: flex;
            align-items: center;
        }
        .points-bubble {
            display: inline-block;
            padding: 5px 10px;
            background-color: #4CAF50;
            color: white;
            border-radius: 50px;
            font-weight: bold;
            margin-left: 15px;
        }
        .header-inline {
            display: inline-block;
            font-size: 2rem;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True
    )

    st.markdown(f"""
    <div class="dashboard-container">
        <div class="header-inline">Employee Dashboard</div>
        <span class="points-bubble">{get_employee_points(st.session_state.username)} points</span>
    </div>
    """, unsafe_allow_html=True)

    issue_type = st.radio("Select the type of issue:", [
        "Food Related Issues (e.g., Packaging Mistake, Wrong Labeling, Spills or Breakage of Container, etc.)",
        "Issue related to Equipment, Appliances (e.g., Cooking equipment, utensils, etc.)"
    ])

    uploaded_file = st.file_uploader("Upload an image related to the issue", type=["jpg", "jpeg", "png"])

    issue_description = st.text_area("Describe the issue briefly")

    if st.button("Submit Issue"):
        if uploaded_file is not None and issue_description:
            save_issue(issue_type, uploaded_file, issue_description)
            st.success(f"{issue_type} submitted successfully!")
        else:
            st.error("Please upload an image and write a description.")

def save_issue(issue_type, image, description):
    conn = sqlite3.connect('auditing.db')
    cursor = conn.cursor()

    image_bytes = image.read()

    cursor.execute(
        '''INSERT INTO issues (issue_type, image, description, raised_by) VALUES (?, ?, ?, ?)''',
        (issue_type, image_bytes, description, st.session_state.username)
    )

    username = st.session_state.username
    cursor.execute("UPDATE users SET points = points + 10 WHERE username = ?", (username,))

    conn.commit()
    conn.close()

import os
import streamlit as st
from login_system import login_user, signup_user, user_exists
from employee import employee_page
from manager import manager_page

def check_and_setup_db():
    if not os.path.exists('auditing.db'):
        st.info("Setting up the database for the first time...")
        import setup_db

check_and_setup_db()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

def select_role():
    if not st.session_state.logged_in:
        st.subheader("Select Your Role")

        role_options = ["Employee", "Manager"]
        if 'role' not in st.session_state or st.session_state.role == "":
            selected_role = st.selectbox("Choose your role", ["Select a role"] + role_options, key="role_selection")
            if selected_role != "Select a role":
                st.session_state.role = selected_role
                st.rerun()

def change_role():
    st.session_state.role = ""
    st.rerun()

def signout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.rerun()

def main():
    st.title("Quality-Quest: Food Safety Auditing System")

    if 'role' not in st.session_state or st.session_state.role == "":
        select_role()
    else:
        if not st.session_state.logged_in:
            if st.button("Change Role"):
                change_role()

        if not st.session_state.logged_in:
            st.subheader(f"{st.session_state.role} Login")
            option = st.radio("Login or Sign up", ["Login", "Sign Up"])

            if option == "Login":
                login_form(st.session_state.role)
            else:
                signup_form(st.session_state.role)
        else:
            st.success(f"Welcome {st.session_state.username}")
            
            if st.button("Sign Out"):
                signout()
            
            if st.session_state.role == "Manager":
                manager_page()
            elif st.session_state.role == "Employee":
                employee_page()

def login_form(role):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = user[1]
            st.session_state.role = user[3]
            st.success(f"Logged in as {user[1]} ({user[3]})")
            st.rerun()
        else:
            st.error("Invalid username or password")

def signup_form(role):
    username = st.text_input("Choose a username")
    password = st.text_input("Choose a password", type="password")
    confirm_password = st.text_input("Confirm your password", type="password")

    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match")
        elif user_exists(username):
            st.error("Username already exists. Please Login")
        else:
            if signup_user(username, password, role):
                st.success(f"{role} account created successfully! You can now login.")
            else:
                st.error("Error creating account. Try again.")

if __name__ == "__main__":
    main()

import streamlit as st
from database import connect_db, generate_code

st.set_page_config(page_title="Smart Campus Chatbot", layout="wide")

if "user_type" not in st.session_state:
    st.session_state.user_type = None

if "username" not in st.session_state:
    st.session_state.username = None

def logout():
    st.session_state.user_type = None
    st.session_state.username = None
    st.rerun()

st.title("🎓 Smart Campus Chatbot")

menu = st.sidebar.selectbox(
    "Menu",
    ["Home", "School Register", "Student Register", "Login"]
)

# HOME
if menu == "Home":
    st.write("Welcome to Smart Campus Chatbot")

# SCHOOL REGISTER
elif menu == "School Register":
    st.header("School Registration")

    school_name = st.text_input("School Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register School"):
        code = generate_code()

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO schools (school_name, username, password, school_code) VALUES (?, ?, ?, ?)",
            (school_name, username, password, code)
        )

        conn.commit()
        conn.close()

        st.success("Registered Successfully")
        st.info(f"School Code: {code}")

# STUDENT REGISTER
elif menu == "Student Register":
    st.header("Student Registration")

    full_name = st.text_input("Full Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    school_code = st.text_input("School Code")

    if st.button("Register Student"):
        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO students (full_name, username, password, school_code) VALUES (?, ?, ?, ?)",
            (full_name, username, password, school_code)
        )

        conn.commit()
        conn.close()

        st.success("Student Registered Successfully")

# LOGIN
elif menu == "Login":
    st.header("Login")

    role = st.selectbox("Login As", ["School", "Student"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = connect_db()
        cur = conn.cursor()

        if role == "School":
            cur.execute(
                "SELECT * FROM schools WHERE username=? AND password=?",
                (username, password)
            )
            user = cur.fetchone()

            if user:
                st.session_state.user_type = "school"
                st.session_state.username = username
                st.success("School Login Successful")
            else:
                st.error("Invalid Login")

        else:
            cur.execute(
                "SELECT * FROM students WHERE username=? AND password=?",
                (username, password)
            )
            user = cur.fetchone()

            if user:
                st.session_state.user_type = "student"
                st.session_state.username = username
                st.success("Student Login Successful")
            else:
                st.error("Invalid Login")

        conn.close()

# DASHBOARDS
if st.session_state.user_type == "school":
    st.sidebar.success("School Dashboard")
    st.write(f"Welcome School: {st.session_state.username}")
    if st.button("Logout"):
        logout()

elif st.session_state.user_type == "student":
    st.sidebar.success("Student Dashboard")
    st.write(f"Welcome Student: {st.session_state.username}")
    if st.button("Logout"):
        logout()
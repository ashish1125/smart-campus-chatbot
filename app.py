import streamlit as st
from database import connect_db, generate_code

st.set_page_config(page_title="Smart Campus Chatbot", layout="wide")

st.title("🎓 Smart Campus Chatbot")
st.subheader("AI Assistant for Schools & Students")

menu = st.sidebar.selectbox(
    "Choose Option",
    ["Home", "School Register", "Student Register"]
)

# HOME
if menu == "Home":
    st.write("Welcome to Smart Campus Chatbot")
    st.write("Schools upload academic data, students ask questions.")

# SCHOOL REGISTER
elif menu == "School Register":
    st.header("School Registration")

    school_name = st.text_input("School / College Name")
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

        st.success(f"School Registered Successfully!")
        st.info(f"Your School Code: {code}")

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

        st.success("Student Registered Successfully!")
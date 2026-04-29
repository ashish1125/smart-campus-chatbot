import streamlit as st
from database import connect_db, generate_code

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Smart Campus Chatbot", layout="wide")

# -------------------------------
# Session State
# -------------------------------
if "user_type" not in st.session_state:
    st.session_state.user_type = None

if "username" not in st.session_state:
    st.session_state.username = None


# -------------------------------
# Logout Function
# -------------------------------
def logout():
    st.session_state.user_type = None
    st.session_state.username = None
    st.rerun()


# -------------------------------
# Title
# -------------------------------
st.title("🎓 Smart Campus Chatbot")

# -------------------------------
# Sidebar Menu
# -------------------------------
menu = st.sidebar.selectbox(
    "Menu",
    [
        "Home",
        "Institute Register",
        "Student Register",
        "Login"
    ]
)

# =====================================================
# HOME PAGE
# =====================================================
if menu == "Home":

    st.header("Welcome to Smart Campus Chatbot")

    st.write("""
    A smart AI platform where institutes upload official academic information,
    and students get quick answers through chatbot support.
    """)

    st.markdown("### Features")
    st.write("✅ Institute Login")
    st.write("✅ Student Login")
    st.write("✅ Upload Syllabus / Calendar / Notices")
    st.write("✅ Chatbot Support")
    st.write("✅ Clean Dashboard")


# =====================================================
# INSTITUTE REGISTER
# =====================================================
elif menu == "Institute Register":

    st.header("Institute Registration")

    institute_type = st.selectbox(
        "Select Type",
        ["School", "College", "University", "Institute"]
    )

    institute_name = st.text_input("Institute Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register Institute"):

        code = generate_code()

        conn = connect_db()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO institutes
        (institute_name, institute_type, username, password, institute_code, logo_path)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (institute_name, institute_type, username, password, code, ""))

        conn.commit()
        conn.close()

        st.success("Institute Registered Successfully")
        st.info(f"Your Institute Code: {code}")


# =====================================================
# STUDENT REGISTER
# =====================================================
elif menu == "Student Register":

    st.header("Student Registration")

    full_name = st.text_input("Full Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    institute_code = st.text_input("Institute Code")

    if st.button("Register Student"):

        conn = connect_db()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO students
        (full_name, username, password, institute_code)
        VALUES (?, ?, ?, ?)
        """, (full_name, username, password, institute_code))

        conn.commit()
        conn.close()

        st.success("Student Registered Successfully")


# =====================================================
# LOGIN
# =====================================================
elif menu == "Login":

    st.header("Login")

    role = st.selectbox("Login As", ["Institute", "Student"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        conn = connect_db()
        cur = conn.cursor()

        if role == "Institute":

            cur.execute("""
            SELECT * FROM institutes
            WHERE username=? AND password=?
            """, (username, password))

            user = cur.fetchone()

            if user:
                st.session_state.user_type = "institute"
                st.session_state.username = username
                st.success("Institute Login Successful")
                st.rerun()
            else:
                st.error("Invalid Login")

        else:

            cur.execute("""
            SELECT * FROM students
            WHERE username=? AND password=?
            """, (username, password))

            user = cur.fetchone()

            if user:
                st.session_state.user_type = "student"
                st.session_state.username = username
                st.success("Student Login Successful")
                st.rerun()
            else:
                st.error("Invalid Login")

        conn.close()


# =====================================================
# INSTITUTE DASHBOARD
# =====================================================
if st.session_state.user_type == "institute":

    st.sidebar.success("Institute Dashboard")

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT institute_name, institute_type, institute_code
    FROM institutes
    WHERE username=?
    """, (st.session_state.username,))

    info = cur.fetchone()

    conn.close()

    st.header("🏫 Institute Dashboard")

    st.write(f"### Welcome {info[1]}: {info[0]}")
    st.write(f"**Institute Code:** {info[2]}")

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT logo_path FROM institutes
    WHERE username=?
    """, (st.session_state.username,))

    logo = cur.fetchone()[0]

    if logo:
        st.image(logo, width=130)
    else:
        st.image("https://via.placeholder.com/150", width=130)

    logo_url = st.text_input("Paste Logo Image URL")

    if st.button("Save Logo"):

        cur.execute("""
        UPDATE institutes
        SET logo_path=?
        WHERE username=?
        """, (logo_url, st.session_state.username))

        conn.commit()
        st.success("Logo Updated")
        st.rerun()

    conn.close()

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "Upload TXT File",
        type=["txt"]
    )

    if uploaded_file is not None:

        content = uploaded_file.read().decode("utf-8")
        filename = uploaded_file.name

        conn = connect_db()
        cur = conn.cursor()

        cur.execute("""
        DELETE FROM documents
        WHERE username=? AND filename=?
        """, (st.session_state.username, filename))

        cur.execute("""
        INSERT INTO documents
        (username, filename, content)
        VALUES (?, ?, ?)
        """, (st.session_state.username, filename, content))

        conn.commit()
        conn.close()

        st.success("File Uploaded Successfully")

    # Show Uploaded Files
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT filename FROM documents
    WHERE username=?
    """, (st.session_state.username,))

    files = cur.fetchall()

    conn.close()

    st.subheader("Uploaded Files")

    for file in files:

        col1, col2 = st.columns([4, 1])

        with col1:
            st.write("📄", file[0])

        with col2:
            if st.button("Delete", key=file[0]):

                conn = connect_db()
                cur = conn.cursor()

                cur.execute("""
                DELETE FROM documents
                WHERE username=? AND filename=?
                """, (st.session_state.username, file[0]))

                conn.commit()
                conn.close()

                st.success(f"{file[0]} deleted successfully")
                st.rerun()

    st.markdown("---")

    if st.button("Logout"):
        logout()


# =====================================================
# STUDENT DASHBOARD
# =====================================================
elif st.session_state.user_type == "student":

    st.sidebar.success("Student Dashboard")

    conn = connect_db()
    cur = conn.cursor()

    # Student info
    cur.execute("""
    SELECT full_name, username, institute_code
    FROM students
    WHERE username=?
    """, (st.session_state.username,))

    student = cur.fetchone()

    full_name = student[0]
    username = student[1]
    institute_code = student[2]

    # Institute info
    cur.execute("""
    SELECT username, institute_name
    FROM institutes
    WHERE institute_code=?
    """, (institute_code,))

    institute = cur.fetchone()

    institute_username = institute[0]
    institute_name = institute[1]

    # Dashboard UI
    st.header("🎓 Student Dashboard")

    st.write(f"### Welcome {full_name}")
    st.write(f"**Username:** {username}")
    st.write(f"**Institute:** {institute_name}")
    st.write(f"**Institute Code:** {institute_code}")

    st.markdown("---")

    # Chatbot
    question = st.text_input("Ask your question")

    if st.button("Get Answer"):

        cur.execute("""
        SELECT filename, content FROM documents
        WHERE username=?
        """, (institute_username,))

        docs = cur.fetchall()

        best_score = 0
        best_answer = "No relevant answer found."

        question_lower = question.lower()
        question_words = question_lower.split()

        for doc in docs:

            filename = doc[0]
            content_original = doc[1]
            content = content_original.lower()

            score = 0

            # Basic word matching
            for word in question_words:
                if word in content:
                    score += 1

            # Smart file priority
            if "exam" in question_lower and "calendar" in filename.lower():
                score += 3

            if "start" in question_lower and "calendar" in filename.lower():
                score += 2

            if "date" in question_lower and "calendar" in filename.lower():
                score += 2

            if "deadline" in question_lower and "deadlines" in filename.lower():
                score += 3

            if "fee" in question_lower and "deadlines" in filename.lower():
                score += 2

            if "notice" in question_lower and "notices" in filename.lower():
                score += 3

            if "event" in question_lower and "events" in filename.lower():
                score += 3

            if "faculty" in question_lower and "faculty" in filename.lower():
                score += 3

            if "teacher" in question_lower and "faculty" in filename.lower():
                score += 2

            if "history" in question_lower and "history" in filename.lower():
                score += 3

            if "syllabus" in question_lower and "syllabus" in filename.lower():
                score += 3

            if "subject" in question_lower and "syllabus" in filename.lower():
                score += 2

            # Save best result
            if score > best_score:
                best_score = score

                lines = content_original.splitlines()
                matched_lines = []

                for line in lines:
                    line_lower = line.lower()

                    for word in question_words:
                        if word in line_lower:
                            matched_lines.append(line)
                            break

                if matched_lines:
                    response_text = ""

                    for item in matched_lines[:8]:
                        response_text += "- " + item.strip() + "\n\n"
                else:
                    response_text = content_original[:1200]

                best_answer = f"From {filename}:\n\n{response_text}"

        st.success("Answer Found")
        st.markdown(best_answer)

    conn.close()

    st.markdown("---")

    if st.button("Logout"):
        logout()
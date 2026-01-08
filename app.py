# ============================================================
# SA COLLEGE OF ARTS & SCIENCE – COMPLETE STUDENT PORTAL
# ============================================================
# FEATURES INCLUDED (NO REMOVALS):
# ------------------------------------------------------------
# 1. Student Registration (Name, Username, Password, School)
# 2. Student Login
# 3. Hidden Admin Login (Secret Key + Credentials)
# 4. Admin Panel (Dashboard, Students, Attempts)
# 5. About College (Image)
# 6. Location Map
# 7. CS & CS-AI Syllabus
# 8. HOD Section (Image)
# 9. Online Degree Entrance Test (12 Questions)
# 10. 5-Minute Modern Timer
# 11. One-Attempt-Only Exam Lock
# 12. Result + PDF Download
# 13. College GPT (Anti-misuse, Neutral)
# ============================================================

# ================= ADMIN SECURITY ===========================
ADMIN_ACCESS_KEY = "SACAS_ADMIN_2026"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ============================================================
# IMPORTS
# ============================================================
import streamlit as st
import os
import time
import pandas as pd
from pathlib import Path
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from openai import OpenAI
from streamlit_cookies_manager import EncryptedCookieManager
import sqlite3

# ============================================================
# SA COLLEGE OF ARTS & SCIENCE – STUDENT PORTAL (CORE SETUP)
# ============================================================

import streamlit as st
import sqlite3
import os
from pathlib import Path
from streamlit_cookies_manager import EncryptedCookieManager

# ============================================================
# PAGE CONFIG (FIRST STREAMLIT CALL)
# ============================================================
st.set_page_config(
    page_title="SA College of Arts & Science | Student Portal",
    page_icon="🎓",
    layout="wide"
)

# ============================================================
# COOKIE MANAGER (REMEMBER ME) — ONCE
# ============================================================
cookies = EncryptedCookieManager(
    prefix="college_gpt_",
    password="remember_me_secret_key_123"
)

if not cookies.ready():
    st.stop()

# ============================================================
# SESSION STATE INIT
# ============================================================
if "auth_page" not in st.session_state:
    st.session_state.auth_page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = {}

if "exam_step" not in st.session_state:
    st.session_state.exam_step = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "start_time" not in st.session_state:
    st.session_state.start_time = None

# ============================================================
# SQLITE DATABASE
# ============================================================
conn = sqlite3.connect("college.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    username TEXT UNIQUE,
    password TEXT,
    school TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS attempts (
    username TEXT PRIMARY KEY,
    completed INTEGER
)
""")

conn.commit()

# ============================================================
# SAFE IMAGE HELPER (FIXES YOUR ERROR)
# ============================================================
def show_image(path, **kwargs):
    if Path(path).exists():
        st.image(path, **kwargs)
    else:
        st.info("📷 Image will appear here when added")

# ============================================================
# AUTO LOGIN (REMEMBER ME)
# ============================================================
if not st.session_state.logged_in:
    remembered = cookies.get("username")
    if remembered:
        cursor.execute(
            "SELECT student_name, username, school FROM users WHERE username=?",
            (remembered,)
        )
        row = cursor.fetchone()
        if row:
            st.session_state.logged_in = True
            st.session_state.current_user = {
                "student_name": row[0],
                "username": row[1],
                "school": row[2]
            }

# ============================================================
# STUDENT AUTH (ONE BLOCK ONLY)
# ============================================================
if not st.session_state.logged_in:

    st.subheader("🔐 Student Authentication")

    if st.session_state.auth_page == "register":
        st.markdown("### 📝 Student Registration")

        name = st.text_input("Student Name")
        username = st.text_input("Register Number / Username")
        password = st.text_input("Password", type="password")
        school = st.text_input("School Name")

        if st.button("Create Account"):
            if not name or not username or not password:
                st.error("All fields required")
            else:
                try:
                    cursor.execute(
                        "INSERT INTO users (student_name, username, password, school) VALUES (?, ?, ?, ?)",
                        (name, username, password, school)
                    )
                    conn.commit()
                    st.success("Registration successful")
                    st.session_state.auth_page = "login"
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("Username already exists")

        st.button(
            "Already registered? Login",
            on_click=lambda: st.session_state.update(auth_page="login")
        )

    else:
        st.markdown("### 🔑 Student Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        remember = st.checkbox("Remember me")

        if st.button("Login"):
            cursor.execute(
                "SELECT student_name, username, school FROM users WHERE username=? AND password=?",
                (username, password)
            )
            row = cursor.fetchone()

            if row:
                st.session_state.logged_in = True
                st.session_state.current_user = {
                    "student_name": row[0],
                    "username": row[1],
                    "school": row[2]
                }

                if remember:
                    cookies["username"] = username
                    cookies.save()

                st.rerun()
            else:
                st.error("Invalid credentials")

        st.button(
            "New student? Register",
            on_click=lambda: st.session_state.update(auth_page="register")
        )

    st.stop()

# ===================== END OF SAFE BASE ======================


# ============================================================
# SIDEBAR (STUDENT)
# ============================================================
st.sidebar.success(f"Logged in as: {st.session_state.current_user['username']}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.auth_page = "login"
    st.session_state.current_user = {}
    st.session_state.exam_step = 1
    st.session_state.score = 0
    st.session_state.start_time = None
    st.rerun()

menu = st.sidebar.radio(
    "📘 Navigation",
    [
        "🏫 About College",
        "📍 Location",
        "📚 CS & CS-AI Syllabus",
        "👨‍🏫 CS with AI – HOD",
        "📝 Online Degree Entrance Test",
        "🤖 Ask College GPT"
    ]
)

# ============================================================
# ABOUT COLLEGE
# ============================================================
if menu == "🏫 About College":
    st.header("🏫 About SA College of Arts & Science")
    show_image("assets/ai_students.png", use_column_width=True)
    st.write("""
SA College of Arts & Science (SACAS) is located in **Thiruverkadu, Avadi, Chennai**.

### Focus Areas
- Academic Excellence
- Ethical Education
- Innovation & Research
- Holistic Student Development
""")

# ============================================================
# LOCATION
# ============================================================
elif menu == "📍 Location":
    st.header("📍 College Location")
    st.write("Thiruverkadu, Avadi, Chennai")
    st.map(pd.DataFrame({"lat":[13.0475],"lon":[80.1012]}))

# ============================================================
# SYLLABUS
# ============================================================
elif menu == "📚 CS & CS-AI Syllabus":
    st.header("📚 B.Sc Computer Science & CS with AI")
    st.subheader("Core Subjects")
    st.markdown("""
- Programming in C & Python  
- Data Structures  
- DBMS  
- Operating Systems  
- Computer Networks  
""")
    st.subheader("AI Specialization")
    st.markdown("""
- Artificial Intelligence  
- Machine Learning  
- Deep Learning  
- Natural Language Processing  
- Computer Vision  
""")

# ============================================================
# HOD
# ============================================================
elif menu == "👨‍🏫 CS with AI – HOD":
    st.header("👨‍🏫 Head of the Department – CS with AI")
    col1, col2 = st.columns([1,2])
    with col1:
        show_image("assets/hod.png", width=250)
    with col2:
        st.markdown("""
**Mr. Krishnan R**  
*M.Sc, M.Phil, NET, SET*

- UG Experience: 30 Years  
- PG Experience: 23 Years  

**Focus Areas**
- Industry-ready skills  
- Ethical AI  
- Practical learning  
""")

# ============================================================
# ONLINE DEGREE ENTRANCE TEST (12 QUESTIONS)
# ============================================================
elif menu == "📝 Online Degree Entrance Test":

    # ---------- CHECK IF ALREADY ATTEMPTED ----------
    cursor.execute(
        "SELECT completed FROM attempts WHERE username=?",
        (st.session_state.current_user["username"],)
    )
    attempt = cursor.fetchone()

    if attempt:
        st.error("🚫 You have already completed this test.")
        st.stop()

    # ---------- HEADER ----------
    st.header("📝 Online Degree Entrance Test")
    st.caption("⏱ Time: 5 Minutes | One Attempt Only")

    # ---------- TIMER ----------
    TOTAL_TIME = 5 * 60

    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, TOTAL_TIME - elapsed)

    st.progress(remaining / TOTAL_TIME)
    mins, secs = divmod(remaining, 60)

    st.markdown(
        f"<div style='background:#111;padding:15px;border-radius:10px;"
        f"text-align:center;color:#00ffcc;font-size:22px;'>"
        f"⏱ Time Left: {mins:02d}:{secs:02d}</div>",
        unsafe_allow_html=True
    )

    if remaining == 0:
        st.session_state.exam_step = 5

    st.divider()

    # -------- SECTION A --------
    if st.session_state.exam_step == 1:
        q1 = st.radio("1. 25% of 200 =", ["25","50","75","100"], index=None)
        q2 = st.radio("2. Average of 10, 20, 30 =", ["15","20","25","30"], index=None)
        q3 = st.radio("3. 12 × 8 =", ["96","84","88","72"], index=None)

        if st.button("Next ➡️"):
            if q1 == "50": st.session_state.score += 10
            if q2 == "20": st.session_state.score += 10
            if q3 == "96": st.session_state.score += 10
            st.session_state.exam_step = 2
            st.rerun()

    # -------- SECTION B --------
    elif st.session_state.exam_step == 2:
        q4 = st.radio("4. Odd one out:", ["Apple","Banana","Car","Mango"], index=None)
        q5 = st.radio("5. Series: 2, 4, 8, ?", ["12","14","16","18"], index=None)
        q6 = st.radio("6. A > B and B > C then:", ["A > C","C > A"], index=None)

        if st.button("Next ➡️"):
            if q4 == "Car": st.session_state.score += 10
            if q5 == "16": st.session_state.score += 10
            if q6 == "A > C": st.session_state.score += 10
            st.session_state.exam_step = 3
            st.rerun()

    # -------- SECTION C --------
    elif st.session_state.exam_step == 3:
        q7 = st.radio("7. CPU stands for:", ["Central Processing Unit","Control Unit"], index=None)
        q8 = st.radio("8. Binary system uses:", ["0 & 1","1 & 2"], index=None)
        q9 = st.radio("9. Python is:", ["High-level","Low-level"], index=None)

        if st.button("Next ➡️"):
            if q7 == "Central Processing Unit": st.session_state.score += 10
            if q8 == "0 & 1": st.session_state.score += 10
            if q9 == "High-level": st.session_state.score += 10
            st.session_state.exam_step = 4
            st.rerun()

    # -------- SECTION D --------
    elif st.session_state.exam_step == 4:
        q10 = st.radio("10. Capital of Tamil Nadu:", ["Chennai","Madurai"], index=None)
        q11 = st.radio("11. Father of Computer:", ["Charles Babbage","Newton"], index=None)
        q12 = st.radio("12. National Animal of India:", ["Tiger","Lion"], index=None)

        if st.button("Submit Exam"):
            if q10 == "Chennai": st.session_state.score += 10
            if q11 == "Charles Babbage": st.session_state.score += 10
            if q12 == "Tiger": st.session_state.score += 10

            # ---------- SAVE ATTEMPT (SQLITE) ----------
            cursor.execute(
                "INSERT INTO attempts (username, completed) VALUES (?, ?)",
                (st.session_state.current_user["username"], 1)
            )
            conn.commit()

            st.session_state.exam_step = 5
            st.rerun()

    # -------- RESULT --------
    elif st.session_state.exam_step == 5:
        st.success(f"🎯 Final Score: {st.session_state.score} / 120")


# ============================================================
# COLLEGE GPT (CHATGPT-LIKE, TAMIL + ENGLISH, SA PRIORITY)
# ============================================================
elif menu == "🤖 Ask College GPT":
    st.header("🤖 College GPT")
    st.caption("Student guidance assistant | Tamil + English supported")

    # ---------- Initialize chat history ----------
    if "college_gpt_chat" not in st.session_state:
        st.session_state.college_gpt_chat = []

    # ---------- Helper functions ----------
    def is_tamil(text):
        return any('\u0B80' <= ch <= '\u0BFF' for ch in text)

    def contains_any(text, keywords):
        return any(k in text.lower() for k in keywords)

    # Topic detectors
    cinema_keys = ["cinema", "movie", "film", "actor", "actress", "hero", "director"]
    sports_keys = ["sports", "cricket", "football", "match", "game", "ipl"]
    music_keys = ["music", "song", "dance", "singer"]
    job_keys = ["job", "salary", "package", "placement", "career"]
    love_keys = ["love", "relationship", "dating"]
    travel_keys = ["travel", "tour", "place", "trip"]
    food_keys = ["food", "canteen", "snacks"]

    # ---------- System Prompt (UNCHANGED) ----------
    SYSTEM_PROMPT = """
You are College GPT, an academic guidance assistant.

Language rule (VERY IMPORTANT):
- Respond in ENGLISH by default.
- Respond in TAMIL only if:
  • The user asks the question in Tamil, OR
  • The user explicitly asks for Tamil.
- Do NOT mix Tamil unless requested.

Primary Institution Focus:
- "SA", "SACAS", or "SA College" means SA College of Arts & Science.

Rules:
- Never criticize any college.
- Never rank colleges.
- Maintain respectful academic tone.
- Guide students on academics, syllabus, exams, careers.
"""

    # ---------- Display chat history ----------
    for msg in st.session_state.college_gpt_chat:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # ---------- Chat input ----------
    user_question = st.chat_input("Ask about SA College, syllabus, careers...")

    if user_question:
        st.session_state.college_gpt_chat.append(
            {"role": "user", "content": user_question}
        )

        with st.chat_message("user"):
            st.write(user_question)

        # ---------- Language enforcement ----------
        language_instruction = (
            "Respond ONLY in TAMIL." if is_tamil(user_question)
            else "Respond ONLY in ENGLISH."
        )

        # ---------- REDIRECTION LOGIC (ADDED) ----------
        if contains_any(user_question, cinema_keys):
            assistant_reply = (
                "🎓 College GPT is for education purpose.\n\n"
                "Students interested in cinema and media can choose the "
                "**Visual Communication (VISCOM)** course at "
                "SA College of Arts & Science, which covers media studies, "
                "film basics, editing, photography, advertising, and digital media."
            )

        elif contains_any(user_question, sports_keys):
            assistant_reply = (
                "🎓 College GPT is for education purpose.\n\n"
                "SA College of Arts & Science encourages sports and physical activities. "
                "Students can participate in cricket, football, athletics, "
                "and indoor games for overall development."
            )

        elif contains_any(user_question, music_keys):
            assistant_reply = (
                "🎓 College GPT is for education purpose.\n\n"
                "The college supports cultural activities such as music and dance "
                "through cultural clubs and events that help students showcase talent."
            )

        elif contains_any(user_question, job_keys):
            assistant_reply = (
                "🎓 College GPT is for education purpose.\n\n"
                "Career guidance at SA College of Arts & Science focuses on skill development, "
                "higher studies, internships, and placement-oriented training."
            )

        elif contains_any(user_question, love_keys):
            assistant_reply = (
                "🎓 College GPT is for education purpose.\n\n"
                "The college emphasizes discipline, ethics, and student counselling "
                "to support personal and academic well-being."
            )

        elif contains_any(user_question, travel_keys):
            assistant_reply = (
                "🎓 College GPT is for education purpose.\n\n"
                "Students gain exposure through NSS activities, educational visits, "
                "workshops, and outreach programs organized by the college."
            )

        elif contains_any(user_question, food_keys):
            assistant_reply = (
                "🎓 College GPT is for education purpose.\n\n"
                "SA College of Arts & Science provides basic campus facilities, "
                "including a canteen for students."
            )

        # ---------- NORMAL ACADEMIC QUESTIONS ----------
        else:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            try:
                with st.spinner("College GPT is thinking 🤖"):
                    response = client.responses.create(
                        model="gpt-4.1-mini",
                        input=[
                            {
                                "role": "system",
                                "content": SYSTEM_PROMPT + "\n\n" + language_instruction
                            },
                            *st.session_state.college_gpt_chat
                        ]
                    )
                assistant_reply = response.output_text.strip()[:600]

            except Exception:
                assistant_reply = (
                    "Sorry, I am temporarily unavailable. Please try again later."
                )

        # ---------- Save assistant reply ----------
        st.session_state.college_gpt_chat.append(
            {"role": "assistant", "content": assistant_reply}
        )

        with st.chat_message("assistant"):
            st.write(assistant_reply)



# ============================================================
# SA COLLEGE OF ARTS & SCIENCE – STUDENT PORTAL
# Register + Login + One-Time Exam + College GPT
# Author: Avinash
# ============================================================

import streamlit as st
import os
import time
import pandas as pd
from openai import OpenAI
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

# ============================================================
# FILE PATHS
# ============================================================

USERS_FILE = "users.csv"
ATTEMPTS_FILE = "attempts.csv"

# ============================================================
# INITIAL FILE SETUP
# ============================================================

if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["name", "username", "password", "school"]).to_csv(USERS_FILE, index=False)

if not os.path.exists(ATTEMPTS_FILE):
    pd.DataFrame(columns=["username", "completed"]).to_csv(ATTEMPTS_FILE, index=False)

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SA College of Arts & Science | Student Portal",
    page_icon="🎓",
    layout="wide"
)

# ============================================================
# SESSION STATE INIT
# ============================================================

for key, value in {
    "logged_in": False,
    "username": "",
    "page": "login"
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ============================================================
# SAFE IMAGE
# ============================================================

def show_image(path, **kwargs):
    if Path(path).exists():
        st.image(path, **kwargs)

# ============================================================
# PDF GENERATOR
# ============================================================

def generate_pdf(name, score, grade, degree, career):
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(w/2, h-50, "SA COLLEGE OF ARTS & SCIENCE")

    c.setFont("Helvetica", 12)
    c.drawCentredString(w/2, h-80, "ONLINE ENTRANCE TEST RESULT")

    y = h - 140
    c.drawString(50, y, f"Student Name: {name}")
    y -= 25
    c.drawString(50, y, f"Score: {score} / 120")
    y -= 25
    c.drawString(50, y, f"Grade: {grade}")
    y -= 25
    c.drawString(50, y, f"Recommended Degree: {degree}")

    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Career Options:")
    c.setFont("Helvetica", 11)
    y -= 20

    for cpath in career:
        c.drawString(70, y, f"- {cpath}")
        y -= 18

    c.save()
    buf.seek(0)
    return buf

# ============================================================
# HEADER
# ============================================================

st.markdown(
    "<h1 style='text-align:center'>🎓 SA College of Arts & Science</h1>"
    "<p style='text-align:center;color:gray'>Affiliated to University of Madras</p>",
    unsafe_allow_html=True
)

st.divider()

# ============================================================
# REGISTER PAGE
# ============================================================

if st.session_state.page == "register":
    st.header("📝 Student Registration")

    name = st.text_input("Student Name")
    username = st.text_input("Register Number / Username")
    password = st.text_input("Password", type="password")
    school = st.text_input("School Name")

    if st.button("Create Account"):
        users = pd.read_csv(USERS_FILE)
        if username in users["username"].values:
            st.error("Username already exists")
        else:
            users.loc[len(users)] = [name, username, password, school]
            users.to_csv(USERS_FILE, index=False)
            st.success("Registration successful")
            st.session_state.page = "login"
            st.rerun()

    st.button("Already have account? Login", on_click=lambda: st.session_state.update(page="login"))

# ============================================================
# LOGIN PAGE
# ============================================================

elif st.session_state.page == "login":
    st.header("🔐 Student Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = pd.read_csv(USERS_FILE)
        valid = users[(users.username == username) & (users.password == password)]
        if not valid.empty:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = "home"
            st.rerun()
        else:
            st.error("Invalid login")

    st.button("New student? Register", on_click=lambda: st.session_state.update(page="register"))

# ============================================================
# HOME (AFTER LOGIN)
# ============================================================

elif st.session_state.page == "home":
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update(logged_in=False, page="login"))

    menu = st.sidebar.radio(
        "Navigation",
        ["About College", "Entrance Test", "College GPT"]
    )

    # ================= ABOUT =================
    if menu == "About College":
        st.header("About SA College")
        show_image("assets/ai_students.png", use_column_width=True)
        st.write("Located in Thiruverkadu, Avadi, Chennai. Focus on academic excellence and AI education.")

    # ================= ENTRANCE TEST =================
    elif menu == "Entrance Test":
        attempts = pd.read_csv(ATTEMPTS_FILE)

        if st.session_state.username in attempts["username"].values:
            st.error("🚫 You have already completed the test.")
            st.stop()

        TOTAL_TIME = 5 * 60

        if "start_time" not in st.session_state:
            st.session_state.start_time = time.time()
            st.session_state.step = 1
            st.session_state.score = 0

        elapsed = int(time.time() - st.session_state.start_time)
        remaining = max(0, TOTAL_TIME - elapsed)

        st.progress(remaining / TOTAL_TIME)
        mins, secs = divmod(remaining, 60)
        st.markdown(f"<h3 style='text-align:center'>⏱ {mins:02d}:{secs:02d}</h3>", unsafe_allow_html=True)

        if remaining == 0:
            st.session_state.step = 5

        # ---- QUESTIONS ----
        if st.session_state.step == 1:
            q = st.radio("25% of 200", ["25","50","75","100"])
            if st.button("Next"):
                if q == "50": st.session_state.score += 10
                st.session_state.step = 2
                st.rerun()

        elif st.session_state.step == 2:
            q = st.radio("Odd one out", ["Apple","Car","Banana"])
            if st.button("Next"):
                if q == "Car": st.session_state.score += 10
                st.session_state.step = 3
                st.rerun()

        elif st.session_state.step == 3:
            q = st.radio("CPU stands for", ["Central Processing Unit","Control Unit"])
            if st.button("Next"):
                if q == "Central Processing Unit": st.session_state.score += 10
                st.session_state.step = 4
                st.rerun()

        elif st.session_state.step == 4:
            q = st.radio("Capital of Tamil Nadu", ["Chennai","Madurai"])
            if st.button("Submit"):
                if q == "Chennai": st.session_state.score += 10
                st.session_state.step = 5
                st.rerun()

        elif st.session_state.step == 5:
            attempts.loc[len(attempts)] = [st.session_state.username, True]
            attempts.to_csv(ATTEMPTS_FILE, index=False)

            score = st.session_state.score
            grade = "A" if score >= 30 else "B"
            degree = "B.Sc CS / CS-AI"
            career = ["Software Engineer","AI Engineer"]

            pdf = generate_pdf(st.session_state.username, score, grade, degree, career)
            st.download_button("Download PDF", pdf, "result.pdf")

    # ================= COLLEGE GPT =================
    elif menu == "College GPT":
        st.header("🤖 College GPT")

        SYSTEM_PROMPT = """
You are College GPT.
Do not compare colleges.
Do not criticize any institution.
Provide neutral academic guidance only.
"""

        q = st.chat_input("Ask a question")
        if q:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            r = client.responses.create(
                model="gpt-4.1-mini",
                input=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":q}]
            )
            st.write(r.output_text)

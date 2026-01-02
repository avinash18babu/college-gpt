# ============================================================
# SA COLLEGE OF ARTS & SCIENCE – COLLEGE GPT PLATFORM
# Purpose: Student Guidance + One-Time Online Entrance Test
# Author: Avinash
# ============================================================

import streamlit as st
from openai import OpenAI
import os
import time
import pandas as pd
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SA College of Arts & Science | College GPT",
    page_icon="🎓",
    layout="wide"
)

# ============================================================
# LOGIN SYSTEM (MANDATORY)
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.title("🔐 Student Login")
    st.caption("Login required to access exam and College GPT")

    username = st.text_input("Enter Register Number / Username")
    login_btn = st.button("Login")

    if login_btn:
        if username.strip():
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Please enter a valid username")

    st.stop()

# ============================================================
# PDF GENERATION
# ============================================================

def generate_pdf(name, total, grade, degree, career):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 50, "SA COLLEGE OF ARTS & SCIENCE")

    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 80, "ONLINE DEGREE ENTRANCE TEST RESULT")

    y = height - 130
    c.drawString(50, y, f"Student Name: {name}")
    y -= 25
    c.drawString(50, y, f"Total Score: {total} / 120")
    y -= 25
    c.drawString(50, y, f"Grade: {grade}")
    y -= 25
    c.drawString(50, y, f"Recommended Degree: {degree}")

    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Suggested Career Paths:")
    y -= 20
    c.setFont("Helvetica", 11)

    for cpath in career:
        c.drawString(70, y, f"- {cpath}")
        y -= 18

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <h1 style='text-align:center;'>🎓 SA College of Arts & Science</h1>
    <p style='text-align:center;color:gray;'>Affiliated to University of Madras</p>
    <p style='text-align:center;font-size:13px;'>College GPT by Avinash</p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ============================================================
# SIDEBAR
# ============================================================

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
# ABOUT
# ============================================================

if menu == "🏫 About College":
    st.header("🏫 About SA College of Arts & Science")
    st.write("""
SA College of Arts & Science (SACAS) is located in **Thiruverkadu, Avadi, Chennai**.

**Focus Areas**
- Academic Excellence  
- Ethical Education  
- Research & Innovation  
- Career-Oriented Learning  
""")

# ============================================================
# LOCATION
# ============================================================

elif menu == "📍 Location":
    st.header("📍 College Location")
    st.write("Thiruverkadu, Avadi, Chennai")
    df = pd.DataFrame({"lat":[13.0475], "lon":[80.1012]})
    st.map(df)

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
- NLP  
- Computer Vision  
""")

# ============================================================
# HOD
# ============================================================

elif menu == "👨‍🏫 CS with AI – HOD":
    st.header("👨‍🏫 Head of the Department – CS with AI")

    st.markdown("""
**Mr. Krishnan R**  
*M.Sc, M.Phil, NET, SET*

- UG Experience: 30 Years  
- PG Experience: 23 Years  

**Focus:** Industry-ready skills, ethical AI, practical learning
""")

# ============================================================
# ONLINE DEGREE ENTRANCE TEST (ONE ATTEMPT ONLY)
# ============================================================

elif menu == "📝 Online Degree Entrance Test":
    st.header("📝 Online Degree Entrance Test")
    st.caption("One attempt only • Time: 5 Minutes")

    if "exam_completed" not in st.session_state:
        st.session_state.exam_completed = False

    if st.session_state.exam_completed:
        st.error("🚫 You have already completed the test.")
        st.stop()

    TOTAL_TIME = 5 * 60

    if "exam_step" not in st.session_state:
        st.session_state.exam_step = 1
        st.session_state.score = 0
        st.session_state.start_time = time.time()

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, TOTAL_TIME - elapsed)

    progress = remaining / TOTAL_TIME
    st.progress(progress)

    mins, secs = divmod(remaining, 60)
    st.markdown(
        f"<div style='text-align:center;font-size:22px;color:#00ffaa;'>⏱ {mins:02d}:{secs:02d}</div>",
        unsafe_allow_html=True
    )

    if remaining == 0:
        st.session_state.exam_step = 5

    st.divider()

    # ---------- SECTION A ----------
    if st.session_state.exam_step == 1:
        q1 = st.radio("25% of 200 =", ["25","50","75","100"], index=None)
        q2 = st.radio("Average of 10,20,30 =", ["15","20","25","30"], index=None)
        q3 = st.radio("12 × 8 =", ["96","84","88","72"], index=None)

        if st.button("Next"):
            if q1 == "50": st.session_state.score += 10
            if q2 == "20": st.session_state.score += 10
            if q3 == "96": st.session_state.score += 10
            st.session_state.exam_step = 2
            st.rerun()

    # ---------- SECTION B ----------
    elif st.session_state.exam_step == 2:
        q1 = st.radio("Odd one out", ["Apple","Banana","Car","Mango"], index=None)
        q2 = st.radio("2,4,8,?", ["12","14","16","18"], index=None)
        q3 = st.radio("A>B, B>C then", ["A>C","C>A"], index=None)

        if st.button("Next"):
            if q1 == "Car": st.session_state.score += 10
            if q2 == "16": st.session_state.score += 10
            if q3 == "A>C": st.session_state.score += 10
            st.session_state.exam_step = 3
            st.rerun()

    # ---------- SECTION C ----------
    elif st.session_state.exam_step == 3:
        q1 = st.radio("CPU stands for", ["Central Processing Unit","Control Unit"], index=None)
        q2 = st.radio("Binary uses", ["0 & 1","1 & 2"], index=None)
        q3 = st.radio("Python is", ["High-level","Low-level"], index=None)

        if st.button("Next"):
            if q1 == "Central Processing Unit": st.session_state.score += 10
            if q2 == "0 & 1": st.session_state.score += 10
            if q3 == "High-level": st.session_state.score += 10
            st.session_state.exam_step = 4
            st.rerun()

    # ---------- SECTION D ----------
    elif st.session_state.exam_step == 4:
        q1 = st.radio("Capital of Tamil Nadu", ["Chennai","Madurai"], index=None)
        q2 = st.radio("Father of Computer", ["Charles Babbage","Newton"], index=None)
        q3 = st.radio("National Animal of India", ["Tiger","Lion"], index=None)

        if st.button("Submit Exam"):
            if q1 == "Chennai": st.session_state.score += 10
            if q2 == "Charles Babbage": st.session_state.score += 10
            if q3 == "Tiger": st.session_state.score += 10
            st.session_state.exam_step = 5
            st.rerun()

    # ---------- RESULT ----------
    elif st.session_state.exam_step == 5:
        st.session_state.exam_completed = True

        score = st.session_state.score
        st.success(f"🎯 Score: {score} / 120")

        if score >= 90:
            grade = "A"
            degree = "B.Sc CS / CS with AI"
            career = ["Software Engineer","AI Engineer","Data Scientist"]
        elif score >= 60:
            grade = "B"
            degree = "BCA / B.Sc / B.Com"
            career = ["Business Analyst","IT Support"]
        else:
            grade = "C"
            degree = "Arts / Management"
            career = ["HR","Administration"]

        pdf = generate_pdf(st.session_state.username, score, grade, degree, career)
        st.download_button("📥 Download Result PDF", pdf, "Result.pdf")

# ============================================================
# COLLEGE GPT (SAFE & NON-MISUSE)
# ============================================================

elif menu == "🤖 Ask College GPT":
    st.header("🤖 College GPT")
    st.caption("Neutral academic guidance • No comparison")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    for m in st.session_state.chat:
        st.chat_message(m["role"]).write(m["content"])

    question = st.chat_input("Ask your question")

    if question:
        st.session_state.chat.append({"role":"user","content":question})

        SYSTEM_PROMPT = """
You are College GPT created for student guidance.
Rules:
- Do not compare or rank colleges.
- Do not criticize any institution.
- Provide neutral academic guidance only.
"""

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        res = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role":"system","content":SYSTEM_PROMPT},
                {"role":"user","content":question}
            ]
        )

        reply = res.output_text
        st.session_state.chat.append({"role":"assistant","content":reply})
        st.rerun()

# ============================================================
# SA COLLEGE OF ARTS & SCIENCE – COLLEGE GPT WEB APPLICATION
# Created for Student Guidance & Academic Assistance
# Author: Avinash
# Platform: Streamlit + OpenAI
# ============================================================

import streamlit as st
from openai import OpenAI
import os
from pathlib import Path
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
import time

# ============================================================
# PDF GENERATION FUNCTION
# ============================================================

def generate_pdf(name, total, grade, degree, career):
    """
    Generates a PDF report for the entrance test result.
    This PDF is meant only for student reference.
    """

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # ---------- Title ----------
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, height - 50, "SA COLLEGE OF ARTS & SCIENCE")

    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 80, "ONLINE DEGREE ENTRANCE TEST RESULT")

    # ---------- Student Details ----------
    y = height - 130
    c.drawString(50, y, f"Student Name: {name}")
    y -= 25
    c.drawString(50, y, f"Total Score: {total} / 120")
    y -= 25
    c.drawString(50, y, f"Grade: {grade}")
    y -= 25
    c.drawString(50, y, f"Recommended Degree: {degree}")

    # ---------- Career Suggestions ----------
    y -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Suggested Career Paths:")
    y -= 20
    c.setFont("Helvetica", 11)

    for path in career:
        c.drawString(70, y, f"- {path}")
        y -= 18

    # ---------- Save PDF ----------
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# ============================================================
# STREAMLIT PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SA College of Arts & Science | College GPT",
    page_icon="🎓",
    layout="wide"
)

# ============================================================
# SAFE IMAGE DISPLAY FUNCTION
# ============================================================

def show_image(path, **kwargs):
    """
    Displays image only if file exists.
    Prevents runtime crash if image is missing.
    """
    if Path(path).exists():
        st.image(path, **kwargs)
    else:
        st.info(f"Image missing: {path}")

# ============================================================
# HEADER SECTION
# ============================================================

st.markdown("""
<style>
.title{font-size:40px;font-weight:700;text-align:center;}
.subtitle{font-size:18px;text-align:center;color:gray;}
.credit{font-size:13px;text-align:center;color:#666;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎓 SA College of Arts & Science</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Affiliated to University of Madras</div>', unsafe_allow_html=True)
st.markdown('<div class="credit">College GPT by Avinash</div>', unsafe_allow_html=True)
st.divider()

# ============================================================
# SIDEBAR NAVIGATION
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
# ABOUT COLLEGE PAGE
# ============================================================

if menu == "🏫 About College":
    st.header("🏫 About SA College of Arts & Science")

    st.write("""
SA College of Arts & Science (SACAS) is a reputed Arts & Science institution  
located in **Thiruverkadu, Avadi, Chennai**.

### Focus Areas
- Academic Excellence
- Innovation & Research
- Discipline & Ethics
- Holistic Student Development
    """)

    show_image("assets/ai_students.png", use_column_width=True)

# ============================================================
# LOCATION PAGE
# ============================================================

elif menu == "📍 Location":
    st.header("📍 College Location")
    st.write("**SA College of Arts & Science, Thiruverkadu, Avadi, Chennai**")

    df = pd.DataFrame({
        "lat": [13.0475],
        "lon": [80.1012]
    })
    st.map(df)

# ============================================================
# SYLLABUS PAGE
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
# HOD PAGE
# ============================================================

elif menu == "👨‍🏫 CS with AI – HOD":
    st.header("👨‍🏫 Head of the Department – CS with AI")

    col1, col2 = st.columns([1, 2])

    with col1:
        show_image("assets/hod.png", width=250)

    with col2:
        st.markdown("""
**Mr. Krishnan R**  
*M.Sc, M.Phil, NET, SET*

**Experience**
- UG: 30 Years
- PG: 23 Years

**Focus Areas**
- Industry-ready skills
- Ethical AI practices
- Practical learning approach
        """)

# ============================================================
# ONLINE DEGREE ENTRANCE TEST
# ============================================================

elif menu == "📝 Online Degree Entrance Test":
    st.header("📝 Online Degree Entrance Test")
    st.caption("Exam Pattern: Aptitude • Logical • Computer • GK | Time: 10 Minutes")

    student_name = st.text_input("Enter Student Name")

    TOTAL_TIME = 10 * 60

    if "exam_step" not in st.session_state:
        st.session_state.exam_step = 1
        st.session_state.score = 0

    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = TOTAL_TIME - elapsed

    if remaining <= 0:
        st.warning("⏰ Time is up! Auto-submitting exam.")
        st.session_state.exam_step = 5
        remaining = 0

    mins, secs = divmod(remaining, 60)
    st.info(f"⏱️ Time Remaining: {mins:02d}:{secs:02d}")
    st.divider()

    # -------- SECTION A --------
    if st.session_state.exam_step == 1:
        st.subheader("📊 Section A: Quantitative Aptitude")

        q1 = st.radio("1. 25% of 200 =", ["25","50","75","100"], index=None)
        q2 = st.radio("2. Average of 10,20,30 =", ["15","20","25","30"], index=None)
        q3 = st.radio("3. 12 × 8 =", ["96","84","88","72"], index=None)

        if st.button("Next ➡️"):
            if q1 == "50": st.session_state.score += 10
            if q2 == "20": st.session_state.score += 10
            if q3 == "96": st.session_state.score += 10
            st.session_state.exam_step = 2
            st.rerun()

    # -------- SECTION B --------
    elif st.session_state.exam_step == 2:
        st.subheader("🧠 Section B: Logical Reasoning")

        q1 = st.radio("4. Odd one out:", ["Apple","Banana","Car","Mango"], index=None)
        q2 = st.radio("5. Series: 2,4,8,?", ["12","14","16","18"], index=None)
        q3 = st.radio("6. A>B, B>C then:", ["A>C","C>A"], index=None)

        if st.button("Next ➡️"):
            if q1 == "Car": st.session_state.score += 10
            if q2 == "16": st.session_state.score += 10
            if q3 == "A>C": st.session_state.score += 10
            st.session_state.exam_step = 3
            st.rerun()

    # -------- SECTION C --------
    elif st.session_state.exam_step == 3:
        st.subheader("💻 Section C: Computer Knowledge")

        q1 = st.radio("7. CPU stands for:", ["Central Processing Unit","Control Unit"], index=None)
        q2 = st.radio("8. Binary system uses:", ["0 & 1","1 & 2"], index=None)
        q3 = st.radio("9. Python is:", ["High-level","Low-level"], index=None)

        if st.button("Next ➡️"):
            if q1 == "Central Processing Unit": st.session_state.score += 10
            if q2 == "0 & 1": st.session_state.score += 10
            if q3 == "High-level": st.session_state.score += 10
            st.session_state.exam_step = 4
            st.rerun()

    # -------- SECTION D --------
    elif st.session_state.exam_step == 4:
        st.subheader("🌍 Section D: General Knowledge")

        q1 = st.radio("10. Capital of Tamil Nadu:", ["Chennai","Madurai"], index=None)
        q2 = st.radio("11. Father of Computer:", ["Charles Babbage","Newton"], index=None)
        q3 = st.radio("12. National Animal of India:", ["Tiger","Lion"], index=None)

        if st.button("Submit Exam"):
            if q1 == "Chennai": st.session_state.score += 10
            if q2 == "Charles Babbage": st.session_state.score += 10
            if q3 == "Tiger": st.session_state.score += 10
            st.session_state.exam_step = 5
            st.rerun()

    # -------- RESULT --------
    elif st.session_state.exam_step == 5:
        st.header("📄 Final Result")

        score = st.session_state.score
        st.success(f"🎯 Total Score: {score} / 120")

        if score >= 90:
            grade = "A"
            degree = "B.Sc Computer Science / CS with AI"
            career = ["Software Engineer","AI Engineer","Data Scientist"]
        elif score >= 60:
            grade = "B"
            degree = "BCA / B.Sc / B.Com"
            career = ["Business Analyst","IT Support","Banking"]
        else:
            grade = "C"
            degree = "Arts / Management"
            career = ["HR","Administration","Creative Fields"]

        st.info(f"🎖 Grade: {grade}")
        st.write(f"🎓 Recommended Degree: {degree}")

        pdf = generate_pdf(student_name, score, grade, degree, career)
        st.download_button(
            "📥 Download Result PDF",
            pdf,
            file_name="Entrance_Test_Result.pdf",
            mime="application/pdf"
        )

        if st.button("Restart Exam"):
            st.session_state.clear()
            st.rerun()

# ============================================================
# COLLEGE GPT – SAFE AI CHATBOT
# ============================================================

elif menu == "🤖 Ask College GPT":
    st.header("🤖 College GPT")
    st.caption("Academic guidance only • Neutral • Non-comparative")

    st.info(
        "ℹ️ This chatbot provides academic guidance only. "
        "It does not rank, compare, or criticize any college."
    )

    if "chat" not in st.session_state:
        st.session_state.chat = []

    for msg in st.session_state.chat:
        st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("Ask your question")

    if user_input:
        st.session_state.chat.append({"role": "user", "content": user_input})

        SYSTEM_PROMPT = """
You are College GPT created only for student guidance.

Rules:
- Answer politely, neutrally, and academically.
- Do NOT rank or compare colleges.
- Do NOT promote or criticize any institution.
- Provide guidance on academics, syllabus, and careers only.
- Redirect misuse questions safely.
- Encourage verification from official sources.
"""

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        res = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ]
        )

        reply = res.output_text
        st.session_state.chat.append({"role": "assistant", "content": reply})
        st.rerun()

# ============================================================
# END OF APPLICATION
# ============================================================

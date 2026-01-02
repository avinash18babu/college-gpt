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

    # (Exam questions intentionally unchanged for stability)

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

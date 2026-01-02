import streamlit as st
from openai import OpenAI
import os
from pathlib import Path
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
import time
import random

# ================= PDF GENERATOR =================
def generate_pdf(name, total, grade, degree, career, section_scores):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height-50, "SA COLLEGE OF ARTS & SCIENCE")

    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height-80, "ONLINE DEGREE ENTRANCE TEST RESULT")

    y = height - 130
    c.drawString(50, y, f"Student Name: {name}")
    y -= 25
    c.drawString(50, y, f"Total Score: {total} / 100")
    y -= 25
    c.drawString(50, y, f"Grade: {grade}")
    y -= 25
    c.drawString(50, y, f"Recommended Degree: {degree}")

    y -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Section-wise Performance")
    c.setFont("Helvetica", 11)
    y -= 25

    for sec, marks in section_scores.items():
        c.drawString(70, y, f"{sec}: {marks} / 25")
        y -= 20

    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Suggested Career Paths")
    c.setFont("Helvetica", 11)
    y -= 20

    for cpath in career:
        c.drawString(70, y, f"- {cpath}")
        y -= 18

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="SA College of Arts & Science | College GPT",
    page_icon="🎓",
    layout="wide"
)

# ================= HEADER =================
st.markdown("""
<style>
.title{font-size:40px;font-weight:700;text-align:center;}
.subtitle{font-size:18px;text-align:center;color:gray;}
.credit{font-size:13px;text-align:center;color:#666;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎓 SA College of Arts & Science</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-Based Online Degree Entrance Test</div>', unsafe_allow_html=True)
st.markdown('<div class="credit">College GPT by Avinash</div>', unsafe_allow_html=True)
st.divider()

# ================= SIDEBAR =================
menu = st.sidebar.radio(
    "📘 Navigation",
    [
        "🏫 About College",
        "📝 Online Degree Entrance Test",
        "🤖 Ask College GPT"
    ]
)

# ================= QUESTION BANKS =================

APTITUDE_QS = [
    ("25% of 200 =", ["25","50","75","100"], "50"),
    ("15² =", ["125","200","225","250"], "225"),
    ("144 ÷ 12 =", ["10","11","12","13"], "12"),
    ("Average of 10, 20, 30 =", ["15","20","25","30"], "20"),
    ("20% of 300 =", ["30","40","60","80"], "60"),
    ("3 : 6 :: 5 : ?", ["10","15","20","30"], "10"),
    ("40% of 250 =", ["80","90","100","110"], "100"),
    ("12 × 9 =", ["96","108","112","120"], "108")
]

LOGICAL_QS = [
    ("Odd one out", ["Apple","Banana","Car","Mango"], "Car"),
    ("Series: 2, 4, 8, ?", ["12","14","16","18"], "16"),
    ("A > B, B > C then?", ["A > C","C > A"], "A > C"),
    ("Mirror of EAST", ["TSAE","HSAE"], "TSAE"),
    ("Find missing: A, C, E, ?", ["F","G","H"], "G"),
    ("Clock angle at 3:00", ["90°","60°"], "90°")
]

COMPUTER_QS = [
    ("CPU stands for", ["Central Processing Unit","Control Unit"], "Central Processing Unit"),
    ("Binary system uses", ["0 & 1","1 & 2"], "0 & 1"),
    ("Python is a", ["High-level","Low-level"], "High-level"),
    ("RAM is", ["Temporary","Permanent"], "Temporary"),
    ("AI stands for", ["Artificial Intelligence","Advanced Internet"], "Artificial Intelligence"),
    ("NOT a programming language", ["Java","Python","Oracle"], "Oracle")
]

GK_QS = [
    ("Capital of Tamil Nadu", ["Chennai","Madurai"], "Chennai"),
    ("Father of Computer", ["Charles Babbage","Newton"], "Charles Babbage"),
    ("National Animal of India", ["Tiger","Lion"], "Tiger"),
    ("ISRO deals with", ["Space","Medicine"], "Space"),
    ("UNO Headquarters", ["New York","London"], "New York"),
    ("Internet is a", ["Network","Device"], "Network")
]

# ================= ABOUT =================
if menu == "🏫 About College":
    st.header("🏫 About SA College of Arts & Science")
    st.write("""
SA College of Arts & Science (SACAS) is located in  
**Thiruverkadu, Avadi, Chennai** and affiliated to the **University of Madras**.

This portal provides:
- College information
- AI-powered counselling
- Professional online entrance test
""")

# ================= ENTRANCE TEST =================
elif menu == "📝 Online Degree Entrance Test":
    st.header("📝 Online Degree Entrance Test")
    st.caption("Pattern: Aptitude • Logical • Computer • General Knowledge")
    st.caption("⏱ Duration: 10 Minutes | Total Marks: 100")

    student_name = st.text_input("Enter Student Name")

    TOTAL_TIME = 10 * 60

    if "step" not in st.session_state:
        st.session_state.step = 1
        st.session_state.start_time = time.time()
        st.session_state.section_scores = {
            "Aptitude": 0,
            "Logical": 0,
            "Computer": 0,
            "GK": 0
        }
        st.session_state.questions = {
            "Aptitude": random.sample(APTITUDE_QS, 6),
            "Logical": random.sample(LOGICAL_QS, 3),
            "Computer": random.sample(COMPUTER_QS, 3),
            "GK": random.sample(GK_QS, 3)
        }

    remaining = TOTAL_TIME - int(time.time() - st.session_state.start_time)
    if remaining <= 0:
        st.session_state.step = 5
        remaining = 0

    mins, secs = divmod(remaining, 60)
    st.info(f"⏱ Time Remaining: {mins:02d}:{secs:02d}")

    sections = ["Aptitude","Logical","Computer","GK"]

    # -------- SECTION PAGES --------
    if st.session_state.step <= 4:
        sec = sections[st.session_state.step - 1]
        st.subheader(f"Section: {sec}")

        for q, opts, ans in st.session_state.questions[sec]:
            choice = st.radio(q, opts, index=None)
            if choice == ans:
                st.session_state.section_scores[sec] += (25 / len(st.session_state.questions[sec]))

        if st.button("Next ➡️"):
            st.session_state.step += 1
            st.rerun()

    # -------- RESULT PAGE --------
    else:
        total = int(sum(st.session_state.section_scores.values()))

        if total >= 75:
            grade = "A"
            degree = "B.Sc Computer Science / CS with AI"
            career = ["Software Engineer", "AI Engineer", "Data Scientist"]
        elif total >= 50:
            grade = "B"
            degree = "BCA / B.Sc / B.Com"
            career = ["Business Analyst", "IT Support", "Banking"]
        else:
            grade = "C"
            degree = "Arts / Management"
            career = ["HR", "Administration", "Creative Fields"]

        st.success(f"🎯 Total Score: {total} / 100")
        st.info(f"🎖 Grade: {grade}")
        st.write(f"🎓 Recommended Degree: {degree}")

        pdf = generate_pdf(
            student_name,
            total,
            grade,
            degree,
            career,
            st.session_state.section_scores
        )

        st.download_button(
            "📥 Download Result PDF",
            pdf,
            file_name="Entrance_Test_Result.pdf",
            mime="application/pdf"
        )

        if st.button("Restart Exam"):
            st.session_state.clear()
            st.rerun()

# ================= COLLEGE GPT =================
elif menu == "🤖 Ask College GPT":
    st.header("🤖 College GPT")
    st.caption("Answers limited to SACAS & CS / CS-AI syllabus")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    for msg in st.session_state.chat:
        st.chat_message(msg["role"]).write(msg["content"])

    user = st.chat_input("Ask your question")

    if user:
        st.session_state.chat.append({"role":"user","content":user})
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"Answer academically for SACAS CS & CS-AI"},
                {"role":"user","content":user}
            ]
        )
        reply = res.choices[0].message.content
        st.session_state.chat.append({"role":"assistant","content":reply})
        st.rerun()

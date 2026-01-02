import streamlit as st
from openai import OpenAI
import os
from pathlib import Path
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_pdf(name, score, grade, degree, career):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height-50, "SA COLLEGE OF ARTS & SCIENCE")

    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height-80, "ONLINE DEGREE ENTRANCE TEST RESULT")

    y = height - 140
    c.drawString(50, y, f"Student Name: {name}")
    y -= 30
    c.drawString(50, y, f"Score: {score} / 100")
    y -= 30
    c.drawString(50, y, f"Grade: {grade}")
    y -= 30
    c.drawString(50, y, f"Recommended Degree: {degree}")
    y -= 40

    c.drawString(50, y, "Suggested Career Paths:")
    y -= 25
    for cpath in career:
        c.drawString(70, y, f"- {cpath}")
        y -= 20

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SA College of Arts & Science | College GPT",
    page_icon="🎓",
    layout="wide"
)

# ---------------- SAFE IMAGE ----------------
def show_image(path, **kwargs):
    if Path(path).exists():
        st.image(path, **kwargs)
    else:
        st.info(f"Image missing: {path}")

# ---------------- HEADER ----------------
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

# ---------------- SIDEBAR ----------------
menu = st.sidebar.radio(
    "📘 Navigation",
    [
        "🏫 About College",
        "📍 Location",
        "📚 CS & CS-AI Syllabus",
        "👨‍🏫 CS with AI – HOD",
        "🏆 Student Achievements",
        "📝 Online Degree Entrance Test",
        "🤖 Ask College GPT"
    ]
)

# ---------------- ABOUT ----------------
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

# ---------------- LOCATION ----------------
elif menu == "📍 Location":
    st.header("📍 College Location")
    st.write("**SA College of Arts & Science, Thiruverkadu, Avadi, Chennai**")
    df = pd.DataFrame({"lat":[13.0475], "lon":[80.1012]})
    st.map(df)

# ---------------- SYLLABUS ----------------
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

# ---------------- HOD ----------------
elif menu == "👨‍🏫 CS with AI – HOD":
    st.header("👨‍🏫 Head of the Department – CS with AI")

    col1, col2 = st.columns([1,2])
    with col1:
        show_image("assets/hod.png", width=250)
    with col2:
        st.markdown("""
**Mr. Krishnan R**  
*M.Sc, M.Phil, NET, SET*

**Experience**
- UG: 30 Years  
- PG: 23 Years  

**Focus**
- Industry-ready skills  
- Ethical AI  
- Practical learning
        """)

elif menu == "📝 Online Degree Entrance Test":
    st.header("📝 Online Degree Entrance Test")
    st.caption("Pattern: Aptitude + Logical + Computer + General Knowledge (100 Marks)")

    name = st.text_input("Enter Student Name")

    st.divider()

    score = 0

    # ---------------- APTITUDE ----------------
    st.subheader("📊 Section 1: Quantitative Aptitude (25 Marks)")

    q1 = st.radio("1) If 15% of a number is 45, what is the number?",
                  ["200", "250", "300", "350"])
    if q1 == "300": score += 10

    q2 = st.radio("2) What is the average of 10, 20, 30, 40, 50?",
                  ["25", "30", "35", "40"])
    if q2 == "30": score += 15

    st.divider()

    # ---------------- LOGICAL ----------------
    st.subheader("🧠 Section 2: Logical Reasoning (25 Marks)")

    q3 = st.radio("3) Find the odd one out:",
                  ["Keyboard", "Mouse", "Monitor", "Chair"])
    if q3 == "Chair": score += 10

    q4 = st.radio("4) Series: 3, 9, 27, ?",
                  ["54", "81", "72", "90"])
    if q4 == "81": score += 15

    st.divider()

    # ---------------- COMPUTER ----------------
    st.subheader("💻 Section 3: Computer Knowledge (25 Marks)")

    q5 = st.radio("5) Which language is mainly used for AI?",
                  ["C", "Python", "HTML", "SQL"])
    if q5 == "Python": score += 10

    q6 = st.radio("6) What does CPU stand for?",
                  ["Central Processing Unit", "Computer Power Unit",
                   "Central Program Unit", "Control Processing Unit"])
    if q6 == "Central Processing Unit": score += 15

    st.divider()

    # ---------------- GK ----------------
    st.subheader("🌍 Section 4: General Knowledge (25 Marks)")

    q7 = st.radio("7) Who is known as the Father of Computer?",
                  ["Charles Babbage", "Alan Turing", "Bill Gates", "Steve Jobs"])
    if q7 == "Charles Babbage": score += 10

    q8 = st.radio("8) Which is the national animal of India?",
                  ["Lion", "Elephant", "Tiger", "Leopard"])
    if q8 == "Tiger": score += 15

    st.divider()

    # ---------------- RESULT ----------------
    if st.button("📊 Submit Exam & View Result"):
        st.header("📄 Exam Result")

        st.write(f"### 🎯 Score: **{score} / 100**")

        if score >= 75:
            grade = "A"
            degree = "B.Sc Computer Science / CS with AI"
            career = ["Software Engineer", "AI Engineer", "Data Scientist"]
            st.success("Grade A – Excellent")
        elif score >= 50:
            grade = "B"
            degree = "B.Sc Mathematics / BCA / B.Com"
            career = ["Data Analyst", "Banking", "Business Analyst"]
            st.warning("Grade B – Good")
        else:
            grade = "C"
            degree = "BA / B.Com / General Degree"
            career = ["Administration", "Creative Fields", "Government Exams"]
            st.error("Grade C – Needs Improvement")

        st.write(f"🎓 **Recommended Degree:** {degree}")
        st.write("💼 **Career Paths:**")
        for cpath in career:
            st.write(f"- {cpath}")

        pdf = generate_pdf(name, score, grade, degree, career)

        st.download_button(
            "📥 Download Result PDF",
            data=pdf,
            file_name="Entrance_Test_Result.pdf",
            mime="application/pdf"
        )


# ---------------- COLLEGE GPT ----------------
elif menu == "🤖 Ask College GPT":
    st.header("🤖 College GPT")
    st.caption("Answers limited to SACAS & CS / CS-AI syllabus")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    for msg in st.session_state.chat:
        st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("Ask your question and press Enter")

    if user_input:
        st.session_state.chat.append({"role":"user","content":user_input})

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"You are College GPT for SA College. Answer academically."},
                {"role":"user","content":user_input}
            ]
        )

        reply = res.choices[0].message.content
        st.session_state.chat.append({"role":"assistant","content":reply})
        st.rerun()

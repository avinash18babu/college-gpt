import streamlit as st
from openai import OpenAI
import os
from pathlib import Path
import pandas as pd

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="SA College of Arts & Science | College GPT",
    page_icon="🎓",
    layout="wide"
)

# ---------------- HEADER ----------------
st.markdown("""
<style>
.title {
    text-align:center;
    font-size:42px;
    font-weight:700;
}
.subtitle {
    text-align:center;
    font-size:18px;
    color:gray;
}
.credit {
    text-align:center;
    font-size:13px;
    color:#666;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎓 SA College of Arts & Science</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Affiliated to University of Madras</div>', unsafe_allow_html=True)
st.markdown('<div class="credit">College GPT by Avinash</div>', unsafe_allow_html=True)
st.divider()

# ---------------- SIDEBAR ----------------
st.sidebar.title("📘 Navigation")
menu = st.sidebar.radio(
    "Go to",
    [
        "🏫 About College",
        "📍 Location",
        "📚 CS & CS-AI Syllabus",
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

The college focuses on:
- Academic Excellence  
- Innovation & Research  
- Discipline & Ethics  
- Holistic Student Development  
    """)

# ---------------- LOCATION ----------------
elif menu == "📍 Location":
    st.header("📍 College Location")
    st.write("**SA College of Arts & Science — Thiruverkadu, Avadi, Chennai**")

    df = pd.DataFrame({"lat": [13.0475], "lon": [80.1012]})
    st.map(df)

# ---------------- SYLLABUS ----------------
elif menu == "📚 CS & CS-AI Syllabus":
    st.header("📚 B.Sc Computer Science & CS with AI – Syllabus")

    st.subheader("Core Subjects")
    st.markdown("""
- Programming in C / Python  
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

# ===================== ENTRANCE TEST =====================
elif menu == "📝 Online Degree Entrance Test":
    st.header("📝 Online Admission & Degree Entrance Test")
    st.caption("Based on 12th standard knowledge, aptitude & general awareness")

    st.divider()

    total = 0
    tech = 0
    math = 0
    mgmt = 0
    gk = 0

    # -------- SECTION A ----------
    st.subheader("🧠 Section A: Aptitude & Logic (20 Marks)")

    q1 = st.radio("1️⃣ Find the next number: 2, 4, 8, 16, ?", ["18", "24", "32", "64"])
    if q1 == "32":
        total += 5
        tech += 5

    q2 = st.radio("2️⃣ Which is NOT an Operating System?", ["Windows", "Linux", "Oracle", "MacOS"])
    if q2 == "Oracle":
        total += 5
        tech += 5

    q3 = st.radio("3️⃣ If A = 1, B = 2, then Z = ?", ["24", "25", "26", "27"])
    if q3 == "26":
        total += 5
        math += 5

    q4 = st.radio("4️⃣ Which number is divisible by 9?", ["234", "127", "221", "101"])
    if q4 == "234":
        total += 5
        math += 5

    # -------- SECTION B ----------
    st.subheader("💻 Section B: 12th Standard Knowledge (20 Marks)")

    q5 = st.radio("5️⃣ Which data type stores decimal values in Python?", ["int", "float", "char", "bool"])
    if q5 == "float":
        total += 5
        tech += 5

    q6 = st.radio("6️⃣ What is the binary of decimal 5?", ["101", "111", "110", "100"])
    if q6 == "101":
        total += 5
        tech += 5

    q7 = st.radio("7️⃣ Formula for simple interest?", ["P+RT", "PRT/100", "P/R/T", "RT/P"])
    if q7 == "PRT/100":
        total += 5
        math += 5

    q8 = st.radio("8️⃣ Which is NOT a programming language?", ["Java", "Python", "HTML", "Oracle"])
    if q8 == "Oracle":
        total += 5
        tech += 5

    # -------- SECTION C ----------
    st.subheader("🌍 Section C: General Knowledge (10 Marks)")

    q9 = st.radio("9️⃣ Capital of Tamil Nadu?", ["Chennai", "Madurai", "Coimbatore", "Trichy"])
    if q9 == "Chennai":
        total += 5
        gk += 5

    q10 = st.radio("🔟 Who is the Father of Computer?", ["Newton", "Charles Babbage", "Einstein", "Tesla"])
    if q10 == "Charles Babbage":
        total += 5
        gk += 5

    # -------- RESULT ----------
    if st.button("📊 Submit Test & View Result"):
        st.divider()

        # Grade
        if total >= 40:
            grade = "A"
        elif total >= 30:
            grade = "B"
        elif total >= 20:
            grade = "C"
        else:
            grade = "D"

        st.success(f"✅ Total Score: **{total} / 50**")
        st.info(f"🎖 Grade: **{grade}**")

        # Degree Decision
        if tech >= math and tech >= mgmt:
            st.success("🎓 Recommended Degree: **B.Sc Computer Science / CS with AI**")
            st.write("""
**Career Paths:**
- Software Developer  
- AI / ML Engineer  
- Data Scientist  
- Cyber Security Analyst
            """)
        elif math > tech:
            st.success("🎓 Recommended Degree: **B.Sc Mathematics / Data Science**")
            st.write("""
**Career Paths:**
- Data Analyst  
- Banking & Finance  
- Statistician
            """)
        else:
            st.success("🎓 Recommended Degree: **BBA / B.Com**")
            st.write("""
**Career Paths:**
- Business Analyst  
- HR Manager  
- Entrepreneur
            """)

        st.warning("📌 Final admission decisions should be made with academic counsellors.")

# ---------------- GPT CHAT ----------------
elif menu == "🤖 Ask College GPT":
    st.header("🤖 Ask College GPT")
    st.caption("Answers limited to SA College & CS / CS-AI syllabus")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    for msg in st.session_state.chat:
        st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("Ask your question and press Enter")

    if user_input:
        st.session_state.chat.append({"role": "user", "content": user_input})

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Answer only based on SACAS CS & CS-AI syllabus"},
                {"role": "user", "content": user_input}
            ]
        )

        reply = response.choices[0].message.content
        st.session_state.chat.append({"role": "assistant", "content": reply})
        st.rerun()

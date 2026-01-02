import streamlit as st
from openai import OpenAI
import os
from pathlib import Path
import pandas as pd

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

# ---------------- ACHIEVEMENTS ----------------
elif menu == "🏆 Student Achievements":
    st.header("🏆 Student Achievements – CS with AI")
    show_image("assets/ai_achievements.png", use_column_width=True)

# ---------------- ENTRANCE TEST ----------------
elif menu == "📝 Online Degree Entrance Test":
    st.header("📝 Online Degree Entrance Test")
    st.caption("Pattern similar to TCS / AMCAT | Total: 100 Marks")

    if "step" not in st.session_state:
        st.session_state.step = 1
        st.session_state.score = 0

    # -------- APTITUDE --------
    if st.session_state.step == 1:
        st.subheader("📊 Quantitative Aptitude")
        q1 = st.radio("20% of 200 =", ["20","40","60","80"])
        q2 = st.radio("5² =", ["10","20","25","30"])

        if st.button("Next"):
            if q1=="40": st.session_state.score+=10
            if q2=="25": st.session_state.score+=10
            st.session_state.step=2
            st.rerun()

    # -------- LOGIC --------
    elif st.session_state.step == 2:
        st.subheader("🧠 Logical Reasoning")
        q1 = st.radio("Odd one out", ["Apple","Banana","Car","Mango"])
        q2 = st.radio("Series: 2,4,8,?", ["12","14","16","18"])

        if st.button("Next"):
            if q1=="Car": st.session_state.score+=10
            if q2=="16": st.session_state.score+=10
            st.session_state.step=3
            st.rerun()

    # -------- COMPUTER --------
    elif st.session_state.step == 3:
        st.subheader("💻 Computer Basics")
        q1 = st.radio("CPU stands for?", ["Central Processing Unit","Control Unit"])
        q2 = st.radio("Binary uses?", ["0 & 1","1 & 2"])

        if st.button("Submit Test"):
            if q1=="Central Processing Unit": st.session_state.score+=10
            if q2=="0 & 1": st.session_state.score+=10
            st.session_state.step=4
            st.rerun()

    # -------- RESULT --------
    elif st.session_state.step == 4:
        st.header("📄 Result")
        score = st.session_state.score
        st.write(f"### 🎯 Score: **{score}/100**")

        if score >= 60:
            st.success("🎓 Recommended Degree: **B.Sc CS / CS with AI**")
            st.write("""
**Career Paths**
- Software Engineer  
- AI Engineer  
- Data Scientist  
            """)
        else:
            st.info("🎓 Recommended Degree: **Arts / Commerce / Management**")

        if st.button("Restart"):
            st.session_state.clear()
            st.rerun()

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

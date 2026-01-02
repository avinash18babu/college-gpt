import streamlit as st
from openai import OpenAI
import os
from pathlib import Path
import pandas as pd

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="SA College of Arts & Science | CS with AI",
    page_icon="🎓",
    layout="wide"
)

# ---------------- SAFE IMAGE FUNCTION ----------------
def show_image(path, **kwargs):
    if Path(path).exists():
        st.image(path, **kwargs)
    else:
        st.warning(f"Image not found: {path}")

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
    animation: fade 2s infinite alternate;
}
@keyframes fade {
    from {opacity:0.6;}
    to {opacity:1;}
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
        "🎯 Vision & Mission",
        "🏢 Departments",
        "🎉 Events & Activities",
        "📍 Location",
        "📚 CS & CS-AI Syllabus",
        "👨‍🏫 CS with AI – HOD",
        "🏆 Student Achievements",
        "🎓 Career Counselling",
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
    show_image("assets/ai_students.png", use_column_width=True)

# ---------------- VISION ----------------
elif menu == "🎯 Vision & Mission":
    st.header("🎯 Vision & Mission")
    st.success("**Vision:** To empower students with knowledge, skills, and ethical values.")
    st.info("**Mission:** To provide quality education with industry readiness and social responsibility.")

# ---------------- DEPARTMENTS ----------------
elif menu == "🏢 Departments":
    st.header("🏢 Departments")
    st.markdown("""
- Computer Science  
- Computer Science with Artificial Intelligence  
- Commerce  
- Management Studies  
- Mathematics  
- English  
- Physics  
- Chemistry  
    """)

# ---------------- EVENTS ----------------
elif menu == "🎉 Events & Activities":
    st.header("🎉 CS with AI – Events & Activities")
    st.write("Freshers Day, Technical Events, Cultural Programs & Workshops")
    show_image("assets/event.png", caption="Freshers Day – CS with AI", use_column_width=True)

# ---------------- LOCATION ----------------
elif menu == "📍 Location":
    st.header("📍 College Location")
    st.write("**SA College of Arts & Science** — Thiruverkadu, Avadi, Chennai")

    df = pd.DataFrame({
        "lat": [13.0475],
        "lon": [80.1012]
    })
    st.map(df)

# ---------------- SYLLABUS ----------------
elif menu == "📚 CS & CS-AI Syllabus":
    st.header("📚 B.Sc Computer Science & CS with AI – Syllabus")

    st.markdown("""
### Core Subjects
- Programming in C / Python  
- Data Structures  
- DBMS  
- Operating Systems  
- Computer Networks  

### AI Specialization
- Artificial Intelligence  
- Machine Learning  
- Deep Learning  
- NLP  
- Computer Vision  

*(University of Madras – Arts & Science Pattern)*  
    """)

# ---------------- HOD ----------------
elif menu == "👨‍🏫 CS with AI – HOD":
    st.header("👨‍🏫 Head of the Department – CS with AI")

    col1, col2 = st.columns([1, 2])

    with col1:
        show_image("assets/hod.png", width=250)

    with col2:
        st.markdown("""
**Mr. Krishnan R**  
Head of the Department – CS with AI  

**Qualifications:**  
M.Sc, M.Phil, NET, SET  

**Experience:**  
- UG: 30 Years  
- PG: 23 Years  

**Focus Areas:**  
Industry-ready skills, ethical AI, innovation, hands-on learning
        """)

# ---------------- ACHIEVEMENTS ----------------
elif menu == "🏆 Student Achievements":
    st.header("🏆 Student Achievements – CS with AI")
    show_image("assets/ai_achievements.png", use_column_width=True)

# ---------------- CAREER COUNSELLING ----------------
elif menu == "🎓 Career Counselling":
    st.header("🎓 AI-Based Career Counselling")

    q1 = st.radio("What do you enjoy most?", ["Logic", "Creativity", "Management", "Numbers"])
    q2 = st.radio("Preferred work style?", ["Technology", "People", "Data", "Design"])

    if st.button("🔍 Get Recommendation"):
        if q1 == "Logic" and q2 == "Technology":
            st.success("✅ Best Degree: **B.Sc CS / CS with AI**")
            st.write("Careers: Software Developer, AI Engineer, Data Scientist")
        elif q1 == "Numbers":
            st.success("✅ Best Degree: **B.Sc Mathematics / Data Science**")
        elif q2 == "People":
            st.success("✅ Best Degree: **BBA / B.Com**")
        else:
            st.success("✅ Best Degree: **Visual Communication / Design**")

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

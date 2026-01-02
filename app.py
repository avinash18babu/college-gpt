import streamlit as st
from openai import OpenAI
import os
from pathlib import Path
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SA College of Arts & Science | CS with AI",
    page_icon="🎓",
    layout="wide"
)

# ---------------- IMAGE SAFE LOADER ----------------
def show_image(path, **kwargs):
    if Path(path).exists():
        st.image(path, **kwargs)
    else:
        st.error(f"❌ Image missing: {path}")

# ---------------- HEADER ----------------
st.markdown("""
<style>
.title {
    text-align:center;
    font-size:40px;
    font-weight:700;
}
.subtitle {
    text-align:center;
    font-size:18px;
    color:#666;
}
.credit {
    text-align:center;
    font-size:13px;
    color:#888;
}
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
        "🏢 Departments",
        "📚 CS & CS-AI Syllabus",
        "👨‍🏫 CS with AI – HOD",
        "🏆 Student Achievements",
        "🎉 Events & Activities",
        "📝 Online Degree Entrance Test",
        "🤖 Ask College GPT"
    ]
)

# ---------------- ABOUT COLLEGE ----------------
if menu == "🏫 About College":
    st.header("🏫 About SA College of Arts & Science")

    st.write("""
SA College of Arts & Science (SACAS) is a reputed Arts & Science institution
located in **Thiruverkadu, Avadi, Chennai**.

The institution focuses on:
- Academic Excellence
- Innovation & Research
- Discipline & Ethics
- Holistic Student Development
""")

    show_image("assets/ai_students.png", use_column_width=True)

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

# ---------------- SYLLABUS ----------------
elif menu == "📚 CS & CS-AI Syllabus":
    st.header("📚 B.Sc Computer Science & CS with AI")

    st.subheader("Core Subjects")
    st.markdown("""
- Programming in C / Python  
- Data Structures  
- Database Management Systems  
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

    st.caption("📘 As per University of Madras syllabus")

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

**Department Focus:**  
Industry-ready skills, ethical AI, innovation, hands-on learning.
""")

# ---------------- ACHIEVEMENTS ----------------
elif menu == "🏆 Student Achievements":
    st.header("🏆 Student Achievements – CS with AI")
    show_image("assets/ai_achievements.png", use_column_width=True)

# ---------------- EVENTS ----------------
elif menu == "🎉 Events & Activities":
    st.header("🎉 Department Events")
    st.write("Freshers Day, Technical Workshops, Cultural Programs")
    show_image("assets/event.png", use_column_width=True)

# ---------------- ENTRANCE TEST ----------------
elif menu == "📝 Online Degree Entrance Test":
    st.header("📝 Online Degree Entrance Test")
    st.caption("Based on 12th standard + aptitude + general knowledge")

    score = 0

    q1 = st.radio("1️⃣ What is the output of 2 + 3 * 4 ?", ["14", "20", "24", "10"])
    if q1 == "14": score += 10

    q2 = st.radio("2️⃣ Which subject is required for Computer Science?", ["Biology", "Computer Science", "History", "Geography"])
    if q2 == "Computer Science": score += 10

    q3 = st.radio("3️⃣ What does AI stand for?", ["Artificial Intelligence", "Automated Input", "Advanced Internet", "Applied Interface"])
    if q3 == "Artificial Intelligence": score += 10

    q4 = st.radio("4️⃣ Which career needs strong logic?", ["Software Engineer", "Journalist", "Actor", "Designer"])
    if q4 == "Software Engineer": score += 10

    q5 = st.radio("5️⃣ Do you enjoy problem solving?", ["Yes", "No"])
    if q5 == "Yes": score += 10

    if st.button("📊 Submit Test"):
        st.divider()
        st.write(f"### 🎯 Total Score: **{score} / 50**")

        if score >= 40:
            st.success("🎓 Recommended Degree: **B.Sc CS / CS with AI**")
            st.write("Career Paths: Software Engineer, AI Engineer, Data Scientist")
        elif score >= 25:
            st.warning("🎓 Recommended Degree: **B.Sc / BCA / B.Com**")
            st.write("Career Paths: Analyst, Banking, IT Support")
        else:
            st.info("🎓 Recommended Degree: **Arts / Management**")
            st.write("Career Paths: Media, HR, Administration")

# ---------------- GPT CHAT ----------------
elif menu == "🤖 Ask College GPT":
    st.header("🤖 Ask College GPT")
    st.caption("Limited to SACAS & CS / CS-AI syllabus")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    for msg in st.session_state.chat:
        st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("Type your question and press Enter")

    if user_input:
        st.session_state.chat.append({"role": "user", "content": user_input})

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Answer only based on SACAS CS & CS-AI syllabus"},
                {"role": "user", "content": user_input}
            ]
        )

        reply = res.choices[0].message.content
        st.session_state.chat.append({"role": "assistant", "content": reply})
        st.rerun()

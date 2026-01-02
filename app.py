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
.title { text-align:center; font-size:42px; font-weight:700; }
.subtitle { text-align:center; font-size:18px; color:gray; }
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
        "📝 Degree Aptitude Test",
        "🤖 Ask College GPT"
    ]
)

# ---------------- ABOUT ----------------
if menu == "🏫 About College":
    st.header("🏫 About SA College of Arts & Science")
    st.write("""
SA College of Arts & Science (SACAS) is located in **Thiruverkadu, Avadi, Chennai**.

• Academic Excellence  
• Innovation & Research  
• Discipline & Ethics  
• Holistic Student Development  
    """)
    show_image("assets/ai_students.png", use_column_width=True)

# ---------------- VISION ----------------
elif menu == "🎯 Vision & Mission":
    st.header("🎯 Vision & Mission")
    st.success("**Vision:** To empower students with knowledge and ethics.")
    st.info("**Mission:** To provide quality education with industry readiness.")

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
    st.header("🎉 CS with AI – Events")
    show_image("assets/event.png", caption="Freshers Day – CS with AI", use_column_width=True)

# ---------------- LOCATION ----------------
elif menu == "📍 Location":
    st.header("📍 College Location")
    st.write("SA College of Arts & Science — Thiruverkadu, Avadi, Chennai")

    df = pd.DataFrame({"lat": [13.0475], "lon": [80.1012]})
    st.map(df)

# ---------------- SYLLABUS ----------------
elif menu == "📚 CS & CS-AI Syllabus":
    st.header("📚 CS & CS-AI Syllabus")
    st.markdown("""
**Core Subjects**
- C / Python  
- Data Structures  
- DBMS  
- OS  
- Computer Networks  

**AI Specialization**
- AI  
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
M.Sc, M.Phil, NET, SET  

UG: 30 Years  
PG: 23 Years  

Focus: Industry-ready skills & ethical AI
        """)

# ---------------- ACHIEVEMENTS ----------------
elif menu == "🏆 Student Achievements":
    st.header("🏆 Student Achievements – CS with AI")
    show_image("assets/ai_achievements.png", use_column_width=True)

# ---------------- DEGREE APTITUDE TEST ----------------
elif menu == "📝 Degree Aptitude Test":
    st.header("📝 Online Degree Aptitude Test")
    st.write("Find the best degree based on aptitude.")

    score = {"CS":0, "Math":0, "Mgmt":0, "Creative":0}

    q1 = st.radio("What do you enjoy?", ["Logic", "Numbers", "People", "Creativity"])
    q2 = st.radio("Preferred work?", ["Technology", "Data", "Management", "Design"])

    score["CS"] += 3 if q1=="Logic" else 0
    score["Math"] += 3 if q1=="Numbers" else 0
    score["Mgmt"] += 3 if q1=="People" else 0
    score["Creative"] += 3 if q1=="Creativity" else 0

    score["CS"] += 3 if q2=="Technology" else 0
    score["Math"] += 3 if q2=="Data" else 0
    score["Mgmt"] += 3 if q2=="Management" else 0
    score["Creative"] += 3 if q2=="Design" else 0

    if st.button("📊 Get Result"):
        best = max(score, key=score.get)
        if best=="CS":
            st.success("🎓 B.Sc Computer Science / CS with AI")
        elif best=="Math":
            st.success("🎓 B.Sc Mathematics / Data Science")
        elif best=="Mgmt":
            st.success("🎓 BBA / B.Com")
        else:
            st.success("🎓 Visual Communication / Design")

# ---------------- GPT ----------------
elif menu == "🤖 Ask College GPT":
    st.header("🤖 Ask College GPT")

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
                {"role":"system","content":"Answer only SACAS CS & CS-AI syllabus"},
                {"role":"user","content":user}
            ]
        )
        reply = res.choices[0].message.content
        st.session_state.chat.append({"role":"assistant","content":reply})
        st.rerun()

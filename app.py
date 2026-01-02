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
elif menu == "📝 Degree Aptitude Test":
    st.header("📝 Online Degree Aptitude Test")
    st.write(
        "This entry-level aptitude test helps students identify the "
        "**most suitable degree programme** based on skills and interests."
    )

    st.divider()

    # Initialize scores
    score_cs = 0
    score_math = 0
    score_mgmt = 0
    score_creative = 0

    # ---------------- QUESTION 1 ----------------
    q1 = st.radio(
        "1️⃣ What type of task do you enjoy the most?",
        [
            "Solving logical or coding problems",
            "Working with numbers and calculations",
            "Managing people or organizing work",
            "Designing, drawing, or creative work"
        ]
    )

    if q1 == "Solving logical or coding problems":
        score_cs += 3
    elif q1 == "Working with numbers and calculations":
        score_math += 3
    elif q1 == "Managing people or organizing work":
        score_mgmt += 3
    else:
        score_creative += 3

    # ---------------- QUESTION 2 ----------------
    q2 = st.radio(
        "2️⃣ Which subject do you like the most?",
        [
            "Computer Science",
            "Mathematics",
            "Business Studies",
            "Arts / Media"
        ]
    )

    if q2 == "Computer Science":
        score_cs += 3
    elif q2 == "Mathematics":
        score_math += 3
    elif q2 == "Business Studies":
        score_mgmt += 3
    else:
        score_creative += 3

    # ---------------- QUESTION 3 ----------------
    q3 = st.radio(
        "3️⃣ How do you prefer to work?",
        [
            "With technology and systems",
            "With data and analysis",
            "With people and communication",
            "With creativity and imagination"
        ]
    )

    if q3 == "With technology and systems":
        score_cs += 3
    elif q3 == "With data and analysis":
        score_math += 3
    elif q3 == "With people and communication":
        score_mgmt += 3
    else:
        score_creative += 3

    # ---------------- QUESTION 4 ----------------
    q4 = st.radio(
        "4️⃣ What is your long-term career goal?",
        [
            "Software / IT job",
            "Banking / Analytics / Research",
            "Business / Management",
            "Media / Design / Creative field"
        ]
    )

    if q4 == "Software / IT job":
        score_cs += 3
    elif q4 == "Banking / Analytics / Research":
        score_math += 3
    elif q4 == "Business / Management":
        score_mgmt += 3
    else:
        score_creative += 3

    # ---------------- SUBMIT ----------------
    if st.button("📊 Submit Test & Get Result"):
        st.divider()

        scores = {
            "CS": score_cs,
            "Math": score_math,
            "Management": score_mgmt,
            "Creative": score_creative
        }

        best = max(scores, key=scores.get)

        # ---------------- RESULT ----------------
        if best == "CS":
            st.success("🎓 Recommended Degree: **B.Sc Computer Science / CS with AI**")
            st.write("""
**Suggested Career Paths:**
- Software Developer  
- AI / Machine Learning Engineer  
- Data Scientist  
- Cyber Security Analyst  

**Reason:**  
You have strong logical thinking and interest in technology.
            """)

        elif best == "Math":
            st.success("🎓 Recommended Degree: **B.Sc Mathematics / Data Science**")
            st.write("""
**Suggested Career Paths:**
- Data Analyst  
- Statistician  
- Banking & Finance  
- Research Analyst  

**Reason:**  
You are good at numbers, data analysis, and problem-solving.
            """)

        elif best == "Management":
            st.success("🎓 Recommended Degree: **BBA / B.Com**")
            st.write("""
**Suggested Career Paths:**
- Business Analyst  
- HR Manager  
- Marketing Executive  
- Entrepreneur  

**Reason:**  
You have leadership qualities and strong communication skills.
            """)

        else:
            st.success("🎓 Recommended Degree: **Visual Communication / Design / Arts**")
            st.write("""
**Suggested Career Paths:**
- Graphic Designer  
- Media & Film Industry  
- Content Creator  
- UX / UI Designer  

**Reason:**  
You are creative and expressive with ideas.
            """)

        st.info(
            "📌 *This result is based on aptitude analysis. "
            "Final decisions should be made with academic counsellors.*"
        )

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

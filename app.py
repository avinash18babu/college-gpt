import streamlit as st
from pathlib import Path
import pandas as pd

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="SA College of Arts & Science | Degree Entrance Test",
    page_icon="🎓",
    layout="wide"
)

# ---------------- IMAGE SAFE ----------------
def show_image(path, **kwargs):
    if Path(path).exists():
        st.image(path, **kwargs)

# ---------------- HEADER ----------------
st.markdown("""
<style>
.title {text-align:center;font-size:38px;font-weight:700;}
.subtitle {text-align:center;font-size:17px;color:gray;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎓 SA College of Arts & Science</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-Based Online Degree Entrance Test</div>', unsafe_allow_html=True)
st.divider()

# ---------------- SIDEBAR ----------------
menu = st.sidebar.radio(
    "📘 Navigation",
    [
        "🏫 About College",
        "👨‍🏫 CS with AI – HOD",
        "📝 Online Degree Entrance Test",
        "🏆 Student Achievements"
    ]
)

# ---------------- ABOUT ----------------
if menu == "🏫 About College":
    st.header("🏫 About SA College of Arts & Science")
    st.write("""
SA College of Arts & Science (SACAS) is a reputed institution in  
**Thiruverkadu, Avadi, Chennai**, affiliated to the **University of Madras**.

The college emphasizes:
- Academic excellence
- Industry-ready education
- Ethical and professional development
""")
    show_image("assets/ai_students.png", use_column_width=True)

# ---------------- HOD ----------------
elif menu == "👨‍🏫 CS with AI – HOD":
    st.header("👨‍🏫 Head of the Department – CS with AI")
    col1, col2 = st.columns([1, 2])
    with col1:
        show_image("assets/hod.png", width=250)
    with col2:
        st.markdown("""
**Mr. Krishnan R**  
M.Sc, M.Phil, NET, SET  

**Experience:**  
- UG: 30 Years  
- PG: 23 Years  

**Focus:**  
Artificial Intelligence, Industry skills, Ethical Computing
""")

# ---------------- ENTRANCE TEST ----------------
elif menu == "📝 Online Degree Entrance Test":
    st.header("📝 Online Degree Entrance Test")
    st.caption("Pattern similar to TCS / AMCAT | Total Marks: 100")

    if "page" not in st.session_state:
        st.session_state.page = 1
        st.session_state.score = 0

    # ---------- SECTION 1 ----------
    if st.session_state.page == 1:
        st.subheader("📊 Section 1: Quantitative Aptitude (25 Marks)")

        q1 = st.radio("1. 20% of 150 =", ["20", "30", "40", "50"])
        q2 = st.radio("2. If x = 5, value of x² =", ["10", "15", "25", "30"])
        q3 = st.radio("3. Average of 2,4,6,8 =", ["4", "5", "6", "7"])
        q4 = st.radio("4. 12 × 8 =", ["96", "88", "84", "72"])
        q5 = st.radio("5. Simple Interest formula?", ["P×R×T/100", "P+RT", "P×T", "PR/T"])

        if st.button("Next ➡️"):
            if q1 == "30": st.session_state.score += 5
            if q2 == "25": st.session_state.score += 5
            if q3 == "5": st.session_state.score += 5
            if q4 == "96": st.session_state.score += 5
            if q5 == "P×R×T/100": st.session_state.score += 5
            st.session_state.page = 2
            st.rerun()

    # ---------- SECTION 2 ----------
    elif st.session_state.page == 2:
        st.subheader("🧠 Section 2: Logical Reasoning (25 Marks)")

        q1 = st.radio("6. Find the odd one: Dog, Cat, Cow, Car", ["Dog", "Cat", "Cow", "Car"])
        q2 = st.radio("7. Series: 2, 4, 8, ?", ["10", "12", "16", "18"])
        q3 = st.radio("8. All roses are flowers. Some flowers fade. Statement implies?", ["True", "False"])
        q4 = st.radio("9. Clock shows 3:00 – angle?", ["90°", "60°", "120°", "180°"])
        q5 = st.radio("10. If A>B and B>C, then?", ["A>C", "A<C"])

        if st.button("Next ➡️"):
            if q1 == "Car": st.session_state.score += 5
            if q2 == "16": st.session_state.score += 5
            if q3 == "True": st.session_state.score += 5
            if q4 == "90°": st.session_state.score += 5
            if q5 == "A>C": st.session_state.score += 5
            st.session_state.page = 3
            st.rerun()

    # ---------- SECTION 3 ----------
    elif st.session_state.page == 3:
        st.subheader("💻 Section 3: Computer & Science Basics (25 Marks)")

        q1 = st.radio("11. CPU stands for?", ["Central Processing Unit", "Control Unit"])
        q2 = st.radio("12. Binary system uses?", ["0 & 1", "1 & 2", "2 & 3"])
        q3 = st.radio("13. Which is an input device?", ["Monitor", "Keyboard"])
        q4 = st.radio("14. AI means?", ["Artificial Intelligence", "Automated Internet"])
        q5 = st.radio("15. RAM is?", ["Temporary memory", "Permanent memory"])

        if st.button("Next ➡️"):
            if q1 == "Central Processing Unit": st.session_state.score += 5
            if q2 == "0 & 1": st.session_state.score += 5
            if q3 == "Keyboard": st.session_state.score += 5
            if q4 == "Artificial Intelligence": st.session_state.score += 5
            if q5 == "Temporary memory": st.session_state.score += 5
            st.session_state.page = 4
            st.rerun()

    # ---------- SECTION 4 ----------
    elif st.session_state.page == 4:
        st.subheader("🌍 Section 4: General Knowledge (25 Marks)")

        q1 = st.radio("16. Capital of India?", ["Delhi", "Mumbai"])
        q2 = st.radio("17. Father of Computer?", ["Charles Babbage", "Newton"])
        q3 = st.radio("18. ISRO is related to?", ["Space", "Medical"])
        q4 = st.radio("19. AI is used in?", ["Robots", "Farming only"])
        q5 = st.radio("20. Internet is?", ["Network", "Device"])

        if st.button("📊 Submit Test"):
            if q1 == "Delhi": st.session_state.score += 5
            if q2 == "Charles Babbage": st.session_state.score += 5
            if q3 == "Space": st.session_state.score += 5
            if q4 == "Robots": st.session_state.score += 5
            if q5 == "Network": st.session_state.score += 5
            st.session_state.page = 5
            st.rerun()

    # ---------- RESULT ----------
    elif st.session_state.page == 5:
        st.header("📄 Test Result")
        score = st.session_state.score
        st.write(f"### 🎯 Total Score: **{score} / 100**")

        if score >= 75:
            st.success("🎓 Recommended Degree: **B.Sc Computer Science / CS with AI**")
            st.write("""
You have strong aptitude, logic, and technical understanding.

**Career Examples:**  
- Software Engineer  
- AI Engineer  
- Data Scientist  
- Cyber Security Analyst
""")
        elif score >= 50:
            st.warning("🎓 Recommended Degree: **BCA / B.Sc / B.Com**")
            st.write("""
You have good general and analytical skills.

**Career Examples:**  
- Business Analyst  
- IT Support  
- Banking & Finance
""")
        else:
            st.info("🎓 Recommended Degree: **Arts / Management**")
            st.write("""
You may excel in creative or management roles.

**Career Examples:**  
- Media  
- HR  
- Administration
""")

        st.button("🔄 Restart Test", on_click=lambda: st.session_state.clear())

# ---------------- ACHIEVEMENTS ----------------
elif menu == "🏆 Student Achievements":
    st.header("🏆 Student Achievements")
    show_image("assets/ai_achievements.png", use_column_width=True)

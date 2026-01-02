import streamlit as st
from openai import OpenAI
import os
from pathlib import Path

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
        "🤖 Ask College GPT"
    ]
)

# ---------------- ABOUT ----------------
if menu == "🏫 About College":
    st.header("🏫 About SA College of Arts & Science")
    st.write("""
SA College of Arts & Science (SACAS) is a reputed Arts & Science institution
located in **Thiruverkadu, Avadi, Chennai**.

The college is committed to:
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
elif menu == "🎓 Career Counselling":
    st.header("🎓 AI-Based Career Counselling")
    st.write("Answer this short test to find the best **degree & career path** for you.")

    st.subheader("📝 Student Interest Test")

    q1 = st.radio(
        "1️⃣ Which activity do you enjoy most?",
        ["Solving logical problems", "Designing visuals", "Managing people", "Working with numbers"]
    )

    q2 = st.radio(
        "2️⃣ Which subject do you like the most?",
        ["Computer Science", "Mathematics", "Business Studies", "Arts & Creativity"]
    )

    q3 = st.radio(
        "3️⃣ How do you prefer to work?",
        ["With technology", "With people", "With data", "Creatively"]
    )

    q4 = st.radio(
        "4️⃣ What is your career goal?",
        ["High-paying tech job", "Government job", "Business", "Creative profession"]
    )

    if st.button("🔍 Get Career Recommendation"):
        st.divider()

        # AI / TECH PATH
        if q1 == "Solving logical problems" and q3 == "With technology":
            st.success("✅ Recommended Degree: **B.Sc Computer Science / CS with AI**")
            st.write("""
**Best Career Paths:**
- Software Developer  
- AI / ML Engineer  
- Data Scientist  
- Cyber Security Analyst  

**Why this fits you:**  
You enjoy logic, technology, and problem solving.
            """)

        # DATA / MATH PATH
        elif q1 == "Working with numbers" or q2 == "Mathematics":
            st.success("✅ Recommended Degree: **B.Sc Mathematics / Data Science**")
            st.write("""
**Best Career Paths:**
- Data Analyst  
- Statistician  
- Banking & Finance  
- Actuarial Science  

**Why this fits you:**  
You are strong with numbers and analysis.
            """)

        # MANAGEMENT PATH
        elif q3 == "With people" or q4 == "Business":
            st.success("✅ Recommended Degree: **BBA / B.Com**")
            st.write("""
**Best Career Paths:**
- Business Analyst  
- HR Manager  
- Marketing Executive  
- Entrepreneur  

**Why this fits you:**  
You like leadership, communication, and management.
            """)

        # CREATIVE PATH
        else:
            st.success("✅ Recommended Degree: **BA / Visual Communication / Design**")
            st.write("""
**Best Career Paths:**
- Graphic Designer  
- Media & Film  
- Content Creator  
- UX/UI Designer  

**Why this fits you:**  
You enjoy creativity and expressive work.
            """)

        st.info("📌 *This recommendation is based on your interests. For detailed guidance, consult faculty counsellors.*")


# ---------------- EVENTS ----------------
elif menu == "🎉 Events & Activities":
    st.header("🎉 CS with AI – Events & Activities")
    st.write("Freshers Day, Technical Events, Cultural Programs & Workshops")
    show_image("assets/event.png", caption="Freshers Day – CS with AI", use_column_width=True)

# ---------------- LOCATION ----------------
elif menu == "📍 Location":
    st.header("📍 College Location")
    st.write("""
**SA College of Arts & Science**  
Thiruverkadu, Avadi, Chennai – Tamil Nadu
    """)
    st.map({"lat": [13.0475], "lon": [80.1012]})

# ---------------- SYLLABUS ----------------
elif menu == "📚 CS & CS-AI Syllabus":
    st.header("📚 B.Sc Computer Science & CS with AI – Syllabus")

    st.subheader("Semester Highlights")
    st.markdown("""
**Core Subjects:**
- Programming in C / Python  
- Data Structures  
- Database Management Systems  
- Operating Systems  
- Computer Networks  

**AI Specialization:**
- Artificial Intelligence  
- Machine Learning  
- Deep Learning  
- Natural Language Processing  
- Computer Vision  

*(As per University of Madras norms)*  
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
*Head of the Department – CS with AI*

**Qualifications:**  
M.Sc, M.Phil, NET, SET  

**Experience:**  
- UG: 30 Years  
- PG: 23 Years  

**Focus:**  
Industry-ready skills, ethical AI, innovation, and hands-on learning.
        """)

# ---------------- ACHIEVEMENTS ----------------
elif menu == "🏆 Student Achievements":
    st.header("🏆 Student Achievements – CS with AI")
    show_image("assets/ai_achievements.png", use_column_width=True)

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
                {
                    "role": "system",
                    "content": "You are an academic assistant for SA College of Arts & Science. Answer only based on CS and CS with AI syllabus."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        reply = response.choices[0].message.content
        st.session_state.chat.append({"role": "assistant", "content": reply})
        st.rerun()

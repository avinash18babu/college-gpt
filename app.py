import streamlit as st
from openai import OpenAI
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="College GPT by Avinash",
    page_icon="🎓",
    layout="wide"
)

# ---------------- TOP TITLE (SMALL, PROFESSIONAL) ----------------
st.markdown("""
<style>
@keyframes glow {
  0% { text-shadow: 0 0 3px #22c55e; }
  50% { text-shadow: 0 0 8px #22c55e; }
  100% { text-shadow: 0 0 3px #22c55e; }
}
.small-title {
  font-size: 14px;
  font-weight: 500;
  color: #22c55e;
  animation: glow 2s infinite;
  text-align: right;
}
.section-box {
  background-color: #0f172a;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 15px;
}
.chat-user {
  background-color: #1f2937;
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 5px;
}
.chat-ai {
  background-color: #064e3b;
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 15px;
}
</style>

<div class="small-title">🤖 College GPT by Avinash</div>
<hr>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h2 style='text-align:center;'>🎓 SA College of Arts & Science</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Affiliated to University of Madras</h4>", unsafe_allow_html=True)
st.divider()

# ---------------- SIDEBAR NAVIGATION (EXPANDED) ----------------
st.sidebar.title("📘 Navigation")
menu = st.sidebar.radio(
    "Go to",
    [
        "🏫 About College",
        "🎯 Vision & Mission",
        "🏢 Departments",
        "🎉 Events & Activities",
        "📍 Location",
        "📚 Exact CS & CS-AI Syllabus",
        "🤖 Ask College GPT"
    ]
)

# ---------------- ABOUT COLLEGE (EXPANDED) ----------------
if menu == "🏫 About College":
    st.header("🏫 About SA College of Arts & Science")

    st.markdown("""
    <div class="section-box">
    <b>SA College of Arts & Science (SACAS)</b> is a premier Arts and Science institution
    located in Chennai, Tamil Nadu. The college is committed to providing quality education,
    fostering innovation, and shaping socially responsible graduates.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.image(
            "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f",
            caption="Academic Excellence",
            use_column_width=True
        )

    with col2:
        st.image(
            "https://images.unsplash.com/photo-1503676260728-1c00da094a0b",
            caption="Student-Centered Learning",
            use_column_width=True
        )

    st.markdown("""
    - Affiliated to **University of Madras**
    - Offers UG and PG programmes
    - Focus on academic, cultural, and skill development
    - Well-equipped laboratories and library

    📌 *Information summarized from the official SACAS website.*
    """)

# ---------------- VISION & MISSION ----------------
elif menu == "🎯 Vision & Mission":
    st.header("🎯 Vision & Mission")

    st.markdown("""
    <div class="section-box">
    <b>Vision</b><br>
    To emerge as a center of excellence in higher education by nurturing talent,
    promoting innovation, and contributing to societal development.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section-box">
    <b>Mission</b><br>
    • To provide quality education with ethical values<br>
    • To encourage research and innovation<br>
    • To prepare students for global challenges
    </div>
    """, unsafe_allow_html=True)

# ---------------- DEPARTMENTS ----------------
elif menu == "🏢 Departments":
    st.header("🏢 Academic Departments")

    st.markdown("""
    <div class="section-box">
    • Computer Science<br>
    • Computer Science with Artificial Intelligence<br>
    • Commerce<br>
    • Management Studies<br>
    • Mathematics<br>
    • English<br>
    • Physics<br>
    • Chemistry
    </div>
    """, unsafe_allow_html=True)

# ---------------- EVENTS & ACTIVITIES (VISUAL) ----------------
elif menu == "🎉 Events & Activities":
    st.header("🎉 Events & Student Activities")

    col1, col2 = st.columns(2)

    with col1:
        st.image(
            "https://images.unsplash.com/photo-1523580846011-d3a5bc25702b",
            caption="Technical Symposium",
            use_column_width=True
        )
        st.write("""
        **Technical Symposium**
        - Paper presentations
        - Coding contests
        - Technical workshops
        """)

    with col2:
        st.image(
            "https://images.unsplash.com/photo-1518609878373-06d740f60d8b",
            caption="Cultural Fest",
            use_column_width=True
        )
        st.write("""
        **Cultural Fest**
        - Dance & music competitions
        - Arts and drama
        - Inter-college events
        """)

    st.markdown("""
    <div class="section-box">
    The college actively promotes co-curricular and extra-curricular activities
    to enhance leadership, teamwork, and creativity among students.
    </div>
    """, unsafe_allow_html=True)

# ---------------- LOCATION ----------------
elif menu == "📍 Location":
    st.header("📍 College Location")

    st.write("""
    **Address:**  
    Thiruverkadu, Avadi, Chennai – Tamil Nadu
    """)

    st.markdown("""
    <iframe 
        src="https://www.google.com/maps?q=SA%20College%20of%20Arts%20and%20Science%20Thiruverkadu&output=embed"
        width="100%" height="400" style="border:0;" loading="lazy">
    </iframe>
    """, unsafe_allow_html=True)

# ---------------- SYLLABUS ----------------
elif menu == "📚 Exact CS & CS-AI Syllabus":
    st.header("📚 Computer Science & CS-AI Syllabus")
    st.write("Detailed semester-wise syllabus for academic reference.")

    st.subheader("B.Sc Computer Science")
    st.write("""
    Sem I: Programming in C, Digital Computer Fundamentals  
    Sem II: Data Structures, Discrete Mathematics  
    Sem III: OOP with Java, Operating Systems  
    Sem IV: DBMS, Software Engineering  
    Sem V: Web Programming, Computer Networks  
    Sem VI: Python Programming, Project Work
    """)

    st.subheader("B.Sc Computer Science with Artificial Intelligence")
    st.write("""
    Sem I: Python Programming, Mathematics for AI  
    Sem II: Data Structures, Probability & Statistics  
    Sem III: Artificial Intelligence, Operating Systems  
    Sem IV: Machine Learning, DBMS  
    Sem V: Deep Learning, NLP  
    Sem VI: Computer Vision, AI Project
    """)

# ---------------- COLLEGE GPT ----------------
elif menu == "🤖 Ask College GPT":
    st.header("🤖 College GPT")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Ask your academic question and press ENTER")
        send = st.form_submit_button("Send")

    if send and user_input:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an academic assistant for SA College of Arts and Science."},
                {"role": "user", "content": user_input}
            ]
        )
        st.session_state.chat_history.append({
            "question": user_input,
            "answer": response.choices[0].message.content
        })

    for chat in st.session_state.chat_history:
        st.markdown(f"<div class='chat-user'><b>You:</b> {chat['question']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-ai'><b>College GPT:</b> {chat['answer']}</div>", unsafe_allow_html=True)

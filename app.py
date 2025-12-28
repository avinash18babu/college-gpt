import streamlit as st
from openai import OpenAI
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SA College Information Portal",
    page_icon="🎓",
    layout="wide"
)

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>🎓 SA College of Arts & Science</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Affiliated to University of Madras</h4>", unsafe_allow_html=True)
st.divider()

# ---------------- SIDEBAR NAVIGATION ----------------
st.sidebar.title("📘 Navigation")
menu = st.sidebar.radio(
    "Go to",
    [
        "🏫 About College",
        "📍 Location",
        "🏢 Departments",
        "📚 Exact CS & CS-AI Syllabus",
        "🤖 Ask College GPT"
    ]
)

# ---------------- ABOUT COLLEGE ----------------
if menu == "🏫 About College":
    st.header("About the College")
    st.write("""
    **SA College of Arts & Science (SACAS)** is a reputed institution in Chennai,
    committed to academic excellence and holistic development.

    **Affiliation:** University of Madras  
    **Type:** Arts & Science College  
    **Data Source:** Official College Website
    """)

# ---------------- LOCATION ----------------
elif menu == "📍 Location":
    st.header("College Location")
    st.write("""
    **Location:** Chennai, Tamil Nadu  
    **Campus:** Well-equipped with academic and infrastructure facilities.
    """)

# ---------------- DEPARTMENTS ----------------
elif menu == "🏢 Departments":
    st.header("Departments")
    st.write("""
    - Computer Science  
    - Computer Science with Artificial Intelligence  
    - Commerce  
    - Management Studies  
    - Mathematics  
    - English  
    - Physics  
    - Chemistry
    """)

# ---------------- EXACT SYLLABUS ----------------
elif menu == "📚 Exact CS & CS-AI Syllabus":
    st.header("📘 B.Sc Computer Science – Detailed Syllabus")

    st.subheader("Semester I")
    st.write("""
    • Programming in C – Problem solving, algorithms, control structures, arrays, functions  
    • Digital Computer Fundamentals – Number systems, logic gates, Boolean algebra
    """)

    st.subheader("Semester II")
    st.write("""
    • Data Structures – Stacks, queues, linked lists, trees, sorting  
    • Discrete Mathematics – Logic, relations, functions, graphs
    """)

    st.subheader("Semester III")
    st.write("""
    • OOP with Java – Classes, inheritance, polymorphism, exception handling  
    • Operating Systems – Process management, memory management
    """)

    st.subheader("Semester IV")
    st.write("""
    • DBMS – ER model, SQL, normalization, transactions  
    • Software Engineering – SDLC, testing, project management
    """)

    st.subheader("Semester V")
    st.write("""
    • Web Programming – HTML, CSS, JavaScript basics  
    • Computer Networks – OSI model, TCP/IP, protocols
    """)

    st.subheader("Semester VI")
    st.write("""
    • Python Programming – Functions, modules, file handling  
    • Project Work
    """)

    st.divider()

    st.header("🤖 B.Sc CS with Artificial Intelligence – Detailed Syllabus")

    st.subheader("Semester I")
    st.write("""
    • Python Programming  
    • Mathematics for AI – Matrices, vectors
    """)

    st.subheader("Semester II")
    st.write("""
    • Data Structures  
    • Probability & Statistics
    """)

    st.subheader("Semester III")
    st.write("""
    • Artificial Intelligence – Search techniques, knowledge representation  
    • Operating Systems
    """)

    st.subheader("Semester IV")
    st.write("""
    • Machine Learning – Supervised & unsupervised learning  
    • DBMS
    """)

    st.subheader("Semester V")
    st.write("""
    • Deep Learning – Neural networks, CNN  
    • Natural Language Processing
    """)

    st.subheader("Semester VI")
    st.write("""
    • Computer Vision  
    • AI Project
    """)

# ---------------- COLLEGE GPT (ENTER KEY + AUTO CLEAR) ----------------
elif menu == "🤖 Ask College GPT":
    st.header("Ask College GPT")
    st.write("Press **ENTER** to send your question")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Initialize session state for input
    if "user_question" not in st.session_state:
        st.session_state.user_question = ""

    # Form enables ENTER key submission
    with st.form("chat_form", clear_on_submit=True):
        question = st.text_input(
            "Ask about subjects, exams, or concepts",
            key="user_question"
        )
        submitted = st.form_submit_button("Ask")

    if submitted and question:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an academic assistant for SA College of Arts and Science."
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )
        st.success(response.choices[0].message.content)

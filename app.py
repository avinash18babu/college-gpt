import streamlit as st
import os
from openai import OpenAI

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="SA College Academic Portal",
    page_icon="🎓",
    layout="wide"
)

# =========================
# MODERN DARK + ANIMATION CSS
# =========================
st.markdown("""
<style>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.main {
  background: radial-gradient(circle at top, #1a0008, #050507);
}

h1, h2, h3 {
  color: #ff003c;
  text-shadow: 0 0 12px #ff003c;
  animation: fadeIn 1s ease-in-out;
}

p, li, div, label {
  color: #e5e7eb;
  font-size: 16px;
  animation: fadeIn 1.2s ease-in-out;
}

.stTextInput input {
  background-color: #0f0f14;
  color: white;
  border: 1px solid #ff003c;
}

.stButton > button {
  background: linear-gradient(90deg, #ff003c, #ff4d6d);
  color: white;
  border-radius: 10px;
  height: 45px;
  font-size: 16px;
  transition: transform 0.2s ease;
}

.stButton > button:hover {
  transform: scale(1.05);
}

.sidebar {
  background-color: #0b0b0f;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER WITH LOGO
# =========================
st.markdown("<h1 style='text-align:center;'>🎓 SA College of Arts & Science</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Academic Information & AI Assistance Portal</h4>", unsafe_allow_html=True)

# Optional logo (place logo.png in repo root)
try:
    st.image("logo.png", width=120)
except:
    pass

st.divider()

# =========================
# SIDEBAR
# =========================
menu = st.sidebar.radio(
    "📘 Navigation",
    [
        "🏫 About College",
        "🏢 Departments",
        "📚 CS & CS-AI Syllabus",
        "🤖 College GPT"
    ]
)

# =========================
# ABOUT COLLEGE
# =========================
if menu == "🏫 About College":
    st.header("🏫 About the College")
    st.write("""
    **SA College of Arts & Science (SACAS)** is a reputed Arts & Science institution
    located in Chennai, Tamil Nadu.

    - Affiliated to **University of Madras**
    - Focus on academic excellence
    - Offers UG & PG programmes

    📌 *Information referenced from the official SACAS website.*
    """)

# =========================
# DEPARTMENTS
# =========================
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

# =========================
# SYLLABUS (REFERENCE DATA)
# =========================
elif menu == "📚 CS & CS-AI Syllabus":
    st.header("📘 B.Sc Computer Science")

    st.markdown("""
    **Semester I:** Programming in C, Digital Computer Fundamentals  
    **Semester II:** Data Structures, Discrete Mathematics  
    **Semester III:** OOP with Java, Operating Systems  
    **Semester IV:** DBMS, Software Engineering  
    **Semester V:** Web Programming, Computer Networks  
    **Semester VI:** Python Programming, Project Work  
    """)

    st.divider()

    st.header("🤖 B.Sc Computer Science with Artificial Intelligence")

    st.markdown("""
    **Semester I:** Python Programming, Mathematics for AI  
    **Semester II:** Data Structures, Probability & Statistics  
    **Semester III:** Artificial Intelligence, Operating Systems  
    **Semester IV:** Machine Learning, DBMS  
    **Semester V:** Deep Learning, Natural Language Processing  
    **Semester VI:** Computer Vision, AI Project  
    """)

# =========================
# COLLEGE GPT (SYLLABUS-RESTRICTED)
# =========================
elif menu == "🤖 College GPT":
    st.header("🤖 College GPT")
    st.write("Answers are **STRICTLY based on SACAS CS / CS-AI syllabus**")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    question = st.text_input("Type your question and press ENTER")

    marks = st.selectbox(
        "Answer format",
        ["2 Marks", "5 Marks", "10 Marks"]
    )

    if question:
        with st.spinner("Analyzing syllabus..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """
You are a college academic assistant for SA College of Arts & Science.
You must answer ONLY from B.Sc Computer Science and
B.Sc Computer Science with Artificial Intelligence syllabus.
If the question is outside syllabus, politely say:
'This question is outside the prescribed syllabus.'
Answers must be exam-oriented.
"""
                    },
                    {
                        "role": "user",
                        "content": f"Answer in {marks} format: {question}"
                    }
                ]
            )
        st.success(response.choices[0].message.content)

# =========================
# FOOTER
# =========================
st.divider()
st.markdown(
    "<p style='text-align:center;'>© SA College of Arts & Science | Academic Project</p>",
    unsafe_allow_html=True
)

import streamlit as st
from openai import OpenAI
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="College GPT by Avinash",
    page_icon="🎓",
    layout="wide"
)

# ---------------- HEADER ----------------
st.markdown("""
<style>
.title-main {
    font-size: 36px;
    font-weight: 700;
    text-align: center;
}
.subtitle {
    text-align: center;
    font-size: 16px;
    color: #555;
}
.small-tag {
    text-align:center;
    font-size:12px;
    color:#777;
    margin-bottom:20px;
}
.card {
    background-color:#f9f9f9;
    padding:20px;
    border-radius:12px;
    margin-bottom:20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title-main'>🎓 SA College of Arts & Science</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Affiliated to University of Madras</div>", unsafe_allow_html=True)
st.markdown("<div class='small-tag'>College GPT by Avinash</div>", unsafe_allow_html=True)

st.divider()

# ---------------- SIDEBAR ----------------
st.sidebar.title("📘 Navigation")

menu = st.sidebar.radio(
    "Go to",
    [
        "🏫 About College",
        "🎯 Vision & Mission",
        "💻 B.Sc CS with AI Department",
        "👨‍🏫 Faculty (CS-AI)",
        "🎉 Events & Activities",
        "📍 Location",
        "📚 Exact CS & CS-AI Syllabus",
        "🤖 Ask College GPT"
    ]
)

# ---------------- ABOUT ----------------
if menu == "🏫 About College":
    st.markdown("## 🏫 About SA College of Arts & Science")
    st.markdown("""
    <div class="card">
    <b>SA College of Arts & Science (SACAS)</b> is a premier institution located in 
    <b>Thiruverkadu, Avadi, Chennai</b>. The college is committed to academic excellence,
    innovation, and holistic student development.

    • Affiliated to University of Madras  
    • Well-equipped campus  
    • Strong focus on skill development  
    • Active placement and training cell
    </div>
    """, unsafe_allow_html=True)

    st.image(
        [
            "https://sacas.ac.in/wp-content/uploads/2023/07/college-campus.jpg",
            "https://sacas.ac.in/wp-content/uploads/2023/07/library.jpg"
        ],
        use_column_width=True
    )

# ---------------- VISION ----------------
elif menu == "🎯 Vision & Mission":
    st.markdown("## 🎯 Vision & Mission")
    st.markdown("""
    <div class="card">
    <b>Vision:</b><br>
    To emerge as a centre of excellence in higher education by nurturing knowledge,
    innovation, and ethical values.

    <br><br>
    <b>Mission:</b><br>
    • Provide quality education aligned with industry needs<br>
    • Encourage research and innovation<br>
    • Develop socially responsible graduates
    </div>
    """, unsafe_allow_html=True)

# ---------------- CS AI DEPT ----------------
elif menu == "💻 B.Sc CS with AI Department":
    st.markdown("## 💻 B.Sc Computer Science with Artificial Intelligence")
    st.markdown("""
    <div class="card">
    The <b>B.Sc Computer Science with Artificial Intelligence</b> programme is designed
    to equip students with strong foundations in computing along with modern AI concepts.

    <br><br>
    <b>Key Highlights:</b>
    • Python, Java, Data Structures  
    • Machine Learning & AI fundamentals  
    • Hands-on projects  
    • Industry-oriented curriculum  
    • University of Madras syllabus
    </div>
    """, unsafe_allow_html=True)

# ---------------- FACULTY ----------------
elif menu == "👨‍🏫 Faculty (CS-AI)":
    st.markdown("## 👨‍🏫 Head of the Department – CS with AI")

    col1, col2 = st.columns([1,2])
    with col1:
        st.image(
            "https://sacas.ac.in/wp-content/uploads/2023/08/krishnan-r.jpg",
            use_column_width=True
        )
    with col2:
        st.markdown("""
        <div class="card">
        <b>Mr. Krishnan R</b><br>
        Head of the Department – CS with AI<br><br>

        Qualifications:<br>
        M.Sc, M.Phil, NET, SET<br><br>

        Experience:<br>
        • UG: 30 Years<br>
        • PG: 23 Years<br><br>

        Focus on industry-ready skills, ethical AI, and innovation.
        </div>
        """, unsafe_allow_html=True)

# ---------------- EVENTS ----------------
elif menu == "🎉 Events & Activities":
    st.markdown("## 🎉 CS-AI Department Events")
    st.markdown("""
    <div class="card">
    <b>Freshers Day – 26.08.2025</b><br>
    Organized by CS with AI department with cultural events, games, and student performances.
    The event encouraged interaction between seniors and juniors.
    </div>
    """, unsafe_allow_html=True)

    st.image(
        [
            "https://sacas.ac.in/wp-content/uploads/2025/09/18-2025-09-01T160424.061-768x768.jpg",
            "https://sacas.ac.in/wp-content/uploads/2025/09/16-2025-09-01T160429.711-768x768.jpg"
        ],
        use_column_width=True
    )

# ---------------- LOCATION ----------------
elif menu == "📍 Location":
    st.markdown("## 📍 College Location")
    st.markdown("""
    <div class="card">
    SA College of Arts & Science<br>
    Thiruverkadu, Avadi, Chennai – Tamil Nadu
    </div>
    """, unsafe_allow_html=True)

    st.map({"lat":[13.0557], "lon":[80.1164]})

# ---------------- SYLLABUS ----------------
elif menu == "📚 Exact CS & CS-AI Syllabus":
    st.markdown("## 📚 CS & CS-AI Syllabus (University of Madras)")
    st.markdown("""
    <div class="card">
    <b>Core Subjects Include:</b><br>
    • Python Programming<br>
    • Java Programming<br>
    • Data Structures<br>
    • Operating Systems<br>
    • Database Management Systems<br>
    • Artificial Intelligence<br>
    • Machine Learning<br>
    • Computer Networks<br><br>

    *Exact syllabus is followed as prescribed by University of Madras.*
    </div>
    """, unsafe_allow_html=True)

# ---------------- GPT ----------------
elif menu == "🤖 Ask College GPT":
    st.markdown("## 🤖 Ask College GPT (CS / CS-AI Only)")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    question = st.text_input("Ask your question and press Enter", key="input")

    if question:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are College GPT for SA College of Arts & Science. "
                        "Answer only based on CS and CS-AI syllabus, University of Madras. "
                        "Do not answer unrelated topics."
                    )
                },
                {"role": "user", "content": question}
            ]
        )

        st.session_state.chat.append(("You", question))
        st.session_state.chat.append(("College GPT", response.choices[0].message.content))
        st.session_state.input = ""

    for sender, msg in st.session_state.chat:
        if sender == "You":
            st.markdown(f"**🧑 You:** {msg}")
        else:
            st.markdown(f"**🤖 College GPT:** {msg}")

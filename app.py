import streamlit as st
from openai import OpenAI
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="College GPT by Avinash",
    page_icon="🎓",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}
h1, h2, h3, h4 {
    color: #0b2545;
}
p, li {
    color: #1c1c1c;
    font-size: 16px;
}
img {
    border-radius: 14px;
}
.chat-box {
    background: #ffffff;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
}
.footer {
    text-align: center;
    color: gray;
    font-size: 13px;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    "<h2 style='text-align:center;'>🎓 SA College of Arts & Science</h2>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center;'>Affiliated to University of Madras<br>"
    "<small>College GPT by Avinash</small></p>",
    unsafe_allow_html=True
)

st.divider()

# ---------------- SIDEBAR ----------------
st.sidebar.title("📘 Navigation")

menu = st.sidebar.radio(
    "Go to",
    [
        "🏫 About College",
        "🎯 Vision & Mission",
        "🏢 CS with AI Department",
        "🎉 Events & Achievements",
        "📍 Location",
        "🤖 Ask College GPT"
    ]
)

# ---------------- ABOUT COLLEGE ----------------
if menu == "🏫 About College":
    st.header("🏫 About SA College of Arts & Science")

    st.write("""
    **SA College of Arts & Science (SACAS)** is a reputed Arts & Science institution
    located at **Thiruverkadu, Avadi, Chennai**, offering quality higher education.

    The college is committed to academic excellence, innovation, discipline,
    and holistic student development.
    """)

    st.image(
        ["assets/ai_students.jpg", "assets/event.jpg"],
        use_column_width=True
    )

# ---------------- VISION & MISSION ----------------
elif menu == "🎯 Vision & Mission":
    st.header("🎯 Vision & Mission")

    st.subheader("Vision")
    st.write("""
    To empower students with knowledge, skills, and ethical values
    to meet global challenges.
    """)

    st.subheader("Mission")
    st.write("""
    - Deliver quality education  
    - Promote research and innovation  
    - Encourage industry-ready skills  
    - Develop socially responsible graduates  
    """)

# ---------------- CS WITH AI DEPARTMENT ----------------
elif menu == "🏢 CS with AI Department":
    st.header("🤖 B.Sc Computer Science with Artificial Intelligence")

    st.write("""
    The **Department of Computer Science with Artificial Intelligence**
    prepares students for careers in AI, Data Science, Software Development,
    and emerging technologies through a strong academic foundation.
    """)

    st.subheader("👨‍🏫 Head of the Department")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image("assets/hod.jpg", width=220)

    with col2:
        st.markdown("""
        **Mr. Krishnan R**  
        *Head of the Department – CS with AI*

        **Qualifications:**  
        M.Sc, M.Phil, NET, SET  

        **Experience:**  
        - UG: 30 Years  
        - PG: 23 Years  

        Focus on industry-ready skills, ethical AI,
        hands-on learning, and student mentoring.
        """)

# ---------------- EVENTS & ACHIEVEMENTS ----------------
elif menu == "🎉 Events & Achievements":
    st.header("🎉 Events & Student Achievements")

    st.write("""
    The CS with AI department regularly conducts Freshers Day,
    technical events, workshops, and cultural programs.
    """)

    st.image(
        ["assets/ai_students_achievement.jpg"],
        use_column_width=True
    )

# ---------------- LOCATION ----------------
elif menu == "📍 Location":
    st.header("📍 College Location")

    st.write("""
    **SA College of Arts & Science**  
    Thiruverkadu, Avadi  
    Chennai, Tamil Nadu
    """)

    st.markdown("""
    <iframe
        src="https://www.google.com/maps?q=SA+College+of+Arts+and+Science+Thiruverkadu&output=embed"
        width="100%" height="450" style="border:0;" allowfullscreen="" loading="lazy">
    </iframe>
    """, unsafe_allow_html=True)

# ---------------- COLLEGE GPT CHAT ----------------
elif menu == "🤖 Ask College GPT":
    st.header("🤖 College GPT – CS with AI Assistant")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    user_input = st.chat_input("Ask about CS, AI, exams, syllabus...")

    if user_input:
        st.session_state.chat.append(("user", user_input))

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an academic assistant for SA College of Arts & Science, CS with AI department."
                }
            ] + [
                {"role": role, "content": msg}
                for role, msg in st.session_state.chat
            ]
        )

        reply = response.choices[0].message.content
        st.session_state.chat.append(("assistant", reply))

    for role, msg in st.session_state.chat:
        if role == "user":
            st.markdown(f"<div class='chat-box'><b>You:</b> {msg}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-box'><b>College GPT:</b> {msg}</div>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
© 2025 SA College of Arts & Science | College GPT Project by Avinash
</div>
""", unsafe_allow_html=True)

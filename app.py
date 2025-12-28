import streamlit as st
from openai import OpenAI
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="College GPT by Avinash",
    page_icon="🎓",
    layout="wide"
)

# ---------------- TOP TITLE (SMALL NAME + ANIMATION) ----------------
st.markdown("""
<style>
@keyframes glow {
  0% { text-shadow: 0 0 4px #22c55e; }
  50% { text-shadow: 0 0 10px #22c55e; }
  100% { text-shadow: 0 0 4px #22c55e; }
}
.small-title {
  font-size: 14px;
  font-weight: 500;
  color: #22c55e;
  animation: glow 2s infinite;
  text-align: right;
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

# ---------------- LOCATION (UPDATED + GOOGLE MAP) ----------------
elif menu == "📍 Location":
    st.header("College Location")

    st.write("""
    **Address:**  
    Thiruverkadu, Avadi, Chennai – Tamil Nadu
    """)

    st.subheader("📍 Google Map Location")

    # Google Maps Embed
    st.markdown("""
    <iframe 
        src="https://www.google.com/maps?q=SA%20College%20of%20Arts%20and%20Science%20Thiruverkadu&output=embed"
        width="100%" 
        height="400" 
        style="border:0;" 
        allowfullscreen="" 
        loading="lazy">
    </iframe>
    """, unsafe_allow_html=True)

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
    st.write("• Programming in C\n• Digital Computer Fundamentals")

    st.subheader("Semester II")
    st.write("• Data Structures\n• Discrete Mathematics")

    st.subheader("Semester III")
    st.write("• OOP with Java\n• Operating Systems")

    st.subheader("Semester IV")
    st.write("• DBMS\n• Software Engineering")

    st.subheader("Semester V")
    st.write("• Web Programming\n• Computer Networks")

    st.subheader("Semester VI")
    st.write("• Python Programming\n• Project Work")

    st.divider()

    st.header("🤖 B.Sc CS with Artificial Intelligence")

    st.subheader("Semester I")
    st.write("• Python Programming\n• Mathematics for AI")

    st.subheader("Semester II")
    st.write("• Data Structures\n• Probability & Statistics")

    st.subheader("Semester III")
    st.write("• Artificial Intelligence\n• Operating Systems")

    st.subheader("Semester IV")
    st.write("• Machine Learning\n• DBMS")

    st.subheader("Semester V")
    st.write("• Deep Learning\n• Natural Language Processing")

    st.subheader("Semester VI")
    st.write("• Computer Vision\n• AI Project")

# ---------------- COLLEGE GPT (CHAT STYLE) ----------------
elif menu == "🤖 Ask College GPT":
    st.header("Ask College GPT")
    st.write("Type your question and press **ENTER**")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Your question")
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

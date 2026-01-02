import streamlit as st
from openai import OpenAI
import os
from pathlib import Path
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_pdf(name, score, grade, degree, career):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height-50, "SA COLLEGE OF ARTS & SCIENCE")

    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height-80, "ONLINE DEGREE ENTRANCE TEST RESULT")

    y = height - 140
    c.drawString(50, y, f"Student Name: {name}")
    y -= 30
    c.drawString(50, y, f"Score: {score} / 100")
    y -= 30
    c.drawString(50, y, f"Grade: {grade}")
    y -= 30
    c.drawString(50, y, f"Recommended Degree: {degree}")
    y -= 40

    c.drawString(50, y, "Suggested Career Paths:")
    y -= 25
    for cpath in career:
        c.drawString(70, y, f"- {cpath}")
        y -= 20

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SA College of Arts & Science | College GPT",
    page_icon="🎓",
    layout="wide"
)

# ---------------- SAFE IMAGE ----------------
def show_image(path, **kwargs):
    if Path(path).exists():
        st.image(path, **kwargs)
    else:
        st.info(f"Image missing: {path}")

# ---------------- HEADER ----------------
st.markdown("""
<style>
.title{font-size:40px;font-weight:700;text-align:center;}
.subtitle{font-size:18px;text-align:center;color:gray;}
.credit{font-size:13px;text-align:center;color:#666;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎓 SA College of Arts & Science</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Affiliated to University of Madras</div>', unsafe_allow_html=True)
st.markdown('<div class="credit">College GPT by Avinash</div>', unsafe_allow_html=True)
st.divider()

# ---------------- SIDEBAR ----------------
menu = st.sidebar.radio(
    "📘 Navigation",
    [
        "🏫 About College",
        "📍 Location",
        "📚 CS & CS-AI Syllabus",
        "👨‍🏫 CS with AI – HOD",
        "🏆 Student Achievements",
        "📝 Online Degree Entrance Test",
        "🤖 Ask College GPT"
    ]
)

# ---------------- ABOUT ----------------
if menu == "🏫 About College":
    st.header("🏫 About SA College of Arts & Science")
    st.write("""
SA College of Arts & Science (SACAS) is a reputed Arts & Science institution  
located in **Thiruverkadu, Avadi, Chennai**.

### Focus Areas
- Academic Excellence  
- Innovation & Research  
- Discipline & Ethics  
- Holistic Student Development  
    """)
    show_image("assets/ai_students.png", use_column_width=True)

# ---------------- LOCATION ----------------
elif menu == "📍 Location":
    st.header("📍 College Location")
    st.write("**SA College of Arts & Science, Thiruverkadu, Avadi, Chennai**")
    df = pd.DataFrame({"lat":[13.0475], "lon":[80.1012]})
    st.map(df)

# ---------------- SYLLABUS ----------------
elif menu == "📚 CS & CS-AI Syllabus":
    st.header("📚 B.Sc Computer Science & CS with AI")

    st.subheader("Core Subjects")
    st.markdown("""
- Programming in C & Python  
- Data Structures  
- DBMS  
- Operating Systems  
- Computer Networks  
    """)

    st.subheader("AI Specialization")
    st.markdown("""
- Artificial Intelligence  
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
*M.Sc, M.Phil, NET, SET*

**Experience**
- UG: 30 Years  
- PG: 23 Years  

**Focus**
- Industry-ready skills  
- Ethical AI  
- Practical learning
        """)

elif menu == "📝 Online Degree Entrance Test":
    st.header("📝 Online Degree Entrance Test")
    st.caption("Aptitude • Logical • Computer • General Knowledge | 100 Marks")

    student_name = st.text_input("Enter Student Name")

    TOTAL_TIME = 20 * 60  # 20 minutes

    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()
        st.session_state.submitted = False

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = TOTAL_TIME - elapsed

    if remaining <= 0:
        st.warning("⏰ Time is up! Auto-submitting test.")
        st.session_state.submitted = True
        remaining = 0

    mins, secs = divmod(remaining, 60)
    st.info(f"⏱️ Time Remaining: **{mins:02d}:{secs:02d}**")

    score = 0
    st.divider()

    # ================= APTITUDE =================
    st.subheader("📊 Section A: Quantitative Aptitude (25 Marks)")

    if st.radio("1. If 20% of a number is 60, the number is:", ["200", "250", "300", "350"]) == "300": score += 4
    if st.radio("2. Average of 12, 18, 24, 30:", ["18", "20", "21", "22"]) == "21": score += 4
    if st.radio("3. Simple Interest formula:", ["PRT/100", "P+RT", "P/T", "PR+T"]) == "PRT/100": score += 4
    if st.radio("4. 15² =", ["125", "200", "225", "250"]) == "225": score += 4
    if st.radio("5. 3 : 6 :: 5 : ?", ["10", "15", "20", "30"]) == "10": score += 4
    if st.radio("6. 144 ÷ 12 =", ["10", "11", "12", "13"]) == "12": score += 5

    # ================= LOGICAL =================
    st.subheader("🧠 Section B: Logical Reasoning (25 Marks)")

    if st.radio("7. Odd one out:", ["Laptop", "Keyboard", "Mouse", "Table"]) == "Table": score += 4
    if st.radio("8. Series: 5, 10, 20, 40, ?", ["60", "70", "80", "90"]) == "80": score += 4
    if st.radio("9. All cats are animals. Some animals are wild. Conclusion?", ["True", "False"]) == "True": score += 4
    if st.radio("10. Mirror of EAST:", ["TSAE", "HSAE", "TSÆ", "EAST"]) == "TSAE": score += 4
    if st.radio("11. Find missing: A, C, E, ?", ["F", "G", "H", "I"]) == "G": score += 4
    if st.radio("12. If A > B and B > C, then:", ["A > C", "C > A"]) == "A > C": score += 5

    # ================= COMPUTER =================
    st.subheader("💻 Section C: Computer Knowledge (25 Marks)")

    if st.radio("13. Binary system uses:", ["0 & 1", "1 & 2", "2 & 3", "0–9"]) == "0 & 1": score += 4
    if st.radio("14. Python is a:", ["Low-level", "High-level", "Machine", "Assembly"]) == "High-level": score += 4
    if st.radio("15. CPU is part of:", ["Software", "Hardware", "Network", "OS"]) == "Hardware": score += 4
    if st.radio("16. AI stands for:", ["Artificial Intelligence", "Advanced Internet"]) == "Artificial Intelligence": score += 4
    if st.radio("17. RAM is:", ["Permanent", "Temporary", "External", "Secondary"]) == "Temporary": score += 4
    if st.radio("18. Which is NOT a programming language?", ["Java", "Python", "HTML", "Oracle"]) == "Oracle": score += 5

    # ================= GK =================
    st.subheader("🌍 Section D: General Knowledge (25 Marks)")

    if st.radio("19. Capital of Tamil Nadu:", ["Chennai", "Madurai", "Trichy", "Salem"]) == "Chennai": score += 4
    if st.radio("20. Father of Computer:", ["Charles Babbage", "Newton"]) == "Charles Babbage": score += 4
    if st.radio("21. ISRO deals with:", ["Space", "Medicine", "Agriculture"]) == "Space": score += 4
    if st.radio("22. National animal of India:", ["Tiger", "Lion", "Elephant"]) == "Tiger": score += 4
    if st.radio("23. UNO headquarters:", ["New York", "London", "Paris"]) == "New York": score += 4
    if st.radio("24. Internet is a:", ["Network", "Device", "Software"]) == "Network": score += 5

    # ================= SUBMIT =================
    if st.button("📊 Submit Test") or st.session_state.submitted:
        st.divider()
        st.header("📄 Exam Result")

        st.success(f"🎯 Score: **{score} / 100**")

        if score >= 75:
            grade = "A"
            degree = "B.Sc Computer Science / CS with AI"
            career = ["Software Engineer", "AI Engineer", "Data Scientist"]
        elif score >= 50:
            grade = "B"
            degree = "BCA / B.Sc / B.Com"
            career = ["Business Analyst", "IT Support", "Banking"]
        else:
            grade = "C"
            degree = "Arts / Management"
            career = ["Administration", "HR", "Creative Fields"]

        st.info(f"🎖 Grade: **{grade}**")
        st.write(f"🎓 Recommended Degree: **{degree}**")
        st.write("💼 Career Paths:")
        for c in career:
            st.write(f"- {c}")

        pdf = generate_pdf(student_name, score, grade, degree, career)
        st.download_button(
            "📥 Download Result PDF",
            pdf,
            file_name="Entrance_Test_Result.pdf",
            mime="application/pdf"
        )

    # ---------------- RESULT ----------------
    if st.button("📊 Submit Exam & View Result"):
        st.header("📄 Exam Result")

        st.write(f"### 🎯 Score: **{score} / 100**")

        if score >= 75:
            grade = "A"
            degree = "B.Sc Computer Science / CS with AI"
            career = ["Software Engineer", "AI Engineer", "Data Scientist"]
            st.success("Grade A – Excellent")
        elif score >= 50:
            grade = "B"
            degree = "B.Sc Mathematics / BCA / B.Com"
            career = ["Data Analyst", "Banking", "Business Analyst"]
            st.warning("Grade B – Good")
        else:
            grade = "C"
            degree = "BA / B.Com / General Degree"
            career = ["Administration", "Creative Fields", "Government Exams"]
            st.error("Grade C – Needs Improvement")

        st.write(f"🎓 **Recommended Degree:** {degree}")
        st.write("💼 **Career Paths:**")
        for cpath in career:
            st.write(f"- {cpath}")

        pdf = generate_pdf(name, score, grade, degree, career)

        st.download_button(
            "📥 Download Result PDF",
            data=pdf,
            file_name="Entrance_Test_Result.pdf",
            mime="application/pdf"
        )


# ---------------- COLLEGE GPT ----------------
elif menu == "🤖 Ask College GPT":
    st.header("🤖 College GPT")
    st.caption("Answers limited to SACAS & CS / CS-AI syllabus")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    for msg in st.session_state.chat:
        st.chat_message(msg["role"]).write(msg["content"])

    user_input = st.chat_input("Ask your question and press Enter")

    if user_input:
        st.session_state.chat.append({"role":"user","content":user_input})

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"You are College GPT for SA College. Answer academically."},
                {"role":"user","content":user_input}
            ]
        )

        reply = res.choices[0].message.content
        st.session_state.chat.append({"role":"assistant","content":reply})
        st.rerun()

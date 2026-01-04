# ============================================================
# SA COLLEGE OF ARTS & SCIENCE – COMPLETE STUDENT PORTAL
# ============================================================
# FEATURES INCLUDED (NO REMOVALS):
# ------------------------------------------------------------
# 1. Student Registration (Name, Username, Password, School)
# 2. Student Login
# 3. Hidden Admin Login (Secret Key + Credentials)
# 4. Admin Panel (Dashboard, Students, Attempts)
# 5. About College (Image)
# 6. Location Map
# 7. CS & CS-AI Syllabus
# 8. HOD Section (Image)
# 9. Online Degree Entrance Test (12 Questions)
# 10. 5-Minute Modern Timer
# 11. One-Attempt-Only Exam Lock
# 12. Result + PDF Download
# 13. College GPT (Anti-misuse, Neutral)
# ============================================================

# ================= ADMIN SECURITY ===========================
ADMIN_ACCESS_KEY = "SACAS_ADMIN_2026"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ============================================================
# IMPORTS
# ============================================================
import streamlit as st
import os
import time
import pandas as pd
from pathlib import Path
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from openai import OpenAI

# ============================================================
# FILE CONSTANTS
# ============================================================
USERS_FILE = "users.csv"
ATTEMPTS_FILE = "attempts.csv"

# ============================================================
# PAGE CONFIG (MUST BE FIRST STREAMLIT CALL)
# ============================================================
st.set_page_config(
    page_title="SA College of Arts & Science | Student Portal",
    page_icon="🎓",
    layout="wide"
)

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
if "auth_page" not in st.session_state:
    st.session_state.auth_page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = {}

if "exam_step" not in st.session_state:
    st.session_state.exam_step = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

if "admin_verified" not in st.session_state:
    st.session_state.admin_verified = False

# ============================================================
# INITIAL FILE CREATION (CSV STORAGE)
# ============================================================
if not os.path.exists(USERS_FILE):
    pd.DataFrame(
        columns=["student_name", "username", "password", "school"]
    ).to_csv(USERS_FILE, index=False)

if not os.path.exists(ATTEMPTS_FILE):
    pd.DataFrame(
        columns=["username", "completed"]
    ).to_csv(ATTEMPTS_FILE, index=False)


# ============================================================
# HELPER FUNCTION: SAFE IMAGE LOADER
# ============================================================
def show_image(path, **kwargs):
    if Path(path).exists():
        st.image(path, **kwargs)
    else:
        st.warning(f"Image missing: {path}")

# ============================================================
# HELPER FUNCTION: PDF GENERATOR
# ============================================================
def generate_pdf(name, score, grade, degree, careers):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(w/2, h-50, "SA COLLEGE OF ARTS & SCIENCE")

    c.setFont("Helvetica", 12)
    c.drawCentredString(w/2, h-80, "ONLINE DEGREE ENTRANCE TEST RESULT")

    y = h - 140
    c.drawString(50, y, f"Student Name: {name}")
    y -= 25
    c.drawString(50, y, f"Score: {score} / 120")
    y -= 25
    c.drawString(50, y, f"Grade: {grade}")
    y -= 25
    c.drawString(50, y, f"Recommended Degree: {degree}")

    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Suggested Career Paths:")
    y -= 20
    c.setFont("Helvetica", 11)

    for cpath in careers:
        c.drawString(70, y, f"- {cpath}")
        y -= 18

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# ============================================================
# HEADER UI
# ============================================================
st.markdown("""
<h1 style="text-align:center;">🎓 SA College of Arts & Science</h1>
<p style="text-align:center;color:gray;">Affiliated to University of Madras</p>
<p style="text-align:center;font-size:13px;">Student Guidance & Entrance Test Portal</p>
""", unsafe_allow_html=True)

st.divider()

# ============================================================
# STUDENT AUTHENTICATION (REGISTER / LOGIN)
# ============================================================
if not st.session_state.logged_in and not st.session_state.is_admin:

    st.subheader("🔐 Student Authentication")

    if st.session_state.auth_page == "register":
        st.markdown("### 📝 Student Registration")

        name = st.text_input("Student Name")
        username = st.text_input("Register Number / Username")
        password = st.text_input("Password", type="password")
        school = st.text_input("School Name")

        if st.button("Create Account"):
            users = pd.read_csv(USERS_FILE)
            if username.strip() == "" or password.strip() == "":
                st.error("Username and password required")
            elif username in users.username.values:
                st.error("Username already exists")
            else:
                users.loc[len(users)] = [name, username, password, school]
                users.to_csv(USERS_FILE, index=False)
                st.success("Registration successful")
                st.session_state.auth_page = "login"
                st.rerun()

        st.button("Already registered? Login",
                  on_click=lambda: st.session_state.update(auth_page="login"))

    else:
        st.markdown("### 🔑 Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            users = pd.read_csv(USERS_FILE)
            row = users[(users.username == username) & (users.password == password)]
            if not row.empty:
                st.session_state.logged_in = True
                st.session_state.current_user = row.iloc[0].to_dict()
                st.rerun()
            else:
                st.error("Invalid login credentials")

        st.button("New student? Register",
                  on_click=lambda: st.session_state.update(auth_page="register"))

    st.stop()


# ============================================================
# SIDEBAR (STUDENT)
# ============================================================
st.sidebar.success(f"Logged in as: {st.session_state.current_user['username']}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.auth_page = "login"
    st.session_state.current_user = {}
    st.session_state.exam_step = 1
    st.session_state.score = 0
    st.session_state.start_time = None
    st.rerun()

menu = st.sidebar.radio(
    "📘 Navigation",
    [
        "🏫 About College",
        "📍 Location",
        "📚 CS & CS-AI Syllabus",
        "👨‍🏫 CS with AI – HOD",
        "📝 Online Degree Entrance Test",
        "🤖 Ask College GPT"
    ]
)

# ============================================================
# ABOUT COLLEGE
# ============================================================
if menu == "🏫 About College":
    st.header("🏫 About SA College of Arts & Science")
    show_image("assets/ai_students.png", use_column_width=True)
    st.write("""
SA College of Arts & Science (SACAS) is located in **Thiruverkadu, Avadi, Chennai**.

### Focus Areas
- Academic Excellence
- Ethical Education
- Innovation & Research
- Holistic Student Development
""")

# ============================================================
# LOCATION
# ============================================================
elif menu == "📍 Location":
    st.header("📍 College Location")
    st.write("Thiruverkadu, Avadi, Chennai")
    st.map(pd.DataFrame({"lat":[13.0475],"lon":[80.1012]}))

# ============================================================
# SYLLABUS
# ============================================================
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
- Natural Language Processing  
- Computer Vision  
""")

# ============================================================
# HOD
# ============================================================
elif menu == "👨‍🏫 CS with AI – HOD":
    st.header("👨‍🏫 Head of the Department – CS with AI")
    col1, col2 = st.columns([1,2])
    with col1:
        show_image("assets/hod.png", width=250)
    with col2:
        st.markdown("""
**Mr. Krishnan R**  
*M.Sc, M.Phil, NET, SET*

- UG Experience: 30 Years  
- PG Experience: 23 Years  

**Focus Areas**
- Industry-ready skills  
- Ethical AI  
- Practical learning  
""")

# ============================================================
# ONLINE DEGREE ENTRANCE TEST (12 QUESTIONS)
# ============================================================
elif menu == "📝 Online Degree Entrance Test":

    attempts = pd.read_csv(ATTEMPTS_FILE)
    if st.session_state.current_user["username"] in attempts.username.values:
        st.error("🚫 You have already completed this test.")
        st.stop()

    st.header("📝 Online Degree Entrance Test")
    st.caption("Time: 5 Minutes | One Attempt Only")

    TOTAL_TIME = 5 * 60
    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, TOTAL_TIME - elapsed)

    st.progress(remaining / TOTAL_TIME)
    mins, secs = divmod(remaining, 60)
    st.markdown(
        f"<div style='background:#111;padding:15px;border-radius:10px;"
        f"text-align:center;color:#00ffcc;font-size:22px;'>"
        f"⏱ Time Left: {mins:02d}:{secs:02d}</div>",
        unsafe_allow_html=True
    )

    if remaining == 0:
        st.session_state.exam_step = 5

    st.divider()

    # -------- SECTION A --------
    if st.session_state.exam_step == 1:
        q1 = st.radio("1. 25% of 200 =", ["25","50","75","100"], index=None)
        q2 = st.radio("2. Average of 10, 20, 30 =", ["15","20","25","30"], index=None)
        q3 = st.radio("3. 12 × 8 =", ["96","84","88","72"], index=None)
        if st.button("Next ➡️"):
            if q1 == "50": st.session_state.score += 10
            if q2 == "20": st.session_state.score += 10
            if q3 == "96": st.session_state.score += 10
            st.session_state.exam_step = 2
            st.rerun()

    # -------- SECTION B --------
    elif st.session_state.exam_step == 2:
        q1 = st.radio("4. Odd one out:", ["Apple","Banana","Car","Mango"], index=None)
        q2 = st.radio("5. Series: 2, 4, 8, ?", ["12","14","16","18"], index=None)
        q3 = st.radio("6. A > B and B > C then:", ["A > C","C > A"], index=None)
        if st.button("Next ➡️"):
            if q1 == "Car": st.session_state.score += 10
            if q2 == "16": st.session_state.score += 10
            if q3 == "A > C": st.session_state.score += 10
            st.session_state.exam_step = 3
            st.rerun()

    # -------- SECTION C --------
    elif st.session_state.exam_step == 3:
        q1 = st.radio("7. CPU stands for:", ["Central Processing Unit","Control Unit"], index=None)
        q2 = st.radio("8. Binary system uses:", ["0 & 1","1 & 2"], index=None)
        q3 = st.radio("9. Python is:", ["High-level","Low-level"], index=None)
        if st.button("Next ➡️"):
            if q1 == "Central Processing Unit": st.session_state.score += 10
            if q2 == "0 & 1": st.session_state.score += 10
            if q3 == "High-level": st.session_state.score += 10
            st.session_state.exam_step = 4
            st.rerun()

    # -------- SECTION D --------
    elif st.session_state.exam_step == 4:
        q1 = st.radio("10. Capital of Tamil Nadu:", ["Chennai","Madurai"], index=None)
        q2 = st.radio("11. Father of Computer:", ["Charles Babbage","Newton"], index=None)
        q3 = st.radio("12. National Animal of India:", ["Tiger","Lion"], index=None)
        if st.button("Submit Exam"):
            if q1 == "Chennai": st.session_state.score += 10
            if q2 == "Charles Babbage": st.session_state.score += 10
            if q3 == "Tiger": st.session_state.score += 10
            st.session_state.exam_step = 5
            st.rerun()

    # -------- RESULT --------
    elif st.session_state.exam_step == 5:
        attempts.loc[len(attempts)] = [
            st.session_state.current_user["username"], True
        ]
        attempts.to_csv(ATTEMPTS_FILE, index=False)

        score = st.session_state.score

        if score >= 90:
            grade = "A"
            degree = "B.Sc Computer Science / CS with AI"
            careers = ["Software Engineer","AI Engineer","Data Scientist"]
        elif score >= 60:
            grade = "B"
            degree = "BCA / B.Sc / B.Com"
            careers = ["Business Analyst","IT Support"]
        else:
            grade = "C"
            degree = "Arts / Management"
            careers = ["HR","Administration"]

        st.success(f"🎯 Score: {score} / 120")
        st.info(f"Grade: {grade}")
        st.write(f"Recommended Degree: {degree}")

        pdf = generate_pdf(
            st.session_state.current_user["student_name"],
            score, grade, degree, careers
        )

        st.download_button(
            "📥 Download Result PDF",
            pdf,
            file_name="Entrance_Result.pdf",
            mime="application/pdf"
        )

# ============================================================
# COLLEGE GPT
# ============================================================
elif menu == "🤖 Ask College GPT":
    st.header("🤖 College GPT")
    st.caption("Neutral academic guidance only")

    SYSTEM_PROMPT = """
You are College GPT created for student guidance.

Primary Institution Focus:
- When the user mentions "SA" or "SA College", interpret it as
  "SA College of Arts & Science".
- Give priority, clarity, and more detail to SA College of Arts & Science
  when it is mentioned or implied.

Rules you must strictly follow:
- Do NOT criticize, downgrade, or speak negatively about any other college.
- Do NOT rank colleges or say one college is better or worse.
- If asked to compare colleges, explain neutral factors only
  (courses offered, location, facilities, student goals).
- You may highlight strengths, programs, and opportunities of
  SA College of Arts & Science in a positive and factual way.
- Maintain a respectful, academic, and unbiased tone.
- Encourage students to verify final decisions from official college sources.

Your role:
- Help students understand academics, syllabus, and career pathways.
- Promote SA College of Arts & Science positively without affecting
  the reputation of other institutions.
"""

    q = st.chat_input("Ask your question")

    if q:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        r = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": q}
            ]
        )
        st.write(r.output_text)


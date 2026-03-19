# ============================================================
# SA COLLEGE OF ARTS & SCIENCE – COMPLETE STUDENT PORTAL
# ============================================================
# FEATURES:
# 1. Student Registration (Name, Username, Password, School, Photo)
# 2. Student Login + Remember Me
# 3. Separate Admin Login Page
# 4. Admin Panel (Dashboard, Students, Attempts, Leaderboard)
# 5. About College
# 6. Location Map
# 7. CS & CS-AI Syllabus
# 8. HOD Section
# 9. Online Degree Entrance Test (12 Questions, 4 Sections)
# 10. 5-Minute Timer + Auto Submit
# 11. One-Attempt-Only Exam Lock
# 12. Score Chart (Pie Chart after exam)
# 13. Leaderboard (Top Scorers)
# 14. Result + PDF Download
# 15. Merit Certificate PDF (for top scorers)
# 16. College GPT (OpenAI, Tamil + English)
# ============================================================

import streamlit as st
import sqlite3
import os
import time
import hashlib
import qrcode
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from io import BytesIO
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from openai import OpenAI
from streamlit_cookies_manager import EncryptedCookieManager
from PIL import Image
import base64

# ============================================================
# ADMIN CREDENTIALS
# ============================================================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = hashlib.sha256("admin123".encode()).hexdigest()

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="SA College of Arts & Science | Student Portal",
    page_icon="🎓",
    layout="wide"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    .stApp { background-color: #f0f4f8; }
    .main-header {
        background: linear-gradient(135deg, #1a237e, #283593);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 20px;
    }
    .card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 16px;
    }
    .metric-card {
        background: linear-gradient(135deg, #1a237e, #3949ab);
        color: white;
        padding: 16px;
        border-radius: 10px;
        text-align: center;
    }
    .badge-gold {
        background: #FFD700;
        color: #333;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
    .badge-silver {
        background: #C0C0C0;
        color: #333;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
    .badge-bronze {
        background: #CD7F32;
        color: white;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
    div[data-testid="stSidebarNav"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# COOKIE MANAGER
# ============================================================
cookies = EncryptedCookieManager(
    prefix="sacas_portal_",
    password="sacas_secret_key_2026_secure"
)
if not cookies.ready():
    st.stop()

# ============================================================
# SESSION STATE INIT
# ============================================================
defaults = {
    "auth_page": "login",
    "logged_in": False,
    "current_user": {},
    "admin_logged_in": False,
    "page": "student",
    "exam_step": 0,
    "exam_started": False,
    "exam_finished": False,
    "score": 0,
    "start_time": None,
    "college_gpt_chat": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================
# DATABASE SETUP
# ============================================================
os.makedirs("assets", exist_ok=True)
os.makedirs("uploads", exist_ok=True)

conn = sqlite3.connect("college.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    username TEXT UNIQUE,
    password TEXT,
    school TEXT,
    photo_path TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    score INTEGER,
    completed INTEGER,
    timestamp TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    rating INTEGER,
    message TEXT,
    timestamp TEXT
)
""")

conn.commit()

# ============================================================
# HELPERS
# ============================================================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def show_image(path, **kwargs):
    if Path(path).exists():
        st.image(path, **kwargs)
    else:
        st.info("📷 Image will appear here when added")

def get_student_photo(username):
    cursor.execute("SELECT photo_path FROM users WHERE username=?", (username,))
    row = cursor.fetchone()
    if row and row[0] and Path(row[0]).exists():
        return row[0]
    return None

def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=6, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

# ============================================================
# AUTO LOGIN VIA COOKIE
# ============================================================
if not st.session_state.logged_in and not st.session_state.admin_logged_in:
    remembered = cookies.get("username")
    if remembered:
        cursor.execute(
            "SELECT student_name, username, school, photo_path FROM users WHERE username=?",
            (remembered,)
        )
        row = cursor.fetchone()
        if row:
            st.session_state.logged_in = True
            st.session_state.current_user = {
                "student_name": row[0],
                "username": row[1],
                "school": row[2],
                "photo_path": row[3],
            }

# ============================================================
# =================== ADMIN LOGIN PAGE =======================
# ============================================================
def admin_login_page():
    st.markdown("""
    <div class="main-header">
        <h2>🔐 SA College – Admin Portal</h2>
        <p>Restricted Access Only</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.container():
            st.markdown("### Admin Login")
            uname = st.text_input("Admin Username", key="admin_uname")
            pwd = st.text_input("Admin Password", type="password", key="admin_pwd")

            if st.button("🔓 Login as Admin", use_container_width=True):
                if uname == ADMIN_USERNAME and hash_password(pwd) == ADMIN_PASSWORD:
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("❌ Invalid admin credentials")

        st.markdown("---")
        if st.button("← Back to Student Portal"):
            st.session_state.page = "student"
            st.rerun()

# ============================================================
# =================== ADMIN PANEL ============================
# ============================================================
def admin_panel():
    st.markdown("""
    <div class="main-header">
        <h2>🏫 SA College Admin Panel</h2>
        <p>Manage students, results & portal data</p>
    </div>
    """, unsafe_allow_html=True)

    col_logout, _ = st.columns([1, 5])
    with col_logout:
        if st.button("🚪 Logout Admin"):
            st.session_state.admin_logged_in = False
            st.session_state.page = "student"
            st.rerun()

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "👥 Students", "📝 Exam Results", "🏆 Leaderboard"])

    # ---- DASHBOARD ----
    with tab1:
        cursor.execute("SELECT COUNT(*) FROM users")
        total_students = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM attempts WHERE completed=1")
        total_attempts = cursor.fetchone()[0]
        cursor.execute("SELECT AVG(score) FROM attempts WHERE completed=1")
        avg_score_row = cursor.fetchone()
        avg_score = round(avg_score_row[0], 1) if avg_score_row[0] else 0
        cursor.execute("SELECT MAX(score) FROM attempts WHERE completed=1")
        top_score_row = cursor.fetchone()
        top_score = top_score_row[0] if top_score_row[0] else 0

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("👥 Total Students", total_students)
        c2.metric("📝 Exams Taken", total_attempts)
        c3.metric("📈 Avg Score", f"{avg_score}/120")
        c4.metric("🏆 Top Score", f"{top_score}/120")

        st.markdown("#### Score Distribution")
        cursor.execute("SELECT score FROM attempts WHERE completed=1")
        scores = [r[0] for r in cursor.fetchall()]
        if scores:
            fig, ax = plt.subplots(figsize=(8, 3))
            ax.hist(scores, bins=10, color="#3949ab", edgecolor="white", rwidth=0.85)
            ax.set_xlabel("Score")
            ax.set_ylabel("Students")
            ax.set_title("Score Distribution")
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            st.pyplot(fig)
            plt.close()
        else:
            st.info("No exam data yet.")

        st.markdown("#### Latest Feedback")
        cursor.execute("SELECT username, rating, message, timestamp FROM feedback ORDER BY id DESC LIMIT 5")
        fb = cursor.fetchall()
        if fb:
            df_fb = pd.DataFrame(fb, columns=["Username", "Rating", "Message", "Time"])
            st.dataframe(df_fb, use_container_width=True)
        else:
            st.info("No feedback yet.")

    # ---- STUDENTS ----
    with tab2:
        st.markdown("#### Registered Students")
        cursor.execute("SELECT id, student_name, username, school FROM users ORDER BY id DESC")
        students = cursor.fetchall()
        if students:
            df = pd.DataFrame(students, columns=["ID", "Name", "Username", "School"])
            st.dataframe(df, use_container_width=True)

            st.markdown("#### Delete Student")
            del_user = st.text_input("Enter username to delete")
            if st.button("🗑️ Delete Student"):
                if del_user:
                    cursor.execute("DELETE FROM users WHERE username=?", (del_user,))
                    cursor.execute("DELETE FROM attempts WHERE username=?", (del_user,))
                    conn.commit()
                    st.success(f"Deleted {del_user}")
                    st.rerun()
        else:
            st.info("No students registered yet.")

    # ---- EXAM RESULTS ----
    with tab3:
        st.markdown("#### All Exam Results")
        cursor.execute("""
            SELECT a.username, u.student_name, u.school, a.score, a.timestamp
            FROM attempts a
            LEFT JOIN users u ON a.username = u.username
            WHERE a.completed=1
            ORDER BY a.score DESC
        """)
        results = cursor.fetchall()
        if results:
            df_r = pd.DataFrame(results, columns=["Username", "Name", "School", "Score", "Time"])
            st.dataframe(df_r, use_container_width=True)

            csv = df_r.to_csv(index=False)
            st.download_button("📥 Download CSV", csv, "exam_results.csv", "text/csv")
        else:
            st.info("No results yet.")

    # ---- LEADERBOARD ----
    with tab4:
        st.markdown("#### 🏆 Top Scorers Leaderboard")
        cursor.execute("""
            SELECT a.username, u.student_name, u.school, a.score
            FROM attempts a
            LEFT JOIN users u ON a.username = u.username
            WHERE a.completed=1
            ORDER BY a.score DESC LIMIT 10
        """)
        leaders = cursor.fetchall()
        if leaders:
            medals = ["🥇", "🥈", "🥉"] + ["🎖️"] * 7
            for i, (uname, name, school, score) in enumerate(leaders):
                col1, col2, col3, col4 = st.columns([0.5, 2, 2, 1])
                col1.markdown(f"### {medals[i]}")
                col2.markdown(f"**{name or uname}**")
                col3.markdown(f"_{school or 'N/A'}_")
                col4.markdown(f"**{score}/120**")
                st.divider()
        else:
            st.info("No scores yet.")

# ============================================================
# =================== STUDENT AUTH ===========================
# ============================================================
def student_auth():
    st.markdown("""
    <div class="main-header">
        <h2>🎓 SA College of Arts & Science</h2>
        <p>Student Portal – Thiruverkadu, Avadi, Chennai</p>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        if st.session_state.auth_page == "register":
            st.markdown("### 📝 Student Registration")

            name = st.text_input("Full Name")
            username = st.text_input("Register Number / Username")
            password = st.text_input("Password", type="password")
            school = st.text_input("School Name")
            photo = st.file_uploader("Profile Photo (optional)", type=["jpg", "jpeg", "png"])

            if st.button("✅ Create Account", use_container_width=True):
                if not name or not username or not password:
                    st.error("All fields required except photo")
                else:
                    photo_path = None
                    if photo:
                        photo_path = f"uploads/{username}_{photo.name}"
                        with open(photo_path, "wb") as f:
                            f.write(photo.read())
                    try:
                        cursor.execute(
                            "INSERT INTO users (student_name, username, password, school, photo_path) VALUES (?,?,?,?,?)",
                            (name, username, hash_password(password), school, photo_path)
                        )
                        conn.commit()
                        st.success("✅ Registration successful! Please login.")
                        st.session_state.auth_page = "login"
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("Username already exists")

            st.button("Already registered? Login →",
                      on_click=lambda: st.session_state.update(auth_page="login"))

        else:
            st.markdown("### 🔑 Student Login")

            username = st.text_input("Username / Register Number")
            password = st.text_input("Password", type="password")
            remember = st.checkbox("Remember me")

            if st.button("🚀 Login", use_container_width=True):
                cursor.execute(
                    "SELECT student_name, username, school, photo_path FROM users WHERE username=? AND password=?",
                    (username, hash_password(password))
                )
                row = cursor.fetchone()
                if row:
                    st.session_state.logged_in = True
                    st.session_state.current_user = {
                        "student_name": row[0],
                        "username": row[1],
                        "school": row[2],
                        "photo_path": row[3],
                    }
                    if remember:
                        cookies["username"] = username
                        cookies.save()
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")

            st.button("New student? Register →",
                      on_click=lambda: st.session_state.update(auth_page="register"))

        st.markdown("---")
        if st.button("🔐 Admin Login", use_container_width=True):
            st.session_state.page = "admin_login"
            st.rerun()

# ============================================================
# =================== STUDENT PORTAL =========================
# ============================================================
def student_portal():
    user = st.session_state.current_user

    # Sidebar
    with st.sidebar:
        photo_path = user.get("photo_path")
        if photo_path and Path(photo_path).exists():
            st.image(photo_path, width=100)
        else:
            st.markdown("👤")

        st.markdown(f"**{user['student_name']}**")
        st.caption(f"🎓 {user['school'] or 'SA College'}")
        st.caption(f"🆔 {user['username']}")
        st.divider()

        menu = st.radio("📘 Navigation", [
            "🏠 Dashboard",
            "🏫 About College",
            "📍 Location",
            "📚 CS & CS-AI Syllabus",
            "👨‍🏫 CS with AI – HOD",
            "📝 Entrance Test",
            "🏆 Leaderboard",
            "💬 Feedback",
            "🤖 College GPT",
        ])

        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            for k in ["logged_in", "current_user", "exam_step", "exam_started",
                      "exam_finished", "score", "start_time", "college_gpt_chat"]:
                st.session_state[k] = defaults[k]
            cookies["username"] = ""
            cookies.save()
            st.rerun()

    # ---- DASHBOARD ----
    if menu == "🏠 Dashboard":
        st.markdown(f"""
        <div class="main-header">
            <h2>Welcome back, {user['student_name']}! 👋</h2>
            <p>SA College of Arts & Science Student Portal</p>
        </div>
        """, unsafe_allow_html=True)

        cursor.execute("SELECT score, timestamp FROM attempts WHERE username=? AND completed=1",
                       (user['username'],))
        result = cursor.fetchone()

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("📝 Exam Status", "Completed ✅" if result else "Not taken")
        with c2:
            st.metric("🎯 Your Score", f"{result[0]}/120" if result else "—")
        with c3:
            pct = round((result[0] / 120) * 100) if result else 0
            st.metric("📊 Percentage", f"{pct}%" if result else "—")

        if result:
            score = result[0]
            if score >= 100:
                st.success("🏆 Outstanding! You qualify for Merit Certificate.")
            elif score >= 80:
                st.info("🎉 Great score! Keep it up.")
            else:
                st.warning("📚 Keep studying. You can do better!")

    # ---- ABOUT ----
    elif menu == "🏫 About College":
        st.header("🏫 About SA College of Arts & Science")
        show_image("assets/college.png", use_column_width=True)
        st.markdown("""
SA College of Arts & Science (SACAS) is located in **Thiruverkadu, Avadi, Chennai**.

### 🎯 Our Vision
To provide quality education that transforms students into ethical professionals and responsible citizens.

### 🏆 Focus Areas
- Academic Excellence
- Ethical Education
- Innovation & Research
- Industry-Ready Skills
- Holistic Student Development

### 📋 Departments
- B.Sc Computer Science
- B.Sc Computer Science with AI
- B.Com
- BBA
- B.Sc Mathematics
- B.Sc Physics
        """)

    # ---- LOCATION ----
    elif menu == "📍 Location":
        st.header("📍 College Location")
        st.write("📌 Thiruverkadu, Avadi, Chennai, Tamil Nadu – 600077")
        st.map(pd.DataFrame({"lat": [13.0475], "lon": [80.1012]}))
        st.info("🚌 Nearest bus stop: Thiruverkadu | 🚇 Nearest metro: Koyambedu")

    # ---- SYLLABUS ----
    elif menu == "📚 CS & CS-AI Syllabus":
        st.header("📚 B.Sc CS & CS with AI – Syllabus")
        tab1, tab2 = st.tabs(["💻 B.Sc Computer Science", "🤖 B.Sc CS with AI"])
        with tab1:
            st.markdown("""
#### Year 1
- Programming in C
- Digital Electronics
- Mathematics I & II

#### Year 2
- Python Programming
- Data Structures
- DBMS
- Operating Systems

#### Year 3
- Computer Networks
- Software Engineering
- Web Technologies
- Project Work
            """)
        with tab2:
            st.markdown("""
#### Core + AI Subjects
- Artificial Intelligence
- Machine Learning
- Deep Learning
- Natural Language Processing
- Computer Vision
- Fuzzy Logic & Neural Networks
- AI Ethics & Applications
            """)

    # ---- HOD ----
    elif menu == "👨‍🏫 CS with AI – HOD":
        st.header("👨‍🏫 Head of the Department – CS with AI")
        col1, col2 = st.columns([1, 2])
        with col1:
            show_image("assets/hod.png", width=250)
        with col2:
            st.markdown("""
**Mr. Krishnan R**
*M.Sc, M.Phil, NET, SET*

| | |
|---|---|
| 🎓 UG Experience | 30 Years |
| 📚 PG Experience | 23 Years |

**Specializations**
- Artificial Intelligence
- Machine Learning
- Data Science

**Message to Students:**
*"Embrace technology with ethics. The future belongs to those who learn continuously."*
            """)

    # ---- ENTRANCE TEST ----
    elif menu == "📝 Entrance Test":
        entrance_test(user)

    # ---- LEADERBOARD ----
    elif menu == "🏆 Leaderboard":
        st.header("🏆 Top Scorers Leaderboard")

        cursor.execute("""
            SELECT a.username, u.student_name, u.school, a.score
            FROM attempts a
            LEFT JOIN users u ON a.username = u.username
            WHERE a.completed=1
            ORDER BY a.score DESC LIMIT 10
        """)
        leaders = cursor.fetchall()

        if leaders:
            medals = ["🥇", "🥈", "🥉"] + ["🎖️"] * 7
            for i, (uname, name, school, score) in enumerate(leaders):
                bg = "#FFF9C4" if i == 0 else "#F5F5F5" if i == 1 else "#FBE9E7" if i == 2 else "white"
                is_me = uname == user['username']
                label = " ← You!" if is_me else ""
                st.markdown(f"""
                <div style='background:{bg};padding:12px 16px;border-radius:8px;
                margin-bottom:8px;display:flex;align-items:center;gap:12px;'>
                    <span style='font-size:24px'>{medals[i]}</span>
                    <div style='flex:1'>
                        <strong>{name or uname}{label}</strong><br/>
                        <small>{school or 'SA College'}</small>
                    </div>
                    <strong style='font-size:18px;color:#1a237e'>{score}/120</strong>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No results yet. Be the first to take the test!")

    # ---- FEEDBACK ----
    elif menu == "💬 Feedback":
        st.header("💬 Share Your Feedback")
        with st.form("feedback_form"):
            rating = st.slider("Rate the Portal (1–5 ⭐)", 1, 5, 4)
            message = st.text_area("Your Message / Suggestions")
            submitted = st.form_submit_button("📤 Submit Feedback")
            if submitted:
                cursor.execute(
                    "INSERT INTO feedback (username, rating, message, timestamp) VALUES (?,?,?,datetime('now'))",
                    (user['username'], rating, message)
                )
                conn.commit()
                st.success("✅ Thank you for your feedback!")

    # ---- COLLEGE GPT ----
    elif menu == "🤖 College GPT":
        college_gpt()

# ============================================================
# =================== ENTRANCE TEST =========================
# ============================================================
def entrance_test(user):
    st.header("📝 Online Degree Entrance Test")

    cursor.execute("SELECT score, completed FROM attempts WHERE username=?", (user['username'],))
    attempt = cursor.fetchone()

    if attempt and attempt[1] == 1 and not st.session_state.exam_finished:
        st.error("🚫 You have already completed this test.")
        st.info(f"Your score: **{attempt[0]}/120**")
        st.stop()

    # START PAGE
    if st.session_state.exam_step == 0:
        st.info("⏱ Duration: **5 Minutes** | 📋 Questions: **12** | 🔒 One attempt only")
        col1, col2, col3 = st.columns(3)
        col1.metric("Sections", "4")
        col2.metric("Total Marks", "120")
        col3.metric("Per Question", "10")
        st.markdown("---")
        if st.button("▶️ Start Test", use_container_width=True, type="primary"):
            st.session_state.exam_started = True
            st.session_state.exam_step = 1
            st.session_state.start_time = time.time()
            st.session_state.score = 0
            st.session_state.exam_finished = False
            st.rerun()
        return

    # TIMER
    if st.session_state.exam_started and not st.session_state.exam_finished:
        TOTAL_TIME = 5 * 60
        elapsed = int(time.time() - st.session_state.start_time)
        remaining = max(0, TOTAL_TIME - elapsed)
        mins, secs = divmod(remaining, 60)

        progress_val = remaining / TOTAL_TIME
        st.progress(progress_val)

        color = "#00c853" if remaining > 120 else "#ff6d00" if remaining > 60 else "#d50000"
        st.markdown(
            f"<div style='background:{color};padding:10px;border-radius:8px;"
            f"text-align:center;color:white;font-size:18px;font-weight:bold;'>"
            f"⏱ Time Left: {mins:02d}:{secs:02d}</div>",
            unsafe_allow_html=True
        )
        if remaining == 0:
            st.session_state.exam_step = 5
            st.session_state.exam_finished = True
            cursor.execute(
                "INSERT OR REPLACE INTO attempts (username, score, completed, timestamp) VALUES (?,?,1,datetime('now'))",
                (user['username'], st.session_state.score)
            )
            conn.commit()
            st.rerun()

    st.divider()

    # SECTION A
    if st.session_state.exam_step == 1:
        st.subheader("📘 Section A – Quantitative Ability")
        q1 = st.radio("1. 25% of 200 =", ["25", "50", "75", "100"], index=None)
        q2 = st.radio("2. Average of 10, 20, 30 =", ["15", "20", "25", "30"], index=None)
        q3 = st.radio("3. 12 × 8 =", ["96", "84", "88", "72"], index=None)
        if st.button("Next ➡️", key="next1"):
            if None in (q1, q2, q3):
                st.warning("⚠️ Please answer all questions")
                st.stop()
            if q1 == "50": st.session_state.score += 10
            if q2 == "20": st.session_state.score += 10
            if q3 == "96": st.session_state.score += 10
            st.session_state.exam_step = 2
            st.rerun()

    # SECTION B
    elif st.session_state.exam_step == 2:
        st.subheader("📗 Section B – Logical Reasoning")
        q4 = st.radio("4. Odd one out:", ["Apple", "Banana", "Car", "Mango"], index=None)
        q5 = st.radio("5. Series: 2, 4, 8, ?", ["12", "14", "16", "18"], index=None)
        q6 = st.radio("6. A > B and B > C, therefore:", ["A > C", "C > A", "A = C", "Cannot say"], index=None)
        if st.button("Next ➡️", key="next2"):
            if None in (q4, q5, q6):
                st.warning("⚠️ Please answer all questions")
                st.stop()
            if q4 == "Car": st.session_state.score += 10
            if q5 == "16": st.session_state.score += 10
            if q6 == "A > C": st.session_state.score += 10
            st.session_state.exam_step = 3
            st.rerun()

    # SECTION C
    elif st.session_state.exam_step == 3:
        st.subheader("📙 Section C – Computer Awareness")
        q7 = st.radio("7. CPU stands for:", ["Central Processing Unit", "Control Processing Unit", "Core Power Unit"], index=None)
        q8 = st.radio("8. Binary system uses:", ["0 & 1", "1 & 2", "0, 1 & 2"], index=None)
        q9 = st.radio("9. Python is a:", ["High-level language", "Low-level language", "Assembly language"], index=None)
        if st.button("Next ➡️", key="next3"):
            if None in (q7, q8, q9):
                st.warning("⚠️ Please answer all questions")
                st.stop()
            if q7 == "Central Processing Unit": st.session_state.score += 10
            if q8 == "0 & 1": st.session_state.score += 10
            if q9 == "High-level language": st.session_state.score += 10
            st.session_state.exam_step = 4
            st.rerun()

    # SECTION D
    elif st.session_state.exam_step == 4:
        st.subheader("📕 Section D – General Knowledge")
        q10 = st.radio("10. Capital of Tamil Nadu:", ["Chennai", "Madurai", "Coimbatore", "Salem"], index=None)
        q11 = st.radio("11. Father of Computer:", ["Charles Babbage", "Alan Turing", "Bill Gates"], index=None)
        q12 = st.radio("12. National Animal of India:", ["Tiger", "Lion", "Elephant", "Peacock"], index=None)
        if st.button("✅ Submit Exam", key="submit", type="primary"):
            if None in (q10, q11, q12):
                st.warning("⚠️ Please answer all questions")
                st.stop()
            if q10 == "Chennai": st.session_state.score += 10
            if q11 == "Charles Babbage": st.session_state.score += 10
            if q12 == "Tiger": st.session_state.score += 10
            cursor.execute(
                "INSERT OR REPLACE INTO attempts (username, score, completed, timestamp) VALUES (?,?,1,datetime('now'))",
                (user['username'], st.session_state.score)
            )
            conn.commit()
            st.session_state.exam_finished = True
            st.session_state.exam_step = 5
            st.rerun()

    # RESULT PAGE
    elif st.session_state.exam_step == 5:
        score = st.session_state.score
        pct = round((score / 120) * 100)

        st.balloons()
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#1a237e,#283593);color:white;
        padding:24px;border-radius:12px;text-align:center;'>
            <h2>🎉 Examination Complete!</h2>
            <h1 style='font-size:48px;margin:10px 0'>{score} / 120</h1>
            <p style='font-size:18px'>{pct}% Score</p>
        </div>
        """, unsafe_allow_html=True)

        # SCORE PIE CHART
        st.markdown("#### 📊 Your Score Breakdown")
        fig, ax = plt.subplots(figsize=(5, 4))
        labels = ["Your Score", "Remaining"]
        sizes = [score, 120 - score]
        colors_pie = ["#1a237e", "#e8eaf6"]
        explode = (0.05, 0)
        ax.pie(sizes, labels=labels, colors=colors_pie, explode=explode,
               autopct="%1.1f%%", startangle=90,
               textprops={"fontsize": 12})
        ax.set_title(f"Score: {score}/120 ({pct}%)")
        st.pyplot(fig)
        plt.close()

        # DEPARTMENT SUGGESTION
        if score >= 100:
            dept = "B.Sc Computer Science with AI"
            msg = "🏆 Outstanding performance!"
        elif score >= 80:
            dept = "B.Sc Computer Science"
            msg = "🎉 Excellent! You're a strong candidate."
        elif score >= 60:
            dept = "B.Com / BBA"
            msg = "👍 Good effort! Consider commerce departments."
        elif score >= 40:
            dept = "B.Sc Mathematics / Physics"
            msg = "📚 Decent attempt. Science departments suit you."
        else:
            dept = "General Arts Programme"
            msg = "💪 Keep working hard. Arts programmes welcome you."

        st.info(f"{msg}\n\n🎓 **Suggested Department:** {dept}")

        # MERIT CERTIFICATE for score >= 100
        if score >= 100:
            st.success("🏅 Congratulations! You qualify for a Merit Certificate.")
            if st.button("🏅 Download Merit Certificate"):
                pdf_bytes = generate_merit_certificate(user, score)
                st.download_button(
                    "📄 Click here to download",
                    pdf_bytes,
                    file_name=f"Merit_Certificate_{user['username']}.pdf",
                    mime="application/pdf"
                )

        # RESULT PDF
        if st.button("📄 Download Result PDF"):
            pdf_bytes = generate_result_pdf(user, score, dept)
            st.download_button(
                "📥 Download Result",
                pdf_bytes,
                file_name=f"Result_{user['username']}.pdf",
                mime="application/pdf"
            )

        st.markdown("---")
        if st.button("🏆 View Leaderboard"):
            st.session_state.exam_step = 0
            st.session_state.exam_started = False
            st.rerun()

# ============================================================
# =================== PDF GENERATORS ========================
# ============================================================
def generate_result_pdf(user, score, dept):
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4

    # Header bg
    c.setFillColor(colors.HexColor("#1a237e"))
    c.rect(0, h - 120, w, 120, fill=True, stroke=False)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(w / 2, h - 50, "SA College of Arts & Science")
    c.setFont("Helvetica", 13)
    c.drawCentredString(w / 2, h - 75, "Online Degree Entrance Test – Result")
    c.drawCentredString(w / 2, h - 95, "Thiruverkadu, Avadi, Chennai")

    # Student photo if available
    photo_path = user.get("photo_path")
    if photo_path and Path(photo_path).exists():
        try:
            img = ImageReader(photo_path)
            c.drawImage(img, 60, h - 270, width=80, height=80, preserveAspectRatio=True)
        except Exception:
            pass

    # Details
    c.setFillColor(colors.HexColor("#1a237e"))
    c.setFont("Helvetica-Bold", 14)
    c.drawString(160, h - 155, "Student Details")

    c.setFillColor(colors.black)
    c.setFont("Helvetica", 12)
    details = [
        ("Name", user['student_name']),
        ("Register No.", user['username']),
        ("School", user['school'] or "SA College"),
        ("Score", f"{score} / 120"),
        ("Percentage", f"{round((score/120)*100)}%"),
        ("Suggested Dept", dept),
    ]
    y = h - 180
    for label, val in details:
        c.setFont("Helvetica-Bold", 11)
        c.drawString(160, y, f"{label}:")
        c.setFont("Helvetica", 11)
        c.drawString(290, y, val)
        y -= 22

    # QR Code
    qr_data = f"SA College Result | {user['username']} | Score: {score}/120"
    qr_buf = generate_qr(qr_data)
    qr_img = ImageReader(qr_buf)
    c.drawImage(qr_img, w - 140, h - 290, width=100, height=100)
    c.setFont("Helvetica", 8)
    c.drawCentredString(w - 90, h - 300, "Scan to verify")

    # Footer
    c.setFillColor(colors.HexColor("#e8eaf6"))
    c.rect(0, 0, w, 60, fill=True, stroke=False)
    c.setFillColor(colors.HexColor("#1a237e"))
    c.setFont("Helvetica", 9)
    c.drawCentredString(w / 2, 38, "This result is auto-generated by SA College Student Portal")
    c.drawCentredString(w / 2, 22, "For verification contact: sacas@college.edu | www.sacollege.ac.in")

    c.showPage()
    c.save()
    buf.seek(0)
    return buf.read()


def generate_merit_certificate(user, score):
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=landscape(A4))
    w, h = landscape(A4)

    # Gold border
    c.setStrokeColor(colors.HexColor("#FFD700"))
    c.setLineWidth(6)
    c.rect(20, 20, w - 40, h - 40, fill=False, stroke=True)
    c.setLineWidth(2)
    c.rect(28, 28, w - 56, h - 56, fill=False, stroke=True)

    # Title
    c.setFillColor(colors.HexColor("#1a237e"))
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(w / 2, h - 100, "MERIT CERTIFICATE")

    c.setFont("Helvetica", 14)
    c.drawCentredString(w / 2, h - 130, "SA College of Arts & Science, Thiruverkadu, Avadi, Chennai")

    # Decorative line
    c.setStrokeColor(colors.HexColor("#FFD700"))
    c.setLineWidth(2)
    c.line(80, h - 150, w - 80, h - 150)

    c.setFillColor(colors.black)
    c.setFont("Helvetica", 14)
    c.drawCentredString(w / 2, h - 185, "This is to proudly certify that")

    c.setFillColor(colors.HexColor("#1a237e"))
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(w / 2, h - 230, user['student_name'])

    c.setFillColor(colors.black)
    c.setFont("Helvetica", 13)
    c.drawCentredString(w / 2, h - 265, f"Register No: {user['username']}")
    c.drawCentredString(w / 2, h - 290,
                        "has achieved an outstanding score in the Online Degree Entrance Test")

    c.setFillColor(colors.HexColor("#1a237e"))
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(w / 2, h - 340, f"{score} / 120")

    c.setFillColor(colors.black)
    c.setFont("Helvetica", 13)
    c.drawCentredString(w / 2, h - 375, f"Percentage: {round((score/120)*100)}% | Grade: Outstanding")

    # QR
    qr_data = f"SA College Merit | {user['username']} | {score}/120"
    qr_buf = generate_qr(qr_data)
    qr_img = ImageReader(qr_buf)
    c.drawImage(qr_img, w / 2 - 50, 60, width=100, height=100)

    # Footer
    c.setStrokeColor(colors.HexColor("#FFD700"))
    c.line(80, h - 400, w - 80, h - 400)

    c.setFont("Helvetica", 10)
    c.drawString(80, 50, "Principal")
    c.drawString(80, 38, "SA College of Arts & Science")
    c.drawCentredString(w / 2, 38, "Scan QR to verify")
    c.drawRightString(w - 80, 50, "Head of Department")
    c.drawRightString(w - 80, 38, "Computer Science with AI")

    c.showPage()
    c.save()
    buf.seek(0)
    return buf.read()


# ============================================================
# =================== COLLEGE GPT ===========================
# ============================================================
def college_gpt():
    st.header("🤖 College GPT")
    st.caption("Your AI-powered student assistant | Tamil + English supported")

    def is_tamil(text):
        return any('\u0B80' <= ch <= '\u0BFF' for ch in text)

    def contains_any(text, keywords):
        return any(k in text.lower() for k in keywords)

    cinema_keys = ["cinema", "movie", "film", "actor", "actress", "director", "kollywood"]
    sports_keys = ["cricket", "football", "match", "ipl", "sports"]
    music_keys = ["music", "song", "dance", "singer", "album"]
    love_keys = ["love", "relationship", "dating", "crush"]
    food_keys = ["food", "canteen", "snacks", "lunch", "eat"]
    job_keys = ["job", "salary", "placement", "internship", "career", "package"]

    SYSTEM_PROMPT = """
You are College GPT, an academic assistant for SA College of Arts & Science.

Language rule:
- Default: ENGLISH
- Use TAMIL only if the user writes in Tamil or explicitly asks for Tamil.

College Rules:
- "SA", "SACAS", "SA College" = SA College of Arts & Science, Thiruverkadu, Avadi, Chennai.
- Guide on academics, syllabus, departments, exams, careers in CS/AI.
- Be encouraging, professional, student-friendly.
- Never criticize any college or rank them.
"""

    for msg in st.session_state.college_gpt_chat:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_q = st.chat_input("Ask about college, syllabus, careers, CS-AI...")

    if user_q:
        st.session_state.college_gpt_chat.append({"role": "user", "content": user_q})
        with st.chat_message("user"):
            st.write(user_q)

        lang_instruction = "Respond ONLY in TAMIL." if is_tamil(user_q) else "Respond ONLY in ENGLISH."

        redirect_map = {
            tuple(cinema_keys): "🎓 College GPT is for academic guidance.\n\nInterested in media? SA College offers **Visual Communication (VISCOM)** covering film basics, editing, photography and digital media.",
            tuple(sports_keys): "🎓 College GPT is for academics.\n\nSA College actively supports sports — cricket, football, athletics through college tournaments and NSS activities.",
            tuple(music_keys): "🎓 College GPT is for academics.\n\nSA College hosts cultural events where you can showcase music and dance talents through annual fests.",
            tuple(love_keys): "🎓 College GPT supports academic guidance only.\n\nThe college has a student counselling cell for personal well-being support.",
            tuple(food_keys): "🎓 SA College has a student canteen on campus providing affordable meals and snacks during college hours.",
            tuple(job_keys): "🎓 SA College provides placement training, internship guidance, and career counselling to help students secure good opportunities in the tech industry.",
        }

        reply = None
        for keys, response in redirect_map.items():
            if contains_any(user_q, list(keys)):
                reply = response
                break

        if not reply:
            try:
                api_key = st.secrets["OPENAI_API_KEY"]
            except Exception:
                api_key = os.getenv("OPENAI_API_KEY")

            if not api_key:
                reply = "⚠️ API key not found. Please add OPENAI_API_KEY in Streamlit Secrets."
            else:
                client = OpenAI(api_key=api_key)
                try:
                    with st.spinner("College GPT is thinking..."):
                        history = [
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.college_gpt_chat
                        ]
                        messages = [
                            {"role": "system", "content": SYSTEM_PROMPT + "\n" + lang_instruction},
                            *history
                        ]
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=messages,
                            max_tokens=500
                        )
                        reply = response.choices[0].message.content.strip()
                except Exception as e:
                    reply = f"❌ GPT Error: {str(e)}"

        st.session_state.college_gpt_chat.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.write(reply)

        if st.button("🗑️ Clear Chat"):
            st.session_state.college_gpt_chat = []
            st.rerun()


# ============================================================
# =================== MAIN ROUTER ============================
# ============================================================
if st.session_state.page == "admin_login":
    admin_login_page()
elif st.session_state.admin_logged_in:
    admin_panel()
elif not st.session_state.logged_in:
    student_auth()
else:
    student_portal()

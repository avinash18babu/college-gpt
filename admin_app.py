# ============================================================
# SA COLLEGE OF ARTS & SCIENCE – COMPLETE STUDENT PORTAL
# ============================================================
# Author: Claude (Anthropic)
# Version: 2.0 (No External APIs)
# Features: 15+ including ChatGPT-like rule-based chatbot
# ============================================================

import streamlit as st
import sqlite3
import time
import pandas as pd
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from streamlit_cookies_manager import EncryptedCookieManager

# ============================================================
# ADMIN CREDENTIALS (SECRET)
# ============================================================
ADMIN_ACCESS_KEY = "SACAS_ADMIN_2026"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ============================================================
# PAGE CONFIGURATION (MUST BE FIRST)
# ============================================================
st.set_page_config(
    page_title="SA College of Arts & Science | Student Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS FOR MODERN UI
# ============================================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1e88e5;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .score-display {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #4caf50;
        margin: 20px 0;
    }
    .timer-box {
        background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# COOKIE MANAGER (REMEMBER ME FEATURE)
# ============================================================
cookies = EncryptedCookieManager(
    prefix="sacas_portal_",
    password="secure_cookie_key_2026"
)

if not cookies.ready():
    st.stop()

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        "logged_in": False,
        "is_admin": False,
        "current_user": {},
        "auth_page": "login",
        "exam_step": 0,
        "exam_started": False,
        "exam_finished": False,
        "score": 0,
        "start_time": None,
        "chat_history": [],
        "admin_verified": False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ============================================================
# DATABASE SETUP
# ============================================================
def init_database():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect("college_portal.db", check_same_thread=False)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            school TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Exam attempts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attempts (
            username TEXT PRIMARY KEY,
            score INTEGER,
            completed INTEGER DEFAULT 1,
            attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    return conn

conn = init_database()

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def safe_image(path, **kwargs):
    """Display image if exists, otherwise show placeholder"""
    if Path(path).exists():
        st.image(path, **kwargs)
    else:
        st.info(f"📷 Image placeholder: {path}")

def check_attempt(username):
    """Check if user has already attempted the exam"""
    cursor = conn.cursor()
    cursor.execute("SELECT completed FROM attempts WHERE username=?", (username,))
    result = cursor.fetchone()
    return result is not None

def save_attempt(username, score):
    """Save exam attempt to database"""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO attempts (username, score) VALUES (?, ?)",
        (username, score)
    )
    conn.commit()

def generate_pdf(username, student_name, score, department):
    """Generate PDF certificate for exam result"""
    pdf_name = f"Result_{username}.pdf"
    c = canvas.Canvas(pdf_name, pagesize=A4)
    
    # Header
    c.setFont("Helvetica-Bold", 20)
    c.drawString(150, 800, "SA College of Arts & Science")
    
    c.setFont("Helvetica", 14)
    c.drawString(180, 770, "Online Degree Entrance Test")
    c.drawString(220, 750, "Result Certificate")
    
    # Divider
    c.line(50, 730, 550, 730)
    
    # Student details
    c.setFont("Helvetica", 12)
    c.drawString(100, 690, f"Student Name: {student_name}")
    c.drawString(100, 660, f"Register Number: {username}")
    c.drawString(100, 630, f"Total Score: {score} / 120")
    c.drawString(100, 600, f"Percentage: {(score/120)*100:.2f}%")
    c.drawString(100, 570, f"Suggested Department: {department}")
    
    # Footer
    c.line(50, 550, 550, 550)
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(150, 520, "This is a computer-generated certificate")
    c.drawString(180, 500, "SA College Admission System")
    
    c.showPage()
    c.save()
    
    return pdf_name

# ============================================================
# ADMIN LOGIN (HIDDEN ACCESS)
# ============================================================
def admin_login_page():
    """Hidden admin access page"""
    st.markdown('<p class="main-header">🔐 Admin Access</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        access_key = st.text_input("Access Key", type="password", key="admin_key")
        username = st.text_input("Admin Username", key="admin_user")
        password = st.text_input("Admin Password", type="password", key="admin_pass")
        
        if st.button("🔓 Access Admin Panel", use_container_width=True):
            if (access_key == ADMIN_ACCESS_KEY and 
                username == ADMIN_USERNAME and 
                password == ADMIN_PASSWORD):
                st.session_state.logged_in = True
                st.session_state.is_admin = True
                st.session_state.admin_verified = True
                st.rerun()
            else:
                st.error("❌ Invalid credentials")
        
        if st.button("← Back to Student Login", use_container_width=True):
            st.session_state.admin_verified = False
            st.rerun()

# ============================================================
# ADMIN PANEL
# ============================================================
def admin_panel():
    """Admin dashboard with student and attempt data"""
    st.markdown('<p class="main-header">👨‍💼 Admin Dashboard</p>', unsafe_allow_html=True)
    
    # Logout button
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.is_admin = False
        st.session_state.admin_verified = False
        st.rerun()
    
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "👥 Students", "📝 Exam Attempts"])
    
    with tab1:
        cursor = conn.cursor()
        
        # Statistics
        cursor.execute("SELECT COUNT(*) FROM users")
        total_students = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM attempts")
        total_attempts = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(score) FROM attempts")
        avg_score = cursor.fetchone()[0] or 0
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Students", total_students, "Registered")
        with col2:
            st.metric("Exam Attempts", total_attempts, "Completed")
        with col3:
            st.metric("Average Score", f"{avg_score:.1f}", "Out of 120")
    
    with tab2:
        cursor.execute("SELECT id, student_name, username, school, created_at FROM users")
        students = cursor.fetchall()
        
        if students:
            df = pd.DataFrame(students, columns=["ID", "Name", "Username", "School", "Registered"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No students registered yet")
    
    with tab3:
        cursor.execute("""
            SELECT a.username, u.student_name, a.score, a.attempted_at 
            FROM attempts a
            JOIN users u ON a.username = u.username
            ORDER BY a.score DESC
        """)
        attempts = cursor.fetchall()
        
        if attempts:
            df = pd.DataFrame(attempts, columns=["Username", "Name", "Score", "Date"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No exam attempts yet")

# ============================================================
# STUDENT AUTHENTICATION
# ============================================================
def student_auth():
    """Student login and registration page"""
    st.markdown('<p class="main-header">🎓 SA College Student Portal</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Welcome to the Digital Campus</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.session_state.auth_page == "login":
            st.subheader("🔑 Student Login")
            
            username = st.text_input("Register Number / Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            remember_me = st.checkbox("Remember me on this device")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("🚀 Login", use_container_width=True):
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT student_name, username, school FROM users WHERE username=? AND password=?",
                        (username, password)
                    )
                    result = cursor.fetchone()
                    
                    if result:
                        st.session_state.logged_in = True
                        st.session_state.current_user = {
                            "student_name": result[0],
                            "username": result[1],
                            "school": result[2]
                        }
                        
                        if remember_me:
                            cookies["username"] = username
                            cookies.save()
                        
                        st.success("✅ Login successful!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")
            
            with col_b:
                if st.button("📝 New Student?", use_container_width=True):
                    st.session_state.auth_page = "register"
                    st.rerun()
            
            st.divider()
            if st.button("🔐 Admin Access", use_container_width=True):
                st.session_state.admin_verified = True
                st.rerun()
        
        else:  # Registration page
            st.subheader("📝 Student Registration")
            
            student_name = st.text_input("Full Name", key="reg_name")
            username = st.text_input("Register Number / Username", key="reg_user")
            password = st.text_input("Create Password", type="password", key="reg_pass")
            confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
            school = st.text_input("School Name", key="reg_school")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("✅ Register", use_container_width=True):
                    if not all([student_name, username, password, school]):
                        st.error("All fields are required")
                    elif password != confirm_password:
                        st.error("Passwords don't match")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters")
                    else:
                        try:
                            cursor = conn.cursor()
                            cursor.execute(
                                "INSERT INTO users (student_name, username, password, school) VALUES (?, ?, ?, ?)",
                                (student_name, username, password, school)
                            )
                            conn.commit()
                            st.success("✅ Registration successful! Please login.")
                            time.sleep(2)
                            st.session_state.auth_page = "login"
                            st.rerun()
                        except sqlite3.IntegrityError:
                            st.error("❌ Username already exists")
            
            with col_b:
                if st.button("← Back to Login", use_container_width=True):
                    st.session_state.auth_page = "login"
                    st.rerun()

# ============================================================
# AUTO-LOGIN (REMEMBER ME)
# ============================================================
def auto_login():
    """Check for remembered user and auto-login"""
    if not st.session_state.logged_in and not st.session_state.admin_verified:
        remembered_user = cookies.get("username")
        if remembered_user:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT student_name, username, school FROM users WHERE username=?",
                (remembered_user,)
            )
            result = cursor.fetchone()
            if result:
                st.session_state.logged_in = True
                st.session_state.current_user = {
                    "student_name": result[0],
                    "username": result[1],
                    "school": result[2]
                }

auto_login()

# ============================================================
# RULE-BASED CHATBOT ENGINE
# ============================================================
class CollegeGPT:
    """Intelligent rule-based chatbot for college queries"""
    
    def __init__(self):
        self.knowledge_base = {
            # Greetings
            "greetings": {
                "keywords": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "vanakkam", "வணக்கம்"],
                "response": "Hello! 👋 Welcome to SA College GPT. I'm here to help you with:\n\n• Course information\n• Admission process\n• AI programs\n• Placements & careers\n• Fees & facilities\n• Campus location\n\nWhat would you like to know?"
            },
            
            # Courses
            "courses": {
                "keywords": ["course", "degree", "program", "study", "bsc", "bcom", "bba", "படிப்பு"],
                "response": "📚 **Courses at SA College:**\n\n**Science Stream:**\n• B.Sc Computer Science\n• B.Sc Computer Science with AI\n• B.Sc Mathematics\n• B.Sc Physics\n\n**Commerce & Management:**\n• B.Com (Commerce)\n• BBA (Business Administration)\n\n**Arts:**\n• B.A English\n• B.A Tamil\n• Visual Communication (VISCOM)\n\nWhich stream interests you?"
            },
            
            # AI Program
            "ai_program": {
                "keywords": ["ai", "artificial intelligence", "machine learning", "ml", "deep learning", "nlp", "computer vision"],
                "response": "🤖 **B.Sc Computer Science with AI:**\n\n**Core AI Subjects:**\n• Machine Learning Fundamentals\n• Deep Learning & Neural Networks\n• Natural Language Processing\n• Computer Vision\n• AI Ethics & Applications\n\n**Programming Skills:**\n• Python (NumPy, Pandas, TensorFlow)\n• Data Structures & Algorithms\n• Database Management\n\n**Career Prospects:**\n• AI/ML Engineer\n• Data Scientist\n• Research Associate\n• AI Product Developer\n\n**Duration:** 3 Years\n**Eligibility:** 12th with Maths/Computer Science"
            },
            
            # Admission
            "admission": {
                "keywords": ["admission", "apply", "application", "join", "enroll", "சேர", "விண்ணப்பம்"],
                "response": "📝 **Admission Process:**\n\n**Step 1:** Online Registration\n• Fill basic details\n• Create login credentials\n\n**Step 2:** Entrance Test\n• 12 questions (4 sections)\n• 5-minute duration\n• Online mode\n\n**Step 3:** Document Submission\n• 10th & 12th Marksheets\n• Transfer Certificate\n• Community Certificate (if applicable)\n\n**Step 4:** Fee Payment & Confirmation\n\n**Important:** Each student can attempt the entrance test only once.\n\n**Contact:** Visit college office for direct admission guidance."
            },
            
            # Placement
            "placement": {
                "keywords": ["placement", "job", "career", "interview", "company", "salary", "வேலை", "தொழில்"],
                "response": "💼 **Placement & Career Support:**\n\n**Training Programs:**\n• Resume building workshops\n• Mock interviews\n• Aptitude training\n• Soft skills development\n• Group discussions\n\n**Placement Partners:**\n• IT companies\n• Start-ups\n• MNCs\n• Government sectors\n\n**Career Paths (CS/AI):**\n• Software Developer\n• Data Analyst\n• AI/ML Engineer\n• Web Developer\n• System Administrator\n\n**Internship Opportunities:** Available during final year\n\n**Average Package:** Varies by skill and company"
            },
            
            # Syllabus
            "syllabus": {
                "keywords": ["syllabus", "subjects", "curriculum", "topics", "பாடத்திட்டம்"],
                "response": "📖 **B.Sc Computer Science Syllabus:**\n\n**Year 1:**\n• Programming in C\n• Digital Principles\n• Mathematics for CS\n• Office Automation\n\n**Year 2:**\n• Data Structures\n• Python Programming\n• Database Management (SQL)\n• Web Technologies\n\n**Year 3:**\n• Artificial Intelligence\n• Machine Learning\n• Software Engineering\n• Project Work\n\n**Additional (AI Specialization):**\n• Deep Learning\n• NLP & Computer Vision\n• AI Ethics\n\nWant details on a specific year?"
            },
            
            # Fees
            "fees": {
                "keywords": ["fees", "cost", "price", "payment", "scholarship", "கட்டணம்"],
                "response": "💰 **Fee Structure:**\n\nFees vary by course and category:\n\n• **B.Sc Computer Science:** Contact office\n• **B.Com / BBA:** Contact office\n• **Other programs:** Contact office\n\n**Payment Options:**\n• Semester-wise\n• Annual\n\n**Scholarships Available:**\n• Government scholarships\n• Merit-based scholarships\n• Financial aid for eligible students\n\n**Note:** For exact fee details, please contact:\n📞 College Office\n📧 admission@sacollege.edu (example)\n\nFees are subject to change as per university norms."
            },
            
            # Location
            "location": {
                "keywords": ["location", "address", "where", "map", "reach", "எங்கே", "இடம்"],
                "response": "📍 **SA College Location:**\n\n**Address:**\nSA College of Arts & Science\nThiruverkadu, Avadi\nChennai - 600077\nTamil Nadu, India\n\n**Nearby Landmarks:**\n• Close to Avadi Railway Station\n• Well connected by bus routes\n\n**How to Reach:**\n• **By Bus:** Multiple routes available\n• **By Train:** Avadi Station (nearest)\n• **By Car:** Accessible via Poonamallee High Road\n\nYou can view the exact location on the 'Location' page in the portal!"
            },
            
            # Faculty / HOD
            "faculty": {
                "keywords": ["hod", "faculty", "staff", "teacher", "professor", "head"],
                "response": "👨‍🏫 **Department Faculty:**\n\n**Head of CS with AI:**\nMr. Krishnan R\n• Qualification: M.Sc, M.Phil, NET, SET\n• UG Experience: 30+ years\n• PG Experience: 23+ years\n\n**Focus Areas:**\n• Industry-ready curriculum\n• Practical learning approach\n• Ethical AI education\n• Research & innovation\n\n**Department Strengths:**\n• Experienced faculty team\n• Modern lab facilities\n• Student-centric teaching\n• Industry collaborations\n\nVisit the 'HOD Section' page for more details!"
            },
            
            # Facilities
            "facilities": {
                "keywords": ["facility", "lab", "library", "hostel", "canteen", "sports", "wifi"],
                "response": "🏫 **Campus Facilities:**\n\n**Academic:**\n• Computer Labs with latest systems\n• Library with digital resources\n• Smart classrooms\n• Wi-Fi enabled campus\n\n**Student Amenities:**\n• Canteen\n• Sports ground\n• Indoor games\n• Counseling services\n\n**Co-curricular:**\n• NSS activities\n• Cultural events\n• Technical workshops\n• Seminars & conferences\n\n**Safety:**\n• CCTV surveillance\n• Security personnel\n• First aid facility"
            },
            
            # Exam / Test
            "exam": {
                "keywords": ["exam", "test", "entrance", "question", "result", "தேர்வு"],
                "response": "📝 **Entrance Test Information:**\n\n**Format:**\n• Total Questions: 12\n• Sections: 4 (Quantitative, Logical, Computer, GK)\n• Duration: 5 minutes\n• Type: Multiple Choice\n\n**Important Rules:**\n• ⚠️ One attempt only per student\n• Timer-based (auto-submit)\n• No negative marking\n\n**After Exam:**\n• Instant result display\n• Department suggestion based on score\n• Downloadable PDF certificate\n\n**Scoring:**\n• 90+ marks → CS / CS-AI recommended\n• 70-89 marks → B.Com / BBA\n• 50-69 marks → Science programs\n• Below 50 → Arts programs\n\nReady to take the test? Go to 'Online Entrance Test' page!"
            },
            
            # Thank you
            "thanks": {
                "keywords": ["thank", "thanks", "நன்றி"],
                "response": "You're welcome! 😊 Happy to help you explore SA College.\n\nIf you have more questions, feel free to ask anytime!\n\n**Quick Links:**\n• About College\n• Course Details\n• Admission Process\n• Take Entrance Test\n\nGood luck with your education journey! 🎓"
            }
        }
    
    def get_response(self, user_input):
        """Generate intelligent response based on keywords"""
        user_input_lower = user_input.lower()
        
        # Check each category
        for category, data in self.knowledge_base.items():
            for keyword in data["keywords"]:
                if keyword in user_input_lower:
                    return data["response"]
        
        # Fallback response with suggestions
        return ("🤔 I didn't quite understand that.\n\n"
                "**I can help you with:**\n"
                "• 📚 Course information\n"
                "• 🤖 AI program details\n"
                "• 📝 Admission process\n"
                "• 💼 Placement & careers\n"
                "• 💰 Fees structure\n"
                "• 📍 College location\n"
                "• 👨‍🏫 Faculty information\n"
                "• 🏫 Campus facilities\n"
                "• 📝 Entrance test details\n\n"
                "Try asking something like:\n"
                "• 'Tell me about AI course'\n"
                "• 'What is the admission process?'\n"
                "• 'Where is the college located?'")

# Initialize chatbot
chatbot = CollegeGPT()

# ============================================================
# MAIN APPLICATION LOGIC
# ============================================================

# Check authentication
if not st.session_state.logged_in:
    if st.session_state.admin_verified:
        admin_login_page()
    else:
        student_auth()
    st.stop()

# Admin Panel
if st.session_state.is_admin:
    admin_panel()
    st.stop()

# ============================================================
# STUDENT PORTAL (AFTER LOGIN)
# ============================================================

# Sidebar
st.sidebar.success(f"👤 {st.session_state.current_user['student_name']}")
st.sidebar.caption(f"🆔 {st.session_state.current_user['username']}")
st.sidebar.caption(f"🏫 {st.session_state.current_user['school']}")

st.sidebar.divider()

menu = st.sidebar.radio(
    "📚 Navigation Menu",
    [
        "🏫 About College",
        "📍 Location",
        "📚 Syllabus (CS & AI)",
        "👨‍🏫 HOD Section",
        "📝 Entrance Test",
        "🤖 College GPT"
    ]
)

if st.sidebar.button("🚪 Logout", use_container_width=True):
    # Clear cookies
    if "username" in cookies:
        del cookies["username"]
        cookies.save()
    
    # Reset session
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    st.rerun()

# ============================================================
# PAGE 1: ABOUT COLLEGE
# ============================================================
if menu == "🏫 About College":
    st.markdown('<p class="main-header">🏫 About SA College of Arts & Science</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Welcome to SA College of Arts & Science
        
        Located in **Thiruverkadu, Avadi, Chennai**, SA College of Arts & Science (SACAS) 
        is committed to providing quality education that combines academic excellence with 
        ethical values and practical skills.
        
        ### 🎯 Our Vision
        To be a center of excellence in higher education, fostering innovation, research, 
        and holistic development of students.
        
        ### 🌟 Our Mission
        - Deliver industry-relevant education
        - Promote research and innovation
        - Build ethical and responsible citizens
        - Create opportunities for all-round development
        
        ### 🏆 Key Highlights
        - **Experienced Faculty** with 20+ years expertise
        - **Modern Infrastructure** and smart classrooms
        - **Industry Partnerships** for placements
        - **Student-Centric Approach** to learning
        - **Affordable Education** with scholarship support
        
        ### 📜 Accreditations
        - Affiliated to University of Madras
        - Recognized by UGC
        - ISO Certified Institution
        """)
    
    with col2:
        safe_image("assets/ai_students.png", width=300)
        st.info("**Campus Atmosphere**\nModern facilities meet traditional values")

# ============================================================
# PAGE 2: LOCATION
# ============================================================
elif menu == "📍 Location":
    st.markdown('<p class="main-header">📍 College Location</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Map display
        map_data = pd.DataFrame({
            "lat": [13.0475],
            "lon": [80.1012]
        })
        st.map(map_data, zoom=13)
    
    with col2:
        st.markdown("""
        ### 📫 Address
        **SA College of Arts & Science**  
        Thiruverkadu, Avadi  
        Chennai - 600077  
        Tamil Nadu, India
        
        ### 🚌 How to Reach
        
        **By Bus:**
        - Multiple routes available
        - Stop: Thiruverkadu
        
        **By Train:**
        - Nearest: Avadi Station
        - Distance: ~3 km
        
        **By Car:**
        - Via Poonamallee High Road
        - Ample parking available
        
        ### 📞 Contact
        **Phone:** +91-XXXXXXXXXX  
        **Email:** info@sacollege.edu  
        **Website:** www.sacollege.edu
        """)

# ============================================================
# PAGE 3: SYLLABUS
# ============================================================
elif menu == "📚 Syllabus (CS & AI)":
    st.markdown('<p class="main-header">📚 B.Sc Computer Science & CS with AI</p>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📘 Year 1", "📗 Year 2", "📙 Year 3"])
    
    with tab1:
        st.subheader("First Year - Foundation")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Semester 1**
            - Programming in C
            - Digital Principles & System Design
            - Discrete Mathematics
            - English Communication
            - Tamil / Hindi
            """)
        
        with col2:
            st.markdown("""
            **Semester 2**
            - Data Structures using C
            - Computer Organization
            - Statistical Methods
            - Environmental Science
            - Office Automation Tools
            """)
    
    with tab2:
        st.subheader("Second Year - Core Development")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Semester 3**
            - Object-Oriented Programming (Java)
            - Database Management Systems
            - Python Programming
            - Operating Systems
            - Web Technologies (HTML, CSS, JS)
            """)
        
        with col2:
            st.markdown("""
            **Semester 4**
            - Advanced Java Programming
            - Software Engineering
            - Computer Networks
            - PHP & MySQL
            - Mobile Application Development
            """)
    
    with tab3:
        st.subheader("Third Year - Specialization (AI Focus)")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Semester 5**
            - Artificial Intelligence
            - Machine Learning Fundamentals
            - Data Analytics using Python
            - Cloud Computing
            - Compiler Design
            """)
        
        with col2:
            st.markdown("""
            **Semester 6**
            - Deep Learning & Neural Networks
            - Natural Language Processing
            - Computer Vision
            - AI Ethics & Applications
            - Major Project Work
            """)
    
    st.divider()
    st.info("💡 **Note:** AI specialization subjects are exclusive to B.Sc CS with AI program")

# ============================================================
# PAGE 4: HOD SECTION
# ============================================================
elif menu == "👨‍🏫 HOD Section":
    st.markdown('<p class="main-header">👨‍🏫 Head of Department - CS with AI</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        safe_image("assets/hod.png", width=300)
        st.markdown("""
        <div class="info-box">
        <h3 style="color: white; margin: 0;">Mr. Krishnan R</h3>
        <p style="margin: 5px 0;">M.Sc, M.Phil, NET, SET</p>
        <p style="margin: 0;">Head of Department</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        ### Professional Profile
        
        **Qualifications:**
        - M.Sc in Computer Science
        - M.Phil in Computer Science
        - NET (National Eligibility Test) Qualified
        - SET (State Eligibility Test) Qualified
        
        ### Experience
        - **UG Teaching:** 30+ Years
        - **PG Teaching:** 23+ Years
        - **Research Guidance:** Multiple M.Phil scholars
        
        ### Areas of Expertise
        - Artificial Intelligence & Machine Learning
        - Data Science & Analytics
        - Algorithm Design & Analysis
        - Database Systems
        - Software Engineering
        
        ### Vision for the Department
        > "Our goal is to create AI professionals who are not just technically 
        > competent but also ethically grounded. We focus on practical learning, 
        > industry collaboration, and research-driven education."
        
        ### Key Initiatives
        - Industry-Academia partnerships
        - Student project mentorship
        - Workshop and seminar organization
        - Placement training programs
        - Research paper publications
        
        ### Awards & Recognition
        - Best Teacher Award (2020)
        - Excellence in Research (2018)
        - 25+ years service award
        """)
    
    st.divider()
    
    st.subheader("📢 Message to Students")
    st.info("""
    **"Dear Students,"**
    
    The field of Computer Science and Artificial Intelligence is rapidly evolving. 
    To succeed, you need continuous learning, practical skills, and ethical awareness.
    
    Our department is committed to providing you with:
    - Strong foundational knowledge
    - Hands-on project experience  
    - Industry exposure
    - Research opportunities
    - Career guidance
    
    Remember: Technology is a tool for positive change. Use your skills to solve 
    real-world problems and make a meaningful impact on society.
    
    Wishing you all the best in your academic journey!
    
    **Mr. Krishnan R**  
    *Head of Department, CS with AI*
    """)

# ============================================================
# PAGE 5: ENTRANCE TEST
# ============================================================
elif menu == "📝 Entrance Test":
    
    # Check if already attempted
    if check_attempt(st.session_state.current_user["username"]) and not st.session_state.exam_finished:
        st.error("🚫 You have already completed this entrance test.")
        st.info("Each student is allowed only ONE attempt.")
        st.stop()
    
    # ===== START PAGE =====
    if st.session_state.exam_step == 0:
        st.markdown('<p class="main-header">📝 Online Degree Entrance Test</p>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div class="info-box">
            <h2 style="color: white; text-align: center;">Test Information</h2>
            <ul style="font-size: 1.1rem;">
                <li>⏱ <b>Duration:</b> 5 Minutes</li>
                <li>📝 <b>Questions:</b> 12 (4 sections)</li>
                <li>🎯 <b>Max Score:</b> 120 points</li>
                <li>⚠️ <b>Attempts:</b> One attempt only</li>
                <li>📊 <b>Format:</b> Multiple Choice</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            
            st.markdown("""
            ### 📋 Test Structure
            
            **Section A - Quantitative Ability** (3 questions)
            - Basic mathematics and calculations
            
            **Section B - Logical Reasoning** (3 questions)
            - Pattern recognition and logic
            
            **Section C - Computer Awareness** (3 questions)
            - Basic computer concepts
            
            **Section D - General Knowledge** (3 questions)
            - Current affairs and general awareness
            """)
            
            st.warning("⚠️ **Important:** The test will auto-submit after 5 minutes!")
            
            if st.button("▶️ Start Test Now", use_container_width=True, type="primary"):
                st.session_state.exam_step = 1
                st.session_state.exam_started = True
                st.session_state.start_time = time.time()
                st.session_state.score = 0
                st.rerun()
    
    # ===== TIMER (Display during exam) =====
    if st.session_state.exam_started and not st.session_state.exam_finished:
        TOTAL_TIME = 5 * 60  # 5 minutes
        elapsed = int(time.time() - st.session_state.start_time)
        remaining = max(0, TOTAL_TIME - elapsed)
        
        mins, secs = divmod(remaining, 60)
        
        # Progress bar
        progress = remaining / TOTAL_TIME
        st.progress(progress)
        
        # Timer display
        st.markdown(
            f'<div class="timer-box">⏱ Time Remaining: {mins:02d}:{secs:02d}</div>',
            unsafe_allow_html=True
        )
        
        # Auto-submit when time's up
        if remaining == 0:
            st.session_state.exam_step = 5
            st.session_state.exam_finished = True
            save_attempt(st.session_state.current_user["username"], st.session_state.score)
            st.rerun()
        
        st.divider()
    
    # ===== SECTION A =====
    if st.session_state.exam_step == 1:
        st.subheader("📘 Section A - Quantitative Ability")
        st.caption("Questions 1-3 | 10 points each")
        
        q1 = st.radio(
            "**1. What is 25% of 200?**",
            ["25", "50", "75", "100"],
            index=None,
            key="q1"
        )
        
        q2 = st.radio(
            "**2. Find the average of 10, 20, and 30:**",
            ["15", "20", "25", "30"],
            index=None,
            key="q2"
        )
        
        q3 = st.radio(
            "**3. Calculate: 12 × 8 =**",
            ["72", "84", "88", "96"],
            index=None,
            key="q3"
        )
        
        st.divider()
        
        if st.button("Next Section ➡️", use_container_width=True, type="primary"):
            if None in (q1, q2, q3):
                st.error("⚠️ Please answer all questions before proceeding")
                st.stop()
            
            # Calculate score
            if q1 == "50": st.session_state.score += 10
            if q2 == "20": st.session_state.score += 10
            if q3 == "96": st.session_state.score += 10
            
            st.session_state.exam_step = 2
            st.rerun()
    
    # ===== SECTION B =====
    elif st.session_state.exam_step == 2:
        st.subheader("📗 Section B - Logical Reasoning")
        st.caption("Questions 4-6 | 10 points each")
        
        q4 = st.radio(
            "**4. Which one is the odd one out?**",
            ["Apple", "Banana", "Car", "Mango"],
            index=None,
            key="q4"
        )
        
        q5 = st.radio(
            "**5. Complete the series: 2, 4, 8, 16, __**",
            ["20", "24", "28", "32"],
            index=None,
            key="q5"
        )
        
        q6 = st.radio(
            "**6. If A > B and B > C, then:**",
            ["A > C", "C > A", "A = C", "Cannot determine"],
            index=None,
            key="q6"
        )
        
        st.divider()
        
        if st.button("Next Section ➡️", use_container_width=True, type="primary"):
            if None in (q4, q5, q6):
                st.error("⚠️ Please answer all questions before proceeding")
                st.stop()
            
            if q4 == "Car": st.session_state.score += 10
            if q5 == "32": st.session_state.score += 10
            if q6 == "A > C": st.session_state.score += 10
            
            st.session_state.exam_step = 3
            st.rerun()
    
    # ===== SECTION C =====
    elif st.session_state.exam_step == 3:
        st.subheader("📙 Section C - Computer Awareness")
        st.caption("Questions 7-9 | 10 points each")
        
        q7 = st.radio(
            "**7. CPU stands for:**",
            ["Central Processing Unit", "Central Program Unit", "Computer Personal Unit", "Central Peripheral Unit"],
            index=None,
            key="q7"
        )
        
        q8 = st.radio(
            "**8. Binary number system uses:**",
            ["0 and 1", "1 and 2", "0 and 2", "1 and 3"],
            index=None,
            key="q8"
        )
        
        q9 = st.radio(
            "**9. Python is a:**",
            ["High-level language", "Low-level language", "Machine language", "Assembly language"],
            index=None,
            key="q9"
        )
        
        st.divider()
        
        if st.button("Next Section ➡️", use_container_width=True, type="primary"):
            if None in (q7, q8, q9):
                st.error("⚠️ Please answer all questions before proceeding")
                st.stop()
            
            if q7 == "Central Processing Unit": st.session_state.score += 10
            if q8 == "0 and 1": st.session_state.score += 10
            if q9 == "High-level language": st.session_state.score += 10
            
            st.session_state.exam_step = 4
            st.rerun()
    
    # ===== SECTION D =====
    elif st.session_state.exam_step == 4:
        st.subheader("📕 Section D - General Knowledge")
        st.caption("Questions 10-12 | 10 points each")
        
        q10 = st.radio(
            "**10. Capital of Tamil Nadu:**",
            ["Chennai", "Madurai", "Coimbatore", "Salem"],
            index=None,
            key="q10"
        )
        
        q11 = st.radio(
            "**11. Father of Computer Science:**",
            ["Charles Babbage", "Isaac Newton", "Albert Einstein", "Thomas Edison"],
            index=None,
            key="q11"
        )
        
        q12 = st.radio(
            "**12. National Animal of India:**",
            ["Lion", "Tiger", "Elephant", "Peacock"],
            index=None,
            key="q12"
        )
        
        st.divider()
        
        if st.button("✅ Submit Exam", use_container_width=True, type="primary"):
            if None in (q10, q11, q12):
                st.error("⚠️ Please answer all questions before submitting")
                st.stop()
            
            if q10 == "Chennai": st.session_state.score += 10
            if q11 == "Charles Babbage": st.session_state.score += 10
            if q12 == "Tiger": st.session_state.score += 10
            
            # Save attempt
            save_attempt(st.session_state.current_user["username"], st.session_state.score)
            
            st.session_state.exam_finished = True
            st.session_state.exam_step = 5
            st.rerun()
    
    # ===== RESULT PAGE =====
    elif st.session_state.exam_step == 5:
        st.markdown('<p class="main-header">🎉 Examination Result</p>', unsafe_allow_html=True)
        
        # Display score
        st.markdown(
            f'<div class="score-display">{st.session_state.score} / 120</div>',
            unsafe_allow_html=True
        )
        
        # Calculate percentage
        percentage = (st.session_state.score / 120) * 100
        
        # Department suggestion
        if st.session_state.score >= 90:
            dept = "B.Sc Computer Science / CS with AI"
            icon = "🤖"
            color = "#4caf50"
        elif st.session_state.score >= 70:
            dept = "B.Com / BBA"
            icon = "💼"
            color = "#2196f3"
        elif st.session_state.score >= 50:
            dept = "B.Sc Mathematics / Physics / Chemistry"
            icon = "🔬"
            color = "#ff9800"
        else:
            dept = "B.A English / Tamil / General Arts"
            icon = "📚"
            color = "#9c27b0"
        
        st.markdown(f"""
        <div class="info-box" style="background: {color};">
            <h2 style="color: white; margin: 0;">{icon} Suggested Department</h2>
            <h3 style="color: white; margin: 10px 0;">{dept}</h3>
            <p style="color: white; margin: 0;">Based on your performance of {percentage:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Performance analysis
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Score", st.session_state.score, "Out of 120")
        with col2:
            st.metric("Percentage", f"{percentage:.1f}%", "")
        with col3:
            grade = "A+" if percentage >= 90 else "A" if percentage >= 70 else "B" if percentage >= 50 else "C"
            st.metric("Grade", grade, "")
        
        st.divider()
        
        # Generate PDF
        pdf_file = generate_pdf(
            st.session_state.current_user["username"],
            st.session_state.current_user["student_name"],
            st.session_state.score,
            dept
        )
        
        # Download button
        with open(pdf_file, "rb") as f:
            st.download_button(
                label="📄 Download Result Certificate",
                data=f,
                file_name=f"SA_College_Result_{st.session_state.current_user['username']}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )
        
        st.success("✅ Your result has been saved successfully!")
        
        # Next steps
        st.info("""
        ### 📝 Next Steps:
        
        1. **Download** your result certificate
        2. **Visit** college office for document verification
        3. **Submit** required documents:
           - 10th & 12th Marksheets
           - Transfer Certificate
           - Community Certificate (if applicable)
           - Passport size photos
        4. **Complete** admission formalities
        
        For any queries, contact: **admission@sacollege.edu**
        """)

# ============================================================
# PAGE 6: COLLEGE GPT (CHATGPT-LIKE INTERFACE)
# ============================================================
elif menu == "🤖 College GPT":
    st.markdown('<p class="main-header">🤖 College GPT Assistant</p>', unsafe_allow_html=True)
    st.caption("Your AI-powered college information assistant | Powered by intelligent rules")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    user_input = st.chat_input("Ask me anything about SA College...")
    
    if user_input:
        # Add user message
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Generate response
        with st.chat_message("assistant"):
            # Typing animation
            message_placeholder = st.empty()
            
            # Get bot response
            bot_response = chatbot.get_response(user_input)
            
            # Simulate typing
            displayed_text = ""
            for char in bot_response:
                displayed_text += char
                message_placeholder.markdown(displayed_text + "▌")
                time.sleep(0.01)
            
            # Final message without cursor
            message_placeholder.markdown(bot_response)
        
        # Save assistant response
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": bot_response
        })
    
    # Clear chat button in sidebar
    st.sidebar.divider()
    if st.sidebar.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()
    
    # Usage tips
    with st.sidebar.expander("💡 Tips for Better Responses"):
        st.markdown("""
        **Ask about:**
        - Course details and syllabus
        - Admission process
        - AI program specifics
        - Placement information
        - Fees structure
        - Campus location
        - Faculty details
        - Facilities available
        - Entrance test info
        
        **Example queries:**
        - "Tell me about the AI program"
        - "What is the admission process?"
        - "Where is the college located?"
        - "What are the placement opportunities?"
        """)

# ============================================================
# FOOTER
# ============================================================
st.sidebar.divider()
st.sidebar.caption("© 2026 SA College of Arts & Science")
st.sidebar.caption("Thiruverkadu, Avadi, Chennai")
st.sidebar.caption("Version 2.0 | Powered by Streamlit")

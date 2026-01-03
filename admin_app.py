# ============================================================
# SA COLLEGE OF ARTS & SCIENCE – ADMIN PANEL
# Purpose:
# - Admin-only login
# - View registered students
# - View exam attempts
# - View results
# ============================================================

import streamlit as st
import pandas as pd
import os

# ============================================================
# ADMIN CREDENTIALS (CHANGE IF YOU WANT)
# ============================================================

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ============================================================
# DATA FILES (SHARED WITH STUDENT APP)
# ============================================================

USERS_FILE = "users.csv"
ATTEMPTS_FILE = "attempts.csv"
RESULTS_FILE = "results.csv"

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Admin Panel | SA College",
    page_icon="🔐",
    layout="wide"
)

# ============================================================
# SESSION STATE
# ============================================================

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# ============================================================
# ADMIN LOGIN
# ============================================================

if not st.session_state.admin_logged_in:
    st.title("🔐 Admin Login")

    username = st.text_input("Admin Username")
    password = st.text_input("Admin Password", type="password")

    if st.button("Login"):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.admin_logged_in = True
            st.success("Admin login successful")
            st.rerun()
        else:
            st.error("Invalid admin credentials")

    st.stop()

# ============================================================
# ADMIN DASHBOARD
# ============================================================

st.sidebar.success("Logged in as Admin")

if st.sidebar.button("Logout"):
    st.session_state.admin_logged_in = False
    st.rerun()

menu = st.sidebar.radio(
    "Admin Menu",
    [
        "👨‍🎓 Registered Students",
        "📝 Exam Attempts",
        "📊 Results"
    ]
)

# ============================================================
# REGISTERED STUDENTS
# ============================================================

if menu == "👨‍🎓 Registered Students":
    st.header("👨‍🎓 Registered Students")

    if os.path.exists(USERS_FILE):
        users = pd.read_csv(USERS_FILE)

        if users.empty:
            st.info("No students registered yet.")
        else:
            st.dataframe(users, use_container_width=True)
    else:
        st.warning("users.csv file not found")

# ============================================================
# EXAM ATTEMPTS
# ============================================================

elif menu == "📝 Exam Attempts":
    st.header("📝 Exam Attempts")

    if os.path.exists(ATTEMPTS_FILE):
        attempts = pd.read_csv(ATTEMPTS_FILE)

        if attempts.empty:
            st.info("No exam attempts found.")
        else:
            st.dataframe(attempts, use_container_width=True)
    else:
        st.warning("attempts.csv file not found")

# ============================================================
# RESULTS
# ============================================================

elif menu == "📊 Results":
    st.header("📊 Student Results")

    if os.path.exists(RESULTS_FILE):
        results = pd.read_csv(RESULTS_FILE)

        if results.empty:
            st.info("No results available yet.")
        else:
            st.dataframe(results, use_container_width=True)
    else:
        st.warning("results.csv file not found")

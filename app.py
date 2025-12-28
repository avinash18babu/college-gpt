import streamlit as st
from openai import OpenAI
import os

st.set_page_config(
    page_title="SA College Information Portal",
    page_icon="🎓",
    layout="wide"
)

st.markdown("<h1 style='text-align:center;'>🎓 SA College of Arts & Science</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Affiliated to University of Madras</h4>", unsafe_allow_html=True)
st.divider()

st.sidebar.title("📘 Navigation")
menu = st.sidebar.radio(
    "Go to",
    [
        "🏫 About College",
        "📍 Location",
        "🏢 Departments",
        "📚 Courses & Syllabus",
        "🤖 Ask College GPT"
    ]
)

if menu == "🏫 About College":
    st.header("About the College")
    st.write("""
    **SA College of Arts & Science (SACAS)** is a reputed institution in Chennai,
    committed to academic excellence and holistic development.

    **Affiliation:** University of Madras  
    **Type:** Arts & Science College  
    **Data Source:** Official College Website
    """)

elif menu == "📍 Location":
    st.header("College Location")
    st.write("""
    **Location:** Chennai, Tamil Nadu  
    **Campus:** Well-equipped with academic and infrastructure facilities.
    """)

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

elif menu == "📚 Courses & Syllabus":
    st.header("Courses & Syllabus Overview")
    st.write("""
    **UG Courses:**  
    - B.Sc Computer Science  
    - B.Sc Computer Science with AI  
    - B.Com  
    - BBA  

    **PG Courses:**  
    - M.Sc Computer Science  
    - M.Com  

    *Detailed syllabus is as per University of Madras norms.*
    """)

elif menu == "🤖 Ask College GPT":
    st.header("Ask College GPT")
    question = st.text_input("Ask about subjects, exams, or concepts")

    if st.button("Ask"):
        if question:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
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

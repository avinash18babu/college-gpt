import streamlit as st
from openai import OpenAI
import os

st.set_page_config(page_title="College GPT", page_icon="🤖")

st.title("🤖 College GPT")
st.write("Ask any college-related question")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

question = st.text_input("Your question")

if st.button("Ask"):
    if question:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful college assistant."},
                {"role": "user", "content": question}
            ]
        )
        st.success(response.choices[0].message.content)
    else:
        st.warning("Please enter a question")

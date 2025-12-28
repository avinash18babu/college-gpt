from openai import OpenAI
import streamlit as st
import os

st.title("College GPT")
st.write("Ask any college-related question")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

question = st.text_input("Your question")

if st.button("Ask") and question:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful college assistant."},
            {"role": "user", "content": question}
        ]
    )
    st.write(response.choices[0].message.content)

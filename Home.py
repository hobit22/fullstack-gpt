import streamlit as st
from datetime import datetime
from langchain.prompts import PromptTemplate

today = datetime.today().strftime("%H:%M:%S")

st.title(today)

model = st.selectbox(
    "Choose your model", 
    ("GPT-3", "GPT-4")
)

if model == 'GPT-3':
    st.write("cheap")
else:
    st.write("not cheap")
    
    name = st.text_input("what is your name?")

    st.write(name)


    value = st.slider(
        "temperature", 
        min_value=0.0, 
        max_value=2.0,
        step=0.1
    )


import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

load_dotenv() # Load your API key from a .env file

genai.configure(api_key="YOUR_GEMINI_API_KEY")

def get_gemini_reponse(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Prompt Template
input_prompt = """
As an experienced HR Manager with tech expertise, evaluate the resume against the job description. 
1. Give a percentage match based on keywords.
2. List missing keywords.
3. Provide specific suggestions to improve the ATS score.
4. Suggest 3 job roles/opportunities this candidate is ready for.
Format the output attractively with bullet points.
"""

## Streamlit UI Design
st.set_page_config(page_title="Smart ATS Tracker", page_icon="📄", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 Smart ATS Resume Expert")
st.subheader("Improve your selection rate for Jobs & Internships")

col1, col2 = st.columns([1, 1])

with col1:
    jd = st.text_area("Paste the Job Description (JD) here:", height=250)

with col2:
    uploaded_file = st.file_uploader("Upload your Resume (PDF)...", type=["pdf"])
    if uploaded_file is not None:
        st.success("Resume Uploaded Successfully!")

submit = st.button("Analyze Resume")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_reponse(jd, [text], input_prompt)
        st.subheader("The Results:")
        st.markdown(response)
    else:
        st.error("Please upload a resume first.")
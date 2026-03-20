import streamlit as st
import os
import PyPDF2 as pdf
from groq import Groq # New Library
from dotenv import load_dotenv

load_dotenv()

# --- Setup Groq Client ---
# Add GROQ_API_KEY to your Streamlit Secrets!
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if api_key:
    client = Groq(api_key=api_key)
else:
    st.error("⚠️ Please add GROQ_API_KEY to your Secrets.")

def get_groq_response(jd, resume_text):
    # We use Llama 3.3 70B - it's powerful and free on Groq
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert ATS (Applicant Tracking System) analyzer."},
            {"role": "user", "content": f"Analyze this Resume against the Job Description.\n\nJD: {jd}\n\nResume: {resume_text}\n\nProvide: 1. Match %, 2. Missing Keywords, 3. Improvement Tips."}
        ],
    )
    return completion.choices[0].message.content

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += str(page.extract_text())
    return text

# --- Attractive UI ---
st.set_page_config(page_title="Flash ATS Tracker", page_icon="⚡")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: white; }
    .stButton>button { background: #3b82f6; color: white; border-radius: 8px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ Flash ATS Resume Tracker")
st.write("Using Llama 3.3 via Groq for ultra-fast analysis.")

jd = st.text_area("Paste Job Description", height=200)
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if st.button("Start Analysis"):
    if uploaded_file and jd:
        with st.spinner("Analyzing at light speed..."):
            resume_text = input_pdf_text(uploaded_file)
            response = get_groq_response(jd, resume_text)
            st.success("Analysis Complete!")
            st.markdown(response)
    else:
        st.warning("Please upload a file and paste a JD.")

import streamlit as st
from groq import Groq
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

load_dotenv()

# --- INITIALIZE GROQ CLIENT ---
# This part must be outside the functions so it is "defined" globally
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if api_key:
    client = Groq(api_key=api_key) # Now 'client' is defined!
else:
    st.error("⚠️ GROQ_API_KEY not found in Secrets. Please add it to Streamlit Settings.")
    st.stop() # Stops the app here so it doesn't crash later

def get_groq_response(jd, resume_text):
    # Prompt engineering to get the best result
    input_prompt = f"""
    Act as an advanced ATS (Applicant Tracking System). 
    Analyze the following resume against the job description.
    
    Job Description: {jd}
    Resume Content: {resume_text}
    
    Provide a detailed report including:
    1. Match Percentage (0-100%)
    2. Missing Keywords
    3. Final Thought on candidate fit
    4. Improvement Suggestions
    """
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a professional HR and ATS analyzer."},
            {"role": "user", "content": input_prompt}
        ],
    )
    return completion.choices[0].message.content

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += str(page.extract_text())
    return text

# --- UI DESIGN ---
st.set_page_config(page_title="Flash ATS Tracker", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0f172a; color: white; }
    .stTextArea textarea { border: 2px solid #3b82f6; border-radius: 10px; }
    .stButton>button { 
        background: linear-gradient(45deg, #3b82f6, #2dd4bf); 
        color: white; border-radius: 10px; font-weight: bold; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ AI-Powered Flash ATS Tracker")
st.write("Using Llama 3.3 for lightning-fast resume optimization.")

col1, col2 = st.columns([1, 1])

with col1:
    jd = st.text_area("🎯 Job Description", height=250, placeholder="Paste job requirements here...")

with col2:
    uploaded_file = st.file_uploader("📂 Upload Resume (PDF)", type=["pdf"])
    if uploaded_file:
        st.success("File uploaded!")

if st.button("Start AI Analysis"):
    if uploaded_file and jd:
        with st.spinner("Analyzing..."):
            resume_text = input_pdf_text(uploaded_file)
            response = get_groq_response(jd, resume_text)
            st.markdown("---")
            st.subheader("📊 Results")
            st.markdown(response)
            st.balloons()
    else:
        st.warning("Please upload a resume and paste a Job Description.")

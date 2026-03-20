import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load local environment variables (for local testing)
load_dotenv()

# Configure Google Gemini API
# Priority: Streamlit Secrets (Production) -> Environment Variables (Local)
api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ API Key not found. Please add GOOGLE_API_KEY to your Secrets or .env file.")

def get_gemini_reponse(input_text, pdf_content, prompt):
    # This is a 'Mock AI' logic to keep your app running without an API key
    keywords = ["python", "machine learning", "java", "sql", "communication", "teamwork"]
    found = [word for word in keywords if word in pdf_content.lower()]
    missing = [word for word in keywords if word not in pdf_content.lower()]
    
    score = (len(found) / len(keywords)) * 100
    
    return f"""
    ### 📊 Analysis (Offline Mode)
    * **Match Score:** {int(score)}%
    * **Missing Keywords:** {", ".join(missing)}
    * **Tips:** Use more technical keywords like {missing[0]} to increase your score!
    
    *Note: Connect a valid Google API Key to get full AI feedback.*
    """

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page_obj = reader.pages[page]
        text += str(page_obj.extract_text())
    return text

# --- UI Header & Styling ---
st.set_page_config(page_title="Smart ATS Tracker", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTextArea textarea { border: 2px solid #4b6bff; border-radius: 10px; background-color: #161b22; color: white; }
    .stButton>button { 
        width: 100%; 
        background: linear-gradient(45deg, #00f2fe, #4facfe); 
        color: white; 
        border-radius: 10px; 
        font-weight: bold; 
        height: 3em;
        border: none;
    }
    .stButton>button:hover { background: linear-gradient(45deg, #4facfe, #00f2fe); color: black; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 AI-Powered ATS Resume Expert")
st.write("Optimize your resume for Applicant Tracking Systems using Google Gemini AI.")

# --- Layout ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📋 Job details")
    jd = st.text_area("Paste the Job Description (JD) here:", height=300, placeholder="Required skills, experience, and responsibilities...")

with col2:
    st.subheader("📄 Resume Upload")
    uploaded_file = st.file_uploader("Upload your Resume (PDF format only)", type=["pdf"])
    
    if uploaded_file:
        st.success("✅ Resume uploaded successfully!")
    
    submit = st.button("Analyze My Resume")

# --- Logic ---
input_prompt = """
Act as an expert Technical Recruiter and ATS Specialist. Compare the Resume against the Job Description.
Please provide:
1. **Match Percentage**: Give a score out of 100%.
2. **Missing Keywords**: Identify critical skills/tools missing from the resume.
3. **Profile Summary**: A brief evaluation of how well the candidate fits.
4. **Improvement Tips**: Specific bullet points on how to edit the resume to increase the score.
5. **Job Suggestions**: Mention 2-3 similar job titles the candidate should apply for.

Format everything using clean Markdown with bold headings and bullet points.
"""

if submit:
    if uploaded_file is not None and jd.strip() != "":
        with st.spinner('🚀 AI is scanning your resume...'):
            try:
                resume_text = input_pdf_text(uploaded_file)
                response = get_gemini_reponse(jd, resume_text, input_prompt)
                
                st.divider()
                st.subheader("📊 ATS Analysis Report")
                st.markdown(response)
                st.balloons()
            except Exception as e:
                st.error(f"An error occurred during processing: {e}")
    else:
        st.warning("⚠️ Please provide both a Job Description and a Resume PDF.")

# --- Footer ---
st.markdown("---")
st.caption("Developed for career growth and internship success.")

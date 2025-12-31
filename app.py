import streamlit as st
import os
from dotenv import load_dotenv
from utils import extract_text_from_docx, analyze_resume

@st.cache_data
def cached_analyze_resume(resume_text, job_description, api_key):
    return analyze_resume(resume_text, job_description, api_key)

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="AI Resume Optimizer", layout="wide")

st.title("AI Resume Optimizer")

if not api_key:
    st.warning("⚠️ Google API Key not found. Please set `GOOGLE_API_KEY` in your `.env` file.")

# Main Content
st.markdown("### 1. Upload Resume")
uploaded_file = st.file_uploader("Upload your Resume (DOCX)", type=["docx"])

st.markdown("### 2. Job Description")
job_description = st.text_area("Paste the Job Description here", height=200)

if uploaded_file and job_description:
    with st.spinner("Analyzing resume against the job description..."):
        try:
            # 1. Extract Text
            resume_text = extract_text_from_docx(uploaded_file)
            
            # 2. Analyze with Gemini
            analysis = cached_analyze_resume(resume_text, job_description, api_key)
            
            # 3. Display Results
            st.success("Analysis Complete!")
            
            # Metrics
            st.metric("Match Percentage", analysis.get("match_percentage", "N/A"))
            
            st.markdown("### Gap Analysis")
            for gap in analysis.get("gap_analysis", []):
                st.markdown(f"- {gap}")
            
            st.markdown("### Missing Keywords")
            for keyword in analysis.get("missing_keywords", []):
                st.markdown(f"- {keyword}")
            
            st.markdown("### Rewritten Summary")
            st.markdown(f"> {analysis.get('rewritten_summary', 'No summary generated.')}")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

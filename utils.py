import docx
import json
import re
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List

def extract_text_from_docx(file):
    """
    Extracts text from a DOCX file.
    """
    doc = docx.Document(file)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text)

def extract_json(response_text):
    """
    Extracts JSON from a string that might contain other text or code blocks.
    """
    try:
        # First try parsing the entire string
        return json.loads(response_text)
    except json.JSONDecodeError:
        # Look for code blocks
        match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Look for raw JSON object if no code blocks or pure JSON
        match = re.search(r'(\{.*\})', response_text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
                
    return None

import time

class ResumeAnalysis(BaseModel):
    match_percentage: str = Field(description="The match percentage between the resume and job description, e.g. '85%'")
    gap_analysis: List[str] = Field(description="List of gaps found in the resume compared to the job description")
    missing_keywords: List[str] = Field(description="Key skills and keywords from the JD missing in the resume")
    rewritten_summary: str = Field(description="A rewritten resume summary that better aligns with the job description")

def analyze_resume(resume_text, job_description, api_key):
    """
    Analyzes the resume against the job description using Google Gemini.
    """
    if not api_key:
        raise ValueError("API Key is missing")

    genai.configure(api_key=api_key)
    
    # Models to try in order of preference
    models_to_try = ['gemini-2.0-flash', 'gemini-flash-latest']
    
    last_exception = None

    for model_name in models_to_try:
        model = genai.GenerativeModel(model_name)
        
        prompt = f"""
        You are an expert Resume Optimizer and Career Coach. 
        Your task is to analyze a Candidate's Resume against a Job Description (JD).

        Resume Content:
        {resume_text}

        Job Description:
        {job_description}

        Please provide a structured analysis in valid JSON format with the following keys:
        1. "match_percentage": (string) Estimated match percentage (e.g., "75%").
        2. "gap_analysis": (list of strings) Describe specific gaps (skills, experience, or tone) in the resume compared to the JD.
        3. "missing_keywords": (list of strings) Important keywords or hard skills from the JD that are not present in the resume.
        4. "rewritten_summary": (string) A rewritten professional summary for the resume that incorporates the missing keywords and aligns with the JD's tone.

        Ensure the output is ONLY valid JSON. Do not include any other text.
        """

        max_retries = 3
        retry_delay = 2  # Start with 2 seconds

        for attempt in range(max_retries):
            try:
                response = model.generate_content(prompt)
                parsed_json = extract_json(response.text)
                
                if not parsed_json:
                    # If parsing fails, try the next attempt (or model)
                    last_exception = ValueError(f"Could not parse model response from {model_name}")
                    continue
                    
                return parsed_json

            except Exception as e:
                last_exception = e
                if "429" in str(e) or "quota" in str(e).lower():
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                        continue
                    else:
                        # Move to the next model in the outer loop
                        break 
                else:
                    # For non-quota errors, maybe we shouldn't retry? 
                    # But for now, let's treat them as potentially transient or model-specific
                    # and allow moving to the next model if this one consistently fails.
                    break

    # If we exhaust all models and retries
    error_msg = str(last_exception) if last_exception else "Unknown error"
    return {
        "match_percentage": "Error",
        "gap_analysis": [f"Analysis failed after trying multiple models. Last error: {error_msg}"],
        "missing_keywords": [],
        "rewritten_summary": "Error generating summary."
    }


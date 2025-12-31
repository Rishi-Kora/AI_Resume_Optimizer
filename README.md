# AI Resume Optimizer

## Problem Statement
Job seekers often struggle to get past Applicant Tracking Systems (ATS) and recruiters because their generic resumes do not perfectly align with specific Job Descriptions (JDs).Manually tailoring a resume for every application is time-consuming, and candidates often miss critical keywords or fail to frame their experience to match requirements.

## Solution
This project acts as an intelligent "Career Coach" to bridge the gap between a candidate's resume and a target job. It automates the optimization process using the following features:

1.  **Gap Analysis:** Instantly identifies missing skills, experience years, and specific tools compared to the JD.
2.  **Keyword Optimization:** Detects high-value keywords and hard skills (e.g., "Docker", "Kubernetes") present in the JD but absent in the resume.
3.  **Content Refinement:** Automatically generates a rewritten **Professional Summary** that aligns the tone with the job description to increase shortlisting chances.

## Workflow
The system follows a streamlined workflow to process data and generate insights:

1.  **User Input:** The user uploads a `.docx` resume and pastes the Job Description.
2.  **Detection & Automation:** The system detects when both inputs are present and automatically triggers analysis.
3.  **Caching:** Results are checked against `@st.cache_data` to save API credits and avoid re-analyzing the same data.
4.  **Processing:** * Text is extracted from the resume.
    * Google Gemini AI (`gemini-2.0-flash`) compares the Resume vs. JD.
5.  **Visualization:** The AI response is parsed into JSON and rendered into a readable dashboard.

## Workflow Diagram

<img width="827" height="1338" alt="image" src="https://github.com/user-attachments/assets/f86bb843-adee-4548-a45b-12ad2b5f29a0" />



## Project Structure

### 1. `utils.py` (Backend & AI)
This file handles the "heavy lifting" including file processing and AI interaction.
* **`extract_text_from_docx(file)`:** Converts uploaded `.docx` resumes into plain text strings.
* **`analyze_resume(...)`:** Configures the Gemini API, selects the `gemini-2.0-flash` model, and sends the comparison prompt.It includes retry logic for API limits.
* **`extract_json(response_text)`:** A helper function that cleans the AI response to ensure it is valid JSON, stripping markdown formatting.

### 2. `app.py` (Frontend Interface)
This file builds the web interface using **Streamlit**.
* **Layout:** Displays "Upload Resume" and "Job Description" inputs in a vertical stack.
* **Automation:** Triggers analysis immediately when inputs are detected.
* **Caching:** Implements `@st.cache_data` to store results and optimize performance during interaction.
* **Visualization:** Renders the JSON output from `utils.py` into the final dashboard.

## Tech Stack
* **Frontend:** Streamlit
* **AI Model:** Google Gemini (gemini-2.0-flash)
* **Language:** Python

## Usage
1.  Clone the repository.
2.  Install dependencies (Streamlit, Google Generative AI SDK, etc.).
3.  Run the application:
    ```bash
    streamlit run app.py
    ```
4.  Upload your Resume (`.docx`) and paste the Job Description to receive instant feedback.

**NOTE:** Use your own **API Key** and **Model.**

import pdfplumber
import json
import os
import re
from langchain_google_genai import ChatGoogleGenerativeAI



def parse_pdf(filepath):
    """
    Extract text from a PDF file using pdfplumber.
    """

    text = ""

    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"

    return text



def extract_skills_from_resume(resume_text: str, GOOGLE_API_KEY: str):
    """
    Very simple skill extraction:
    - LLM returns JSON dict: { "skills": [...] }
    - Extract skills list and return top 10
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1,
        google_api_key=GOOGLE_API_KEY,
    )

    prompt = f"""
        Extract the TOP 10 most important technical skills from the resume below.

        Allowed categories only:
        - Programming languages
        - Frameworks / libraries
        - Databases
        - Cloud platforms
        - DevOps tools

        Return output STRICTLY as valid JSON in this exact format:

        {{"skills": ["Skill1", "Skill2", "Skill3"]}}

        No explanations. No extra text.

        Resume:
        ---------
        {resume_text}
        ---------
    """

    try:
        response = llm.invoke(prompt)
        raw = response.content.strip()

        # --- Extract ONLY the JSON dictionary safely ---
        json_match = re.search(r"\{.*\}", raw, re.DOTALL)

        if not json_match:
            return []

        json_text = json_match.group(0)

        # --- Parse JSON ---
        data = json.loads(json_text)

        skills = data.get("skills", [])
        return skills[:10]

    except Exception as e:
        print("❌ Error extracting skills:", e)
        return []
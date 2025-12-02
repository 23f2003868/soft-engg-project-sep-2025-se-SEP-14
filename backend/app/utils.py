import pdfplumber
import json
import os
import re
from langchain_google_genai import ChatGoogleGenerativeAI



def parse_pdf(filepath):
    """
    Extract text from a PDF file using pdfplumber.
    """

    try:
        text = ""

        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                content = page.extract_text()
                if content:
                    text += content + "\n"

        return text.strip()
    
    except Exception as e:
        print("PDF Parse Error:", e)
        return ""




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
    Extract ONLY the **technical skills** from this resume.

    Allowed categories:
    - Programming languages
    - Frameworks / libraries
    - Databases
    - Cloud platforms
    - DevOps tools

    Return STRICT JSON:
    {{
        "skills": ["Skill1", "Skill2", ...]
    }}

    NO explanation.
    NO markdown.
    ONLY JSON.

        Resume:
        ---------
        {resume_text}
        ---------
    """

    try:
        response = llm.invoke(prompt)
        raw = response.content.strip()

        json_match = re.search(r"\{.*?\}", raw, re.DOTALL)

        if not json_match:
            return []

        data = json.loads(json_match.group(0))
        skills = data.get("skills", [])

        clean = []
        for s in skills:
            s = s.strip().title()
            if s and s not in clean:
                clean.append(s)

        return clean[:10]

    except Exception as e:
        print("Skill extraction error:", e)
        return []

from openai import OpenAI
from dotenv import load_dotenv
import os, json, openai
from app.models.resume import Resume, EducationItem, ProfessionalExperienceItem, ProjectItem, AwardItem, CertificationItem, SkillItem
from typing import Dict, Any, List
import logging
from pathlib import Path
import PyPDF2
from pydantic import ValidationError
from app.utils.openai_client import openai_client

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

logger = logging.getLogger(__name__)

def extract_resume(file_path: str) -> Resume:
    """
    Extract resume data from a PDF file and return a validated Resume object.
    """
    try:
        # Extract text from PDF
        cv_text = extract_text_from_cv(file_path)
        
        # Extract structured data
        structured_data = extract_structured_data_from_cv(cv_text)
        
        # Create Resume object with proper validation
        try:
            resume = Resume(
                name=structured_data.get("name", "Unknown"),
                location=structured_data.get("location", "Unknown"),
                social=structured_data.get("social", []),
                email=structured_data.get("email", "Unknown"),
                linkedin=structured_data.get("linkedin"),
                phone=structured_data.get("phone", "Unknown"),
                intro=structured_data.get("intro", ""),
                education=[
                    EducationItem(
                        school=edu.get("school", "Unknown"),
                        class_year=edu.get("class_year", "Unknown"),
                        major=edu.get("major", ""),
                        minor=edu.get("minor"),
                        gpa=float(edu["gpa"]) if edu.get("gpa") and str(edu["gpa"]).replace(".", "").isdigit() else None
                    ) 
                    for edu in structured_data.get("education", [])
                ],
                professional_experience=[
                    ProfessionalExperienceItem(
                        company=exp.get("company", "Unknown"),
                        location=exp.get("location", ""),
                        position=exp.get("position", "Unknown"),
                        seniority=exp.get("seniority", ""),
                        duration=exp.get("duration", "Unknown"),
                        description=exp.get("description", "")
                    )
                    for exp in structured_data.get("professional_experience", [])
                ],
                projects=[
                    ProjectItem(
                        name=proj.get("name", "Unknown"),
                        link=proj.get("link"),
                        tech=proj.get("tech"),
                        duration=proj.get("duration"),
                        description=proj.get("description", "")
                    )
                    for proj in structured_data.get("projects", [])
                ],
                awards=[
                    AwardItem(
                        contest=award.get("contest", "Unknown"),
                        prize=award.get("prize", "Unknown"),
                        description=award.get("description", ""),
                        role=award.get("role"),
                        link=award.get("link"),
                        time=award.get("time", "")
                    )
                    for award in structured_data.get("awards", [])
                ],
                certifications=[
                    CertificationItem(
                        name=cert.get("name", "Unknown"),
                        link=cert.get("link"),
                        org=cert.get("org")
                    )
                    for cert in structured_data.get("certifications", [])
                ],
                skills=[
                    SkillItem(
                        name=skill.get("name", "Unknown"),
                        list=skill.get("list", [])
                    )
                    for skill in structured_data.get("skills", [])
                ]
            )
            return resume
            
        except ValidationError as e:
            logger.error(f"Validation error creating Resume object: {str(e)}")
            # Return a default Resume object instead of raising an error
            return Resume()
            
    except Exception as e:
        logger.error(f"Error in extract_resume: {str(e)}")
        # Return a default Resume object instead of raising an error
        return Resume()

def extract_text_from_cv(file_path: str) -> str:
    """
    Extract text from PDF file with enhanced error handling.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        if not file_path.lower().endswith('.pdf'):
            raise ValueError("File must be a PDF")
            
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                try:
                    text += page.extract_text() + "\n"
                except Exception as e:
                    logger.warning(f"Error extracting text from page: {str(e)}")
                    continue
                    
            if not text.strip():
                raise ValueError("No text could be extracted from the PDF")
                
            return text
                
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise

def create_default_structure() -> Dict[str, Any]:
    """
    Creates a default structure for the resume data.
    """
    return {
        "extracted_data": {
            "name": "Unknown",
            "location": "Unknown",
            "social": [],
            "email": "Unknown",
            "linkedin": None,
            "phone": "Unknown",
            "intro": "No introduction provided.",
            "education": [],
            "professional_experience": [],
            "projects": [],
            "awards": [],
            "certifications": [],
            "skills": [{"name": "Unknown", "list": []}]
        },
        "summary": "Unable to generate summary.",
        "evaluation": "Unable to generate evaluation.",
        "scoring_recommendations": {
            "education": {"score": 0, "reasoning": "Unable to evaluate"},
            "experience": {"score": 0, "reasoning": "Unable to evaluate"},
            "projects": {"score": 0, "reasoning": "Unable to evaluate"},
            "awards": {"score": 0, "reasoning": "Unable to evaluate"},
            "certifications": {"score": 0, "reasoning": "Unable to evaluate"}
        }
    }

def extract_structured_data_from_cv(cv_text: str) -> Dict[str, Any]:
    """
    Extract structured data, summary, and evaluation from CV text using a single OpenAI API call.
    """
    client = openai_client.get_client()
    
    if not cv_text.strip():
        raise ValueError("Empty CV text provided")
    
    # Clean the CV text by removing any markdown-style code block markers.
    cleaned_cv_text = cv_text.replace("```", "").strip()
    
    prompt = f"""Analyze the following CV and provide:
        1. A detailed and complete list of projects (ensure no project is missing),
        2. Structured data extraction, a brief summary, detailed evaluation, and initial scoring recommendations.

        Important Instructions:
        - If there are multiple projects, do not truncate the list.
        - If a field is empty or not found, use an empty string "" for text fields and [] for lists.
        - Never return null/None for required fields.

        Return the results in the following JSON format exactly:
        {{
            "extracted_data": {{
                "name": "string",
                "location": "string",
                "social": ["string"],
                "email": "string",
                "linkedin": "string or null",
                "phone": "string",
                "intro": "string",
                "education": [{{
                    "school": "string",
                    "class_year": "string",
                    "major": "string",
                    "gpa": "number or null"
                }}],
                "professional_experience": [{{
                    "company": "string",
                    "location": "string",
                    "position": "string",
                    "seniority": "string",
                    "duration": "string",
                    "description": "string"
                }}],
                "projects": [{{
                    "name": "string",
                    "tech": "string",
                    "duration": "string",
                    "description": "string"
                }}],
                "awards": [{{
                    "contest": "string",
                    "prize": "string",
                    "description": "string",
                    "time": "string"
                }}],
                "certifications": [{{
                    "name": "string",
                    "org": "string",
                    "link": "string"
                }}],
                "skills": [{{
                    "name": "string",
                    "list": ["string"]
                }}]
            }},
            "summary": "string",
            "evaluation": "string",
            "scoring_recommendations": {{
                "education": {{"score": "number", "reasoning": "string"}},
                "experience": {{"score": "number", "reasoning": "string"}},
                "projects": {{"score": "number", "reasoning": "string"}},
                "awards": {{"score": "number", "reasoning": "string"}},
                "certifications": {{"score": "number", "reasoning": "string"}}
            }}
        }}

        CV Text:
        {cleaned_cv_text}
        """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a professional CV parser. Return only valid JSON that matches the required structure exactly."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,
            temperature=0
        )
        
        response_content = response.choices[0].message.content.strip()
        # Remove markdown formatting markers if present.
        response_content = response_content.replace("```json", "").replace("```", "").strip()
        
        if not response_content:
            logger.error("Empty response from API")
            return create_default_structure()
        
        try:
            structured_data = json.loads(response_content)
            if not isinstance(structured_data, dict) or "extracted_data" not in structured_data:
                logger.error("Response JSON missing required 'extracted_data' field")
                return create_default_structure()
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Raw response: {response_content}")
            return create_default_structure()
            
    except Exception as e:
        logger.error(f"Error during API call: {e}")
        return create_default_structure()
    
    # Ensure all required fields exist.
    default_structure = create_default_structure()
    for key in default_structure:
        if key not in structured_data:
            structured_data[key] = default_structure[key]
    
    return structured_data
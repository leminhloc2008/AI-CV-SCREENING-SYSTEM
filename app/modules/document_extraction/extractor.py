from app.models.resume import Resume, EducationItem, ProfessionalExperienceItem, ProjectItem, AwardItem, CertificationItem, SkillItem
from .ocr import extract_structured_data_from_cv
import re
from typing import List, Optional

def extract_resume(file_path: str) -> Resume:
    """
    Extract structured data from a CV (PDF or DOCX) using LLM and return a Resume object.
    """
    # Extract raw text from the CV
    cv_text = extract_text_from_cv(file_path)

    # Use LLM to extract structured data
    structured_data = extract_structured_data_from_cv(cv_text)

    print(structured_data)

    # Convert the structured data into a Resume object
    return Resume(
        name=structured_data.get("name", "Unknown"),
        location=structured_data.get("location", "Unknown"),
        social=structured_data.get("social", []),
        email=structured_data.get("email", "Unknown"),
        linkedin=structured_data.get("linkedin", None),
        phone=structured_data.get("phone", "Unknown"),
        intro=structured_data.get("intro", "No introduction provided."),
        education=[EducationItem(**edu) for edu in structured_data.get("education", [])],
        professional_experience=[ProfessionalExperienceItem(**exp) for exp in structured_data.get("professional_experience", [])],
        projects=[ProjectItem(**proj) for proj in structured_data.get("projects", [])],
        awards=[AwardItem(**award) for award in structured_data.get("awards", [])],
        certifications=[CertificationItem(**cert) for cert in structured_data.get("certifications", [])],
        skills=[SkillItem(**skill) for skill in structured_data.get("skills", [])]
    )

def extract_text_from_cv(file_path: str) -> str:
    """
    Extract raw text from a CV file (PDF or DOCX).
    """
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    else:
        # Assume it's a plain text file
        with open(file_path, "r") as file:
            return file.read()

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file.
    """
    import PyPDF2
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from a DOCX file.
    """
    from docx import Document
    doc = Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text
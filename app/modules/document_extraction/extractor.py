from app.models.resume import Resume, EducationItem, ProfessionalExperienceItem, ProjectItem, AwardItem, CertificationItem, SkillItem
from .ocr import extract_structured_data_from_cv, create_default_structure
from typing import Dict, Any

def extract_resume(file_path: str) -> Resume:
    """
    Extract structured data from a CV and return a Resume object.
    """
    # Extract raw text from the CV (assuming extract_text_from_cv is defined elsewhere)
    cv_text = extract_text_from_cv(file_path)

    # Get structured data and analysis from the LLM
    result = extract_structured_data_from_cv(cv_text)
    structured_data = result.get("extracted_data", {})

    # Convert numeric fields in education (e.g., GPA) so that scoring functions receive numbers.
    education_items = structured_data.get("education", [])
    for edu in education_items:
        if "gpa" in edu:
            try:
                edu["gpa"] = float(edu["gpa"])
            except Exception:
                edu["gpa"] = None

    # Build and return the Resume object
    resume = Resume(
        name=structured_data.get("name", "Unknown"),
        location=structured_data.get("location", "Unknown"),
        social=structured_data.get("social", []),
        email=structured_data.get("email", "Unknown"),
        linkedin=structured_data.get("linkedin", None),
        phone=structured_data.get("phone", "Unknown"),
        intro=structured_data.get("intro", "No introduction provided."),
        education=[EducationItem(**edu) for edu in education_items],
        professional_experience=[ProfessionalExperienceItem(**exp) for exp in structured_data.get("professional_experience", [])],
        projects=[ProjectItem(**proj) for proj in structured_data.get("projects", [])],
        awards=[AwardItem(**award) for award in structured_data.get("awards", [])],
        certifications=[CertificationItem(**cert) for cert in structured_data.get("certifications", [])],
        skills=[SkillItem(**skill) for skill in structured_data.get("skills", [])]
    )
    
    return resume

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
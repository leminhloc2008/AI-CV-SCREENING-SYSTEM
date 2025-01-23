from app.models.resume import Resume
from app.models.scoring_rules import SCORING_RULES
from .education import calculate_education_score
from .experience import calculate_experience_score
from .projects import calculate_projects_score
from .awards import calculate_awards_score
from .certifications import calculate_certifications_score

def calculate_total_score(resume: Resume) -> dict:
    """
    Calculate the total score for a resume by aggregating scores from all fields.
    """
    # Calculate scores for each section
    education_score = calculate_education_score(resume.education)
    experience_score = calculate_experience_score(resume.professional_experience)
    projects_score = calculate_projects_score(resume.projects)
    awards_score = calculate_awards_score(resume.awards)
    certifications_score = calculate_certifications_score(resume.certifications)
    
    # Weighted sum
    total_score = (
        education_score * (SCORING_RULES["education"]["weight"] / 100) +
        experience_score * (SCORING_RULES["professional_experience"]["weight"] / 100) +
        projects_score * (SCORING_RULES["projects"]["weight"] / 100) +
        awards_score * (SCORING_RULES["awards"]["weight"] / 100) +
        certifications_score * (SCORING_RULES["certifications"]["weight"] / 100)
    )
    
    # Determine status
    status = "Pass" if total_score >= 70 else ("Consider" if total_score >= 50 else "Fail")
    
    return {
        "total_score": total_score,
        "status": status
    }
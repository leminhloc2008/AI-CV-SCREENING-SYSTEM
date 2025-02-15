from typing import Dict, Any, List
import logging
from app.models.resume import (
    Resume, 
    EducationItem, 
    ProfessionalExperienceItem, 
    ProjectItem, 
    AwardItem, 
    CertificationItem
)
from app.models.scoring_rules import SCORING_RULES
from app.utils.openai_client import openai_client

logger = logging.getLogger(__name__)

def calculate_education_item_score(edu: EducationItem) -> float:
    score = 0
    if edu.school and edu.school != "Unknown":
        score += SCORING_RULES["education"].get("school", 0)
    if edu.class_year:
        score += SCORING_RULES["education"].get("class_year", 0)
    if edu.major:
        score += SCORING_RULES["education"].get("major", 0)
    if edu.gpa is not None:
        try:
            gpa = float(edu.gpa)
            # Scale GPA out of 4 to the allotted gpa points
            score += SCORING_RULES["education"].get("gpa", 0) * (gpa / 4.0)
        except Exception:
            pass
    return score

def calculate_experience_item_score(exp: ProfessionalExperienceItem) -> float:
    score = 0
    # In our test example, we assume:
    # - Company contributes 25 points if provided,
    # - Location adds 5,
    # - Position adds 25,
    # - Seniority adds 5,
    # - Duration adds 5,
    # - Description adds 25.
    if exp.company and exp.company != "Unknown":
        score += 25
    if exp.location and exp.location != "Unknown":
        score += 5
    if exp.position and exp.position != "Unknown":
        score += 25
    if exp.seniority and exp.seniority != "Unknown":
        score += 5
    if exp.duration and exp.duration != "Unknown":
        score += 5
    if exp.description and exp.description.strip():
        score += 25
    return score

def calculate_project_item_score(project: ProjectItem) -> float:
    score = 0
    if project.name and project.name != "Unknown":
        score += 10
    if getattr(project, "link", None):
        score += 20
    if getattr(project, "tech", None):
        score += 25
    if getattr(project, "duration", None):
        score += 5
    if project.description and project.description.strip():
        score += 40
    return score

def calculate_award_item_score(award: AwardItem) -> float:
    score = 0
    if award.contest and award.contest != "Unknown":
        score += 30
    if award.prize and award.prize != "Unknown":
        score += 25
    if award.description and award.description.strip():
        score += 25
    if getattr(award, "role", None):
        score += 10
    if getattr(award, "link", None):
        score += 5
    if getattr(award, "time", None):
        score += 5
    return score

def calculate_certification_item_score(cert: CertificationItem) -> float:
    score = 0
    if cert.name and cert.name != "Unknown":
        score += 50
    if getattr(cert, "link", None):
        score += 10
    if cert.org and cert.org != "Unknown":
        score += 40
    return score

def best_item_score(items: List, calc_func) -> float:
    """
    Compute the highest score among items using the provided calculation function.
    If no items exist, return 0.
    The result is capped to a maximum of 100.
    """
    if not items:
        return 0.0
    return min(max(calc_func(item) for item in items), 100)

def calculate_total_score(resume: Resume) -> Dict[str, Any]:
    """
    Calculate the overall weighted score for a resume.
    Each category’s raw score (out of 100) is computed and then weighted according to PRD:
      - Education: 15%
      - Professional Experience: 25%
      - Projects: 20%
      - Awards: 15%
      - Certifications: 5%
    
    Returns:
        Dictionary containing raw scores, weighted scores, overall total score,
        and status ("Pass", "Consider", or "Fail").
    """
    try:
        raw_education = best_item_score(resume.education, calculate_education_item_score)
        raw_experience = best_item_score(resume.professional_experience, calculate_experience_item_score)
        raw_projects = best_item_score(resume.projects, calculate_project_item_score)
        raw_awards = best_item_score(resume.awards, calculate_award_item_score)
        raw_certifications = best_item_score(resume.certifications, calculate_certification_item_score)
    
        weighted_education = raw_education * (SCORING_RULES["education"]["weight"] / 100)
        weighted_experience = raw_experience * (SCORING_RULES["professional_experience"]["weight"] / 100)
        weighted_projects = raw_projects * (SCORING_RULES["projects"]["weight"] / 100)
        weighted_awards = raw_awards * (SCORING_RULES["awards"]["weight"] / 100)
        weighted_certifications = raw_certifications * (SCORING_RULES["certifications"]["weight"] / 100)
    
        total_score = (weighted_education +
                       weighted_experience +
                       weighted_projects +
                       weighted_awards +
                       weighted_certifications)
    
        # Determine status based on weighted total score thresholds.
        status = "Pass" if total_score >= 70 else "Consider" if total_score >= 50 else "Fail"
    
        return {
            "scores": {
                "education": raw_education,
                "experience": raw_experience,
                "projects": raw_projects,
                "awards": raw_awards,
                "certifications": raw_certifications,
            },
            "weighted_scores": {
                "education": weighted_education,
                "experience": weighted_experience,
                "projects": weighted_projects,
                "awards": weighted_awards,
                "certifications": weighted_certifications,
            },
            "total_score": total_score,
            "status": status
        }
    except Exception as e:
        logger.error(f"Error calculating total score: {str(e)}")
        raise
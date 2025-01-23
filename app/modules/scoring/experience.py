from openai import OpenAI
from dotenv import load_dotenv
import os
from app.models.resume import ProfessionalExperienceItem
from app.models.scoring_rules import SCORING_RULES
from app.utils.json_lookup import get_company_score
from typing import List

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def infer_company_size(company: str) -> int:
    """
    Use LLM to infer company size if not found in the JSON file.
    """
    client = OpenAI(api_key=openai_api_key)
    
    prompt = f"""
    Based on the following company name, provide a size score between 0 and 25, where 25 is the highest.
    Company: {company}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a company size evaluator. Provide a score between 0 and 25."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=10,
        temperature=0.3
    )
    
    try:
        score = int(response.choices[0].message.content.strip())
        return min(max(score, 0), 25)  # Ensure score is between 0 and 25
    except:
        return 10  # Default score if parsing fails

def calculate_experience_score(experience: List[ProfessionalExperienceItem]) -> float:
    """
    Calculate the experience score with LLM fallback for unknown companies.
    """
    total_score = 0.0

    for exp in experience:
        # Get company score from JSON or LLM fallback
        company_score = get_company_score(exp.company)
        if company_score == 10:  # Default score for unknown companies
            company_score = infer_company_size(exp.company)
        
        # Rest of the scoring logic
        company_score = company_score * SCORING_RULES["professional_experience"]["company"]
        position_score = 25 if is_technical_position(exp.position) else 0
        description_score = calculate_description_score(exp.description)
        seniority_score = 5 if exp.seniority.lower() in ["senior", "lead", "manager"] else 0
        duration_score = 5 if calculate_duration(exp.duration) >= 6 else 0
        
        total_score += company_score + position_score + description_score + seniority_score + duration_score

    return total_score

def is_technical_position(position: str) -> bool:
    """
    Check if the position is relevant to technical roles.
    """
    technical_keywords = ["software", "frontend", "backend", "web", "mobile", "full stack", "data", "machine learning", "ai", "devops"]
    return any(keyword in position.lower() for keyword in technical_keywords)

def calculate_description_score(description: str) -> int:
    """
    Calculate the score based on the description's clarity, impact, and use of tools.
    """
    score = 0

    # Clarity and Focus (30%)
    if "developed" in description.lower() or "designed" in description.lower():
        score += 10

    # Achievements/Impact (30%)
    if "reduced" in description.lower() or "improved" in description.lower():
        score += 10

    # Use of Tools/Technologies (20%)
    if "python" in description.lower() or "sql" in description.lower():
        score += 10

    return score

def calculate_duration(duration: str) -> int:
    """
    Calculate the duration in months.
    """
    try:
        if " - " in duration:
            # Format: "Jan 2020 - Dec 2021"
            start, end = duration.split(" - ")
            start_year = int(start.split()[-1])
            end_year = int(end.split()[-1])
            return (end_year - start_year) * 12
        elif "year" in duration:
            # Format: "2 years"
            years = int(duration.split()[0])
            return years * 12
        elif "month" in duration:
            # Format: "6 months"
            months = int(duration.split()[0])
            return months
        else:
            # Default to 0 if the format is unrecognized
            return 0
    except:
        # If parsing fails, return 0
        return 0
from openai import OpenAI
from dotenv import load_dotenv
import os
from app.models.resume import ProfessionalExperienceItem
from app.models.scoring_rules import SCORING_RULES
from app.utils.json_lookup import get_company_score
from typing import List
import re
from datetime import datetime
from app.utils.openai_client import openai_client

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def infer_company_size(company: str) -> int:
    """
    Use LLM to infer company size if not found in the JSON file.
    """
    client = openai_client.get_client()
    
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

def parse_experience_duration(duration: str) -> float:
    """
    Parse a duration string (e.g., "2018-01 to 2020-12" or "2018 to 2020")
    and return the approximate number of months of experience.
    """
    dates = re.findall(r"(\d{4}(?:-\d{2})?)", duration)
    if len(dates) >= 2:
        try:
            try:
                start = datetime.strptime(dates[0], "%Y-%m")
            except:
                start = datetime.strptime(dates[0], "%Y")
            try:
                end = datetime.strptime(dates[1], "%Y-%m")
            except:
                end = datetime.strptime(dates[1], "%Y")
            diff = (end.year - start.year) * 12 + (end.month - (start.month if hasattr(start, 'month') else 1))
            return max(diff, 0)
        except Exception:
            return 12  # default if parsing fails
    return 12  # default duration (12 months) if no dates can be parsed

def calculate_experience_score(experiences: List[ProfessionalExperienceItem]) -> float:
    """
    Calculate Experience Score.
    Sum the months of experience for each entry.
    60 months (5 years) of total experience yields full 30 points.
    """
    total_months = 0
    for exp in experiences:
        if exp.duration:
            total_months += parse_experience_duration(exp.duration)
        else:
            total_months += 12  # default 1 year if no duration provided
    score = (total_months / 60) * 30  # 60 months => 30 points
    return min(score, 30)

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
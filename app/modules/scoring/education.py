from openai import OpenAI
from dotenv import load_dotenv
import os
from app.models.resume import EducationItem
from app.models.scoring_rules import SCORING_RULES
from app.utils.json_lookup import get_university_score
from typing import List
from app.utils.openai_client import openai_client

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def infer_university_reputation(university: str) -> int:
    """
    Use LLM to infer university reputation if not found in the JSON file.
    """
    client = openai_client.get_client()
    
    prompt = f"""
    Based on the following university name, provide a reputation score between 0 and 20, where 20 is the highest reputation.
    University: {university}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a university reputation evaluator. Provide a score between 0 and 20."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=10,
        temperature=0.3
    )
    
    try:
        score = int(response.choices[0].message.content.strip())
        return min(max(score, 0), 20)  # Ensure score is between 0 and 20
    except:
        return 10  # Default score if parsing fails

def calculate_education_score(education_items: List[EducationItem]) -> float:
    """
    Calculate Education Score.
    Use the best (maximum) GPA among education items.
    GPA (on a 4.0 scale) is scaled to 30 points.
    """
    scores = []
    for edu in education_items:
        if edu.gpa is not None:
            try:
                scores.append((float(edu.gpa) / 4.0) * 30)
            except Exception:
                continue
    if scores:
        # Use the highest education score
        return min(max(scores), 30)
    return 0.0

def is_technical_major(major: str) -> bool:
    """
    Check if the major is relevant to technical fields.
    """
    technical_keywords = ["computer", "software", "data", "information", "cyber", "cloud", "web", "ai", "machine learning", "analytics"]
    return any(keyword in major.lower() for keyword in technical_keywords)

def calculate_class_score(class_year: str) -> int:
    """
    Calculate the score based on the class year.
    """
    if class_year.lower() == "senior":
        return 30
    elif class_year.lower() == "junior":
        return 20
    elif class_year.lower() == "sophomore":
        return 10
    else:
        return 10
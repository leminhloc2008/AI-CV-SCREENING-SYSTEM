from openai import OpenAI
from dotenv import load_dotenv
import os
from app.models.resume import AwardItem
from app.models.scoring_rules import SCORING_RULES
from typing import List, Optional
from app.utils.openai_client import openai_client

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def infer_contest_prestige(contest: str) -> int:
    """
    Use LLM to infer contest prestige if not found in the JSON file.
    """
    client = openai_client.get_client()
    
    prompt = f"""
    Based on the following contest name, provide a prestige score between 0 and 30, where 30 is the highest.
    Contest: {contest}
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a contest prestige evaluator. Provide a score between 0 and 30."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=10,
        temperature=0.3
    )
    
    try:
        score = int(response.choices[0].message.content.strip())
        return min(max(score, 0), 30)  # Ensure score is between 0 and 30
    except:
        return 10  # Default score if parsing fails

def calculate_awards_score(awards: List[AwardItem]) -> float:
    """
    Calculate Awards Score.
    Each award is worth 2 points, with a maximum of 10 points.
    """
    score = len(awards) * 2
    return min(score, 10)

def calculate_prize_score(prize: str) -> int:
    """
    Calculate the score based on the prize level.
    """
    if "1st" in prize.lower() or "gold" in prize.lower():
        return 25
    elif "2nd" in prize.lower() or "silver" in prize.lower():
        return 20
    elif "3rd" in prize.lower() or "bronze" in prize.lower():
        return 15
    else:
        return 10

def calculate_description_score(description: str) -> int:
    """
    Calculate the score based on the description's clarity and impact.
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

def is_technical_role(role: Optional[str]) -> bool:
    """
    Check if the role is relevant to technical fields.
    """
    if not role:
        return False
    technical_keywords = ["developer", "engineer", "data scientist", "analyst"]
    return any(keyword in role.lower() for keyword in technical_keywords)
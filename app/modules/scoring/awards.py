from openai import OpenAI
from dotenv import load_dotenv
import os
from app.models.resume import AwardItem
from app.models.scoring_rules import SCORING_RULES
from typing import List, Optional

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def infer_contest_prestige(contest: str) -> int:
    """
    Use LLM to infer contest prestige if not found in the JSON file.
    """
    client = OpenAI(api_key=openai_api_key)
    
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
    Calculate the awards score with LLM fallback for unknown contests.
    """
    total_score = 0.0

    for award in awards:
        # Contest Prestige (30%)
        contest_score = infer_contest_prestige(award.contest) * SCORING_RULES["awards"]["contest"]
        
        # Prize (25%)
        prize_score = calculate_prize_score(award.prize) * SCORING_RULES["awards"]["prize"]
        
        # Description (25%)
        description_score = calculate_description_score(award.description) * SCORING_RULES["awards"]["description"]
        
        # Role (10%)
        role_score = 10 if is_technical_role(award.role) else 0
        
        # Link (5%)
        link_score = 5 if award.link else 0
        
        # Time (5%)
        time_score = 5 if award.time else 0
        
        # Total Award Score
        total_score += contest_score + prize_score + description_score + role_score + link_score + time_score

    return total_score

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
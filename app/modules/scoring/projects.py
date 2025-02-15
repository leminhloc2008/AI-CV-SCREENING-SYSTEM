from openai import OpenAI
from dotenv import load_dotenv
import os
from app.models.resume import ProjectItem
from app.models.scoring_rules import SCORING_RULES
from typing import List, Optional
from app.utils.openai_client import openai_client

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def infer_tech_stack_relevance(tech: str) -> int:
    """
    Use LLM to infer tech stack relevance if not found in the JSON file.
    """
    client = openai_client.get_client()
    
    prompt = f"""
    Based on the following tech stack, provide a relevance score between 0 and 25, where 25 is the highest.
    Tech Stack: {tech}
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a tech stack relevance evaluator. Provide a score between 0 and 25."},
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

def calculate_projects_score(projects: List[ProjectItem]) -> float:
    """
    Calculate Projects Score.
    Each project is worth 5 points, capped at 20 points.
    """
    score = len(projects) * 5
    return min(score, 20)

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
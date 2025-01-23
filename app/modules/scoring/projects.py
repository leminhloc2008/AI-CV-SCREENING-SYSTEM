from openai import OpenAI
from dotenv import load_dotenv
import os
from app.models.resume import ProjectItem
from app.models.scoring_rules import SCORING_RULES
from typing import List, Optional

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def infer_tech_stack_relevance(tech: str) -> int:
    """
    Use LLM to infer tech stack relevance if not found in the JSON file.
    """
    client = OpenAI(api_key=openai_api_key)
    
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
    Calculate the projects score with LLM fallback for unknown tech stacks.
    """
    total_score = 0.0

    for project in projects:
        # Tech Stack (25%)
        tech_score = infer_tech_stack_relevance(project.tech) * SCORING_RULES["projects"]["tech"]
        
        # GitHub Link (20%)
        link_score = 20 if project.link else 0
        
        # Description (40%)
        description_score = calculate_description_score(project.description) * SCORING_RULES["projects"]["description"]
        
        # Total Project Score
        total_score += tech_score + link_score + description_score

    return total_score

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
from openai import OpenAI
from dotenv import load_dotenv
import os
from app.models.resume import CertificationItem
from app.models.scoring_rules import SCORING_RULES
from typing import List, Optional
from app.utils.openai_client import openai_client

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def infer_certification_relevance(name: str) -> int:
    """
    Use LLM to infer certification relevance if not found in the JSON file.
    """
    client = openai_client.get_client()
    
    prompt = f"""
    Based on the following certification name, provide a relevance score between 0 and 50, where 50 is the highest.
    Certification: {name}
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a certification relevance evaluator. Provide a score between 0 and 50."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=10,
        temperature=0.3
    )
    
    try:
        score = int(response.choices[0].message.content.strip())
        return min(max(score, 0), 50)  # Ensure score is between 0 and 50
    except:
        return 10  # Default score if parsing fails

def calculate_certifications_score(certifications: List[CertificationItem]) -> float:
    """
    Calculate Certifications Score.
    Each certification is worth 1 point, with a maximum of 10 points.
    """
    score = len(certifications)
    return min(score, 10)

def calculate_name_score(name: str) -> int:
    """
    Calculate the score based on the certification name's relevance.
    """
    if "aws" in name.lower() or "google" in name.lower() or "microsoft" in name.lower():
        return 50
    elif "data" in name.lower() or "cloud" in name.lower() or "ai" in name.lower():
        return 30
    else:
        return 10

def calculate_org_score(org: Optional[str]) -> int:
    """
    Calculate the score based on the organization's reputation.
    """
    if not org:
        return 0
    if "aws" in org.lower() or "google" in org.lower() or "microsoft" in org.lower():
        return 40
    elif "udemy" in org.lower() or "coursera" in org.lower():
        return 25
    else:
        return 10
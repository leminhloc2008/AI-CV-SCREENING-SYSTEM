from openai import OpenAI
from dotenv import load_dotenv
import os
from app.models.resume import CertificationItem
from app.models.scoring_rules import SCORING_RULES
from typing import List, Optional

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def infer_certification_relevance(name: str) -> int:
    """
    Use LLM to infer certification relevance if not found in the JSON file.
    """
    client = OpenAI(api_key=openai_api_key)
    
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
    Calculate the certifications score with LLM fallback for unknown certifications.
    """
    total_score = 0.0

    for cert in certifications:
        # Get name score from JSON or LLM fallback
        name_score = calculate_name_score(cert.name)
        if name_score == 10:  # Default score for unknown certifications
            name_score = infer_certification_relevance(cert.name)
        
        name_score = name_score * SCORING_RULES["certifications"]["name"]
        org_score = calculate_org_score(cert.org) * SCORING_RULES["certifications"]["org"]
        link_score = 10 if cert.link else 0
        
        total_score += name_score + org_score + link_score

    return total_score

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
from openai import OpenAI
from dotenv import load_dotenv
import os, json, openai, re

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_structured_data_from_cv(cv_text: str) -> dict:
    """
    Extract structured data from CV text using OpenAI's API.
    Returns a dictionary containing structured resume data.
    """
    client = OpenAI()
    
    prompt = f"""
    Extract the following fields from the CV below and return the result as a valid JSON object. Do not include any additional text or explanations. Only return the JSON object.

    Required JSON structure:
    {{
        "name": "string",
        "location": "string",
        "social": ["string"],
        "email": "string",
        "linkedin": "string or null",
        "phone": "string",
        "intro": "string",
        "education": [{{
            "school": "string",
            "class_year": "string",
            "major": "string",
            "gpa": "string"
        }}],
        "professional_experience": [{{
            "company": "string",
            "location": "string",
            "position": "string",
            "seniority": "string",
            "duration": "string",
            "description": "string"
        }}],
        "projects": [{{
            "name": "string",
            "tech": "string",
            "duration": "string",
            "description": "string"
        }}],
        "awards": [{{
            "contest": "string",
            "prize": "string",
            "description": "string",
            "time": "string"
        }}],
        "certifications": [{{
            "name": "string",
            "org": "string",
            "link": "string"
        }}],
        "skills": [{{
            "name": "string",
            "list": ["string"]
        }}]
    }}

    CV Text:
    {cv_text}"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a professional CV parser. Return only valid JSON that matches the required structure exactly."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.3
        )
        
        response_content = response.choices[0].message.content.strip()
        if not response_content:
            print("Empty response from API")
            return create_default_structure()
            
        try:
            structured_data = json.loads(response_content)
            if not isinstance(structured_data, dict):
                print("Response is not a dictionary")
                return create_default_structure()
                
            if "skills" in structured_data:
                for skill in structured_data["skills"]:
                    if "skills" in skill and "list" not in skill:
                        skill["list"] = skill.pop("skills")
                    elif "list" not in skill:
                        skill["list"] = []
                        
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            print(f"Raw response: {response_content}")
            return create_default_structure()
            
    except Exception as e:
        print(f"Error during API call: {e}")
        return create_default_structure()
    
    # Ensure all required fields exist
    default_structure = create_default_structure()
    for key in default_structure:
        if key not in structured_data:
            structured_data[key] = default_structure[key]
    
    return structured_data

def create_default_structure() -> dict:
    """
    Creates a default structure for the resume data.
    """
    return {
        "name": "Unknown",
        "location": "Unknown",
        "social": [],
        "email": "Unknown",
        "linkedin": None,
        "phone": "Unknown",
        "intro": "No introduction provided.",
        "education": [],
        "professional_experience": [],
        "projects": [],
        "awards": [],
        "certifications": [],
        "skills": [{"name": "Unknown", "list": []}]
    }
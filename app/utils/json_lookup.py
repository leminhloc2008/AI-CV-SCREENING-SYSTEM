import json
from pathlib import Path

def load_json_data(file_name: str) -> dict:
    """
    Load JSON data from the data folder.
    """
    file_path = Path(__file__).parent.parent / "data" / file_name
    with open(file_path, "r") as file:
        return json.load(file)

def get_university_score(university: str) -> int:
    """
    Get the score for a university based on its reputation.
    """
    universities = load_json_data("universities.json")
    return universities.get(university, 10)

def get_company_score(company: str) -> int:
    """
    Get the score for a company based on its size.
    """
    companies = load_json_data("companies.json")
    return companies.get(company, 10)
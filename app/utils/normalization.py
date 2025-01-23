import unicodedata
from typing import Dict

# Dictionary for Vietnamese university synonyms
UNIVERSITY_SYNONYMS: Dict[str, str] = {
    "Đại học Bách Khoa Hà Nội": "HUST",
    "Đại học Bách Khoa": "HUST",
    "Bách Khoa Hà Nội": "HUST",
    "HUST": "HUST",
    "RMIT University Vietnam": "RMIT",
    "RMIT": "RMIT",
    "VinUniversity": "VinUni",
    "VinUni": "VinUni",
}

def normalize_text(text: str) -> str:
    """
    Normalize text by removing diacritics and converting to lowercase.
    """
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return text.lower()

def normalize_university_name(university: str) -> str:
    """
    Normalize university names using a synonym dictionary.
    """
    # Remove diacritics and convert to lowercase
    normalized_name = normalize_text(university)
    
    # Check if the normalized name matches any synonym
    for key, value in UNIVERSITY_SYNONYMS.items():
        if normalize_text(key) == normalized_name:
            return value
    
    # If no match, return the original normalized name
    return normalized_name
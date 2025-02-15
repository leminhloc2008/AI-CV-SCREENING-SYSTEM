import re
from typing import Optional, Dict, List
from statistics import mean

def normalize_gpa(gpa_value: str) -> Optional[float]:
    """
    Normalize GPA from various formats to a float value between 0-10 or None if invalid.
    """
    if not gpa_value or not isinstance(gpa_value, str):
        return None
        
    # Clean the input string
    gpa_value = gpa_value.strip().lower()
    
    # Case 1: Already a simple number (e.g., "3.5" or "8.7")
    try:
        gpa = float(gpa_value)
        return gpa
    except ValueError:
        pass
    
    # Case 2: Grade format with multiple years (e.g., "Grade 9: 9.9, Grade 10: 9.7, Grade 11: 9.8")
    grade_pattern = r'grade ?\d+:?\s*(\d+\.?\d*)'
    grades = re.findall(grade_pattern, gpa_value)
    if grades:
        try:
            grades = [float(grade) for grade in grades]
            return round(mean(grades), 2)
        except (ValueError, TypeError):
            pass
            
    # Case 3: Simple comma/semicolon separated grades
    try:
        # Split by comma or semicolon and clean
        grades = [g.strip() for g in re.split(r'[,;]', gpa_value)]
        # Convert to float and filter out non-numeric values
        grades = [float(g) for g in grades if re.match(r'^\d+\.?\d*$', g.strip())]
        if grades:
            return round(mean(grades), 2)
    except (ValueError, TypeError):
        pass
        
    # Case 4: Extract the first number found in the string
    number_match = re.search(r'(\d+\.?\d*)', gpa_value)
    if number_match:
        try:
            return float(number_match.group(1))
        except (ValueError, TypeError):
            pass
            
    return None

def convert_to_standard_gpa(gpa: float, scale: str = "10") -> Optional[float]:
    """
    Convert GPA to a standard 4.0 scale if needed.
    Currently supports conversion from 10-point scale.
    """
    if gpa is None:
        return None
        
    if scale == "10":
        # Convert 10-point scale to 4.0 scale
        return round((gpa * 4) / 10, 2)
    
    return gpa

def extract_and_normalize_gpa(education_data: Dict) -> Dict:
    """
    Process education data to normalize GPA values.
    """
    if "gpa" in education_data:
        raw_gpa = education_data["gpa"]
        normalized_gpa = normalize_gpa(str(raw_gpa))
        
        # Only update if we successfully normalized the GPA
        if normalized_gpa is not None:
            education_data["gpa"] = normalized_gpa
        else:
            education_data["gpa"] = None
            
    return education_data

def process_education_items(education_items: List[Dict]) -> List[Dict]:
    """
    Process a list of education items to normalize their GPA values.
    """
    return [extract_and_normalize_gpa(item) for item in education_items]
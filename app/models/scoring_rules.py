SCORING_RULES = {
    "education": {
        "weight": 15,  # 15% of the total score
        "school": 30,
        "class_year": 30,
        "major": 30,
        "minor": 0,
        "gpa": 10
    },
    "professional_experience": {
        "weight": 25,  # 25% of the total score
        "company": 25,
        "location": 5,
        "position": 25,
        "seniority": 5,
        "duration": 5,
        "description": 25
    },
    "projects": {
        "weight": 20,  # 20% of the total score
        "name": 10,
        "link": 20,
        "tech": 25,
        "duration": 5,
        "description": 40
    },
    "awards": {
        "weight": 15,  # 15% of the total score
        "contest": 30,
        "prize": 25,
        "description": 25,
        "role": 10,
        "link": 5,
        "time": 5
    },
    "certifications": {
        "weight": 5,  # 5% of the total score
        "name": 50,
        "link": 10,
        "org": 40
    },
    "skills": {
        "weight": 5,  # 5% of the total score
        "name": 50,
        "list": 50
    }
}
from app.models.resume import EducationItem
from app.modules.scoring.education import calculate_education_score

def test_calculate_education_score():
    education = [
        EducationItem(school="HUST", class_year="Senior", major="Computer Science", gpa=3.5)
    ]
    score = calculate_education_score(education)

    # Output the education score
    print("=== Education Score ===")
    print(f"Score: {score}")

test_calculate_education_score()
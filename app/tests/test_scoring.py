from app.models.resume import Resume, EducationItem, ProfessionalExperienceItem, ProjectItem
from app.modules.scoring.scorer import calculate_total_score

def test_calculate_total_score():
    resume = Resume(
        name="John Doe",
        location="Hanoi",
        social=[],
        email="johndoe@example.com",
        phone="1234567890",
        intro="A passionate software engineer...",
        education=[
            EducationItem(school="HUST", class_year="Senior", major="Computer Science", gpa=3.5)
        ],
        professional_experience=[
            ProfessionalExperienceItem(
                company="FPT Software",
                location="Hanoi",
                position="Software Engineer",
                seniority="Junior",
                duration="Jan 2020 - Dec 2021",  # Valid duration format
                description="Developed web applications using Python and Django."
            )
        ],
        projects=[
            ProjectItem(
                name="E-commerce Website",
                tech="Python, Django, React",
                description="Developed a full-stack e-commerce website."
            )
        ],
        awards=[],
        certifications=[],
        skills=[]
    )
    score = calculate_total_score(resume)

    # Output the total score
    print("=== Total Resume Score ===")
    print(f"Score: {score}")

test_calculate_total_score()
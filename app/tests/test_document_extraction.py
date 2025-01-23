from app.modules.document_extraction.extractor import extract_resume
from app.models.resume import Resume

def test_document_extraction():
    cv_file = "D:\Downloads\LeMinhLocCV.pdf"  

    resume = extract_resume(cv_file)

    # Test that the returned value is a dictionary
    assert isinstance(resume, Resume)
    
    # Test that required fields exist and have expected types
    assert isinstance(resume.name, str)
    assert isinstance(resume.email, str)
    assert isinstance(resume.phone, str)
    assert isinstance(resume.education, list)
    assert isinstance(resume.professional_experience, list)
    assert isinstance(resume.skills, list)
    
    # Test that required fields are not empty or default values
    assert resume.name != ""
    assert resume.email != ""
    assert resume.phone != ""

    # Print the extracted resume data
    print("=== Extracted Resume ===")
    print(f"Name: {resume.name}")
    print(f"Location: {resume.location}")
    print(f"Email: {resume.email}")
    print(f"LinkedIn: {resume.linkedin}")
    print(f"Phone: {resume.phone}")
    print(f"Intro: {resume.intro}")
    print("\nEducation:")
    for edu in resume.education:
        print(f"- {edu.school}, {edu.major}, {edu.class_year}, GPA: {edu.gpa}")
    print("\nProfessional Experience:")
    for exp in resume.professional_experience:
        print(f"- {exp.company}, {exp.position}, {exp.duration}")
        print(f"  {exp.description}")
    print("\nProjects:")
    for project in resume.projects:
        print(f"- {project.name}, {project.tech}, {project.duration}")
        print(f"  {project.description}")
    print("\nAwards:")
    for award in resume.awards:
        print(f"- {award.contest}, {award.prize}, {award.time}")
        print(f"  {award.description}")
    print("\nCertifications:")
    for cert in resume.certifications:
        print(f"- {cert.name}, {cert.org}")
    print("\nSkills:")
    for skill in resume.skills:
        print(f"- {skill.name}: {', '.join(skill.list)}")

test_document_extraction()
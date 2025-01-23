from openai import OpenAI
from dotenv import load_dotenv
import os
from app.models.resume import Resume

load_dotenv()

def evaluate_resume(resume: Resume) -> str:
    """
    Evaluate a resume using OpenAI's API.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = f"Please evaluate the following resume:\n{resume}"
    
    response = client.chat.completions.create(
        model="gpt-4o",  
        messages=[
            {"role": "system", "content": "You are a professional resume evaluator. Provide a detailed evaluation of the resume."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.7
    )
    
    evaluation = response.choices[0].message.content
    
    return evaluation

def format_resume_for_evaluation(resume: Resume) -> str:
    """
    Format the resume into a text string for evaluation.
    """
    evaluation = f"Name: {resume.name}\n"
    evaluation += f"Location: {resume.location}\n"
    evaluation += f"Email: {resume.email}\n"
    evaluation += f"LinkedIn: {resume.linkedin}\n"
    evaluation += f"Phone: {resume.phone}\n"
    evaluation += f"Intro: {resume.intro}\n"

    evaluation += "\nEducation:\n"
    for edu in resume.education:
        evaluation += f"- {edu.school}, {edu.major}, {edu.class_year}, GPA: {edu.gpa}\n"

    evaluation += "\nProfessional Experience:\n"
    for exp in resume.professional_experience:
        evaluation += f"- {exp.company}, {exp.position}, {exp.duration}\n"
        evaluation += f"  {exp.description}\n"

    evaluation += "\nProjects:\n"
    for project in resume.projects:
        evaluation += f"- {project.name}, {project.tech}, {project.duration}\n"
        evaluation += f"  {project.description}\n"

    evaluation += "\nAwards:\n"
    for award in resume.awards:
        evaluation += f"- {award.contest}, {award.prize}, {award.time}\n"
        evaluation += f"  {award.description}\n"

    evaluation += "\nCertifications:\n"
    for cert in resume.certifications:
        evaluation += f"- {cert.name}, {cert.org}\n"

    evaluation += "\nSkills:\n"
    for skill in resume.skills:
        evaluation += f"- {skill.name}: {', '.join(skill.list)}\n"

    return evaluation
from app.utils.openai_client import openai_client
from dotenv import load_dotenv
import os
from app.models.resume import Resume

load_dotenv()

def evaluate_resume(resume: Resume, status: str) -> str:
    """
    Evaluate a resume using OpenAI's API and provide reasoning for the status.
    """
    client = openai_client.get_client()
    
    prompt = f"""Please provide detailed reasoning for why this resume received a {status} status:
    {resume}
    
    Provide specific reasons based on:
    - Education quality and relevance
    - Professional experience depth and relevance
    - Project quality and impact
    - Skills alignment with requirements
    - Any other relevant factors
    
    Be concise but specific, focusing on key decision factors.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",  
        messages=[
            {"role": "system", "content": "You are a professional resume evaluator. Provide specific reasoning for the evaluation status."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0
    )
    
    return response.choices[0].message.content

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
from app.utils.openai_client import openai_client
from dotenv import load_dotenv
import os
from app.models.resume import Resume

load_dotenv()

def summarize_resume(resume: Resume) -> str:
    """
    Summarize a resume using OpenAI's API.
    """
    client = openai_client.get_client()
    
    prompt = f"Please summarize the following resume:\n{resume}"
    
    response = client.chat.completions.create(
        model="gpt-4o",  
        messages=[
            {"role": "system", "content": "You are a professional resume reviewer. Summarize the key points of the resume concisely."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7
    )
    
    return response.choices[0].message.content

def format_resume_for_summary(resume: Resume) -> str:
    """
    Format the resume into a text string for summarization.
    """
    summary = f"Name: {resume.name}\n"
    summary += f"Location: {resume.location}\n"
    summary += f"Email: {resume.email}\n"
    summary += f"LinkedIn: {resume.linkedin}\n"
    summary += f"Phone: {resume.phone}\n"
    summary += f"Intro: {resume.intro}\n"

    summary += "\nEducation:\n"
    for edu in resume.education:
        summary += f"- {edu.school}, {edu.major}, {edu.class_year}, GPA: {edu.gpa}\n"

    summary += "\nProfessional Experience:\n"
    for exp in resume.professional_experience:
        summary += f"- {exp.company}, {exp.position}, {exp.duration}\n"
        summary += f"  {exp.description}\n"

    summary += "\nProjects:\n"
    for project in resume.projects:
        summary += f"- {project.name}, {project.tech}, {project.duration}\n"
        summary += f"  {project.description}\n"

    summary += "\nAwards:\n"
    for award in resume.awards:
        summary += f"- {award.contest}, {award.prize}, {award.time}\n"
        summary += f"  {award.description}\n"

    summary += "\nCertifications:\n"
    for cert in resume.certifications:
        summary += f"- {cert.name}, {cert.org}\n"

    summary += "\nSkills:\n"
    for skill in resume.skills:
        summary += f"- {skill.name}: {', '.join(skill.list)}\n"

    return summary
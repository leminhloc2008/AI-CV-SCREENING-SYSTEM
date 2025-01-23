from pydantic import BaseModel, Field
from typing import List, Optional

class EducationItem(BaseModel):
    school: str
    class_year: str
    major: str
    minor: Optional[str] = None
    gpa: Optional[float] = None

class ProfessionalExperienceItem(BaseModel):
    company: str
    location: str
    position: str
    seniority: str
    duration: str
    description: str

class ProjectItem(BaseModel):
    name: str
    link: Optional[str] = None
    tech: Optional[str] = None
    duration: Optional[str] = None
    description: str

class AwardItem(BaseModel):
    contest: str
    prize: str
    description: str
    role: Optional[str] = None
    link: Optional[str] = None
    time: str

class CertificationItem(BaseModel):
    name: str
    link: Optional[str] = None
    org: Optional[str] = None

class SkillItem(BaseModel):
    name: str
    list: List[str]

class Resume(BaseModel):
    name: str
    location: str
    social: List[str]
    email: str
    linkedin: Optional[str] = None
    phone: str
    intro: str
    education: List[EducationItem]
    professional_experience: List[ProfessionalExperienceItem]
    projects: List[ProjectItem]
    awards: List[AwardItem]
    certifications: List[CertificationItem]
    skills: List[SkillItem]
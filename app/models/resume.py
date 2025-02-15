from pydantic import BaseModel, Field
from typing import List, Optional

class EducationItem(BaseModel):
    school: str = "Unknown"
    class_year: str = "Unknown"
    major: str = ""
    minor: Optional[str] = None
    gpa: Optional[float] = None

class ProfessionalExperienceItem(BaseModel):
    company: str = "Unknown"
    location: str = ""
    position: str = "Unknown"
    seniority: str = ""
    duration: str = "Unknown"
    description: str = ""

class ProjectItem(BaseModel):
    name: str = "Unknown"
    link: Optional[str] = None
    tech: Optional[str] = None
    duration: Optional[str] = None
    description: str = ""

class AwardItem(BaseModel):
    contest: str
    prize: str
    description: str = ""  # Added default
    role: Optional[str] = None
    link: Optional[str] = None
    time: str = ""  # Added default

class CertificationItem(BaseModel):
    name: str
    link: Optional[str] = None
    org: Optional[str] = None

class SkillItem(BaseModel):
    name: str
    list: List[str] = []  # Added default

class Resume(BaseModel):
    name: str = "Unknown"  # Added default
    location: str = "Unknown"  # Added default
    social: List[str] = []  # Added default
    email: str = "Unknown"  # Added default
    linkedin: Optional[str] = None
    phone: str = "Unknown"  # Added default
    intro: str = ""  # Added default
    education: List[EducationItem] = []  # Added default
    professional_experience: List[ProfessionalExperienceItem] = []  # Added default
    projects: List[ProjectItem] = []  # Added default
    awards: List[AwardItem] = []  # Added default
    certifications: List[CertificationItem] = []  # Added default
    skills: List[SkillItem] = []  # Added default

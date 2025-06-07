from enum import Enum
from pydantic import BaseModel, Field, validator
from uuid import UUID, uuid4
from typing import List, Dict
import json

class SectionType(str, Enum):
    REQUIREMENTS = "REQUIREMENTS"
    QUALIFICATIONS = "QUALIFICATIONS"
    RESPONSIBILITIES = "RESPONSIBILITIES"
    EDUCATION = "EDUCATION"  
    EXPERIENCE = "EXPERIENCE"
    SKILLS = "SKILLS"
    PROJECTS = "PROJECTS"
    CERTIFICATIONS = "CERTIFICATIONS"
    INTERNSHIPS = "INTERNSHIPS"
    ACHIEVEMENTS = "ACHIEVEMENTS"
    SUMMARY = "SUMMARY"
    CONTACT = "CONTACT"

class Section(BaseModel):
    title: SectionType
    content: List[str] = Field(..., min_items=1)  # Ensures non-empty string list
    
    @validator('content', pre=True)
    def validate_content(cls, v):
        if not v:
            raise ValueError("Content cannot be empty")
        return [str(item).strip() for item in v if str(item).strip()]

class ParsedResume(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))  # Auto-generate UUID
    category: str
    sections: List[Section]

class ParsedJD(BaseModel):
    jd_id: str
    company: str
    category: str
    sections: List[Section]

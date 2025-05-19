import json
from uuid import uuid4  # Added UUID import
from openai import OpenAI
from ..models import ParsedResume, Section, SectionType

client = OpenAI()

def parse_resume(resume_text: str) -> ParsedResume:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "system",
            "content": "Extract resume sections into JSON format with keys: Education, Experience, Skills, Projects, Certifications, Internships, Achievements, Summary, Contact"
        }, {
            "role": "user",
            "content": resume_text
        }]
    )
    
    raw_data = json.loads(response.choices[0].message.content)
    sections = []
    for key, value in raw_data.items():
        if isinstance(value, str):
            value = [value]
        sections.append(Section(title=SectionType(key.upper()), content=value))
    
    return ParsedResume(
        id=str(uuid4()),  # Automatically generate UUID instead of hardcoded "res_123"
        category="default",
        sections=sections
    )

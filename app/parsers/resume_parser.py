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
            "content": """Extract resume sections into JSON. For each section:
                        - Always return a list of strings
                        - Skip empty sections
                        - Example: {"Skills": ["Python", "SQL"]}"""
        }, {
            "role": "user",
            "content": resume_text
        }]
    )
    
    raw_data = json.loads(response.choices[0].message.content)
    sections = []

    # Ensure string content for sections and filter out empty ones
    for key, value in raw_data.items():
        content = []
        
        if isinstance(value, list):
            content = [str(item).strip() for item in value if str(item).strip()]
        elif isinstance(value, dict):
            content = [f"{k}: {v}".strip() for k, v in value.items() if str(v).strip()]
        else:
            content = [str(value).strip()] if str(value).strip() else []

        # Only add non-empty sections
        if content:
            try:
                sections.append(Section(
                    title=SectionType(key.upper()),
                    content=content
                ))
            except ValueError:  # Handle invalid section type
                sections.append(Section(
                    title=SectionType.REQUIREMENTS,  # Default fallback
                    content=content
                ))

    if not sections:
        raise ValueError("No parsable content found in resume")

    return ParsedResume(
        id=str(uuid4()),  # Generate unique UUID
        category="default",
        sections=sections
    )

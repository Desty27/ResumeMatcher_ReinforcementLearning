import json
from openai import OpenAI
from ..models import ParsedJD, Section, SectionType

client = OpenAI()

def parse_jd(jd_text: str) -> ParsedJD:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "system",
            "content": "Extract job description sections into JSON format with these EXACT keys: REQUIREMENTS, QUALIFICATIONS, RESPONSIBILITIES, EDUCATION, SKILLS"
        }, {
            "role": "user",
            "content": jd_text
        }]
    )
    
    raw_data = json.loads(response.choices[0].message.content)

    # Add validation
    valid_sections = {st.value for st in SectionType}
    sections = []

    for key, value in raw_data.items():
        section_key = key.upper()

        # Ensure valid section key; fallback to "REQUIREMENTS" if necessary
        if section_key not in valid_sections:
            section_key = "REQUIREMENTS"
        
        sections.append(Section(
            title=SectionType(section_key),
            content=value if isinstance(value, list) else [value]
        ))
    
    return ParsedJD(
        jd_id=str(hash(jd_text)),  # Generate a unique ID from the text hash
        company="Unknown",  # Default placeholder, can be extracted separately
        category="default",
        sections=sections
    )

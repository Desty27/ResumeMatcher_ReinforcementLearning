import json
from openai import OpenAI
from typing import List, Dict, Union
from ..models import ParsedJD, Section, SectionType

client = OpenAI()

def parse_jd(jd_text: str) -> ParsedJD:
    """Parse job description text into structured format with empty section handling"""
    try:
        # Step 1: Get structured data from LLM
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": """Extract job description sections into JSON with these keys:
                            - REQUIREMENTS (list)
                            - QUALIFICATIONS (list) 
                            - RESPONSIBILITIES (list)
                            - EDUCATION (list)
                            - SKILLS (list)
                            Return empty lists for missing sections."""
            }, {
                "role": "user",
                "content": jd_text
            }]
        )
        
        # Step 2: Process raw data with validation
        raw_data = json.loads(response.choices[0].message.content)
        sections = []
        valid_sections = {st.value for st in SectionType}
        
        for key, value in raw_data.items():
            # Normalize section key
            section_key = key.upper().strip()
            if section_key not in valid_sections:
                section_key = "REQUIREMENTS"  # Default section type
            
            # Process content
            content = []
            if isinstance(value, list):
                content = [str(item).strip() for item in value if str(item).strip()]
            elif isinstance(value, dict):
                content = [f"{k}: {v}".strip() for k, v in value.items() if str(v).strip()]
            elif value:
                content = [str(value).strip()]
            
            # Only add non-empty sections
            if content:
                sections.append(Section(
                    title=SectionType(section_key),
                    content=content
                ))
        
        # Step 3: Validate we have at least one section
        if not sections:
            sections.append(Section(
                title=SectionType.REQUIREMENTS,
                content=["No parsable content found in job description"]
            ))
        
        return ParsedJD(
            jd_id=str(hash(jd_text)),
            company="Unknown",
            category="default",
            sections=sections
        )
        
    except json.JSONDecodeError:
        # Fallback when LLM returns invalid JSON
        return ParsedJD(
            jd_id=str(hash(jd_text)),
            company="Unknown",
            category="default",
            sections=[Section(
                title=SectionType.REQUIREMENTS,
                content=[jd_text[:500]]  # Return raw text as fallback
            )]
        )
from sentence_transformers import SentenceTransformer, util
from ..models import ParsedResume, ParsedJD

model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightweight for local testing

def calculate_score(resume: ParsedResume, jd: ParsedJD) -> float:
    resume_text = " ".join([
        " ".join(section.content) 
        for section in resume.sections
    ])
    
    jd_text = " ".join([
        " ".join(section.content) 
        for section in jd.sections
    ])

    emb1 = model.encode(resume_text)
    emb2 = model.encode(jd_text)
    
    return float(util.cos_sim(emb1, emb2)[0][0])
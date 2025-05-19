from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from .parsers.resume_parser import parse_resume
from .parsers.jd_parser import parse_jd  # Added import for JD parsing
from .matching.scoring import calculate_score
from .database import get_db, init_db
from app.models import ParsedResume, ParsedJD
import json

app = FastAPI()

# Initialize database
init_db()

# Pydantic model for structured request validation
class ResumeRequest(BaseModel):
    resume_text: str
    category: Optional[str] = "default"

class JDRequest(BaseModel):
    jd_text: str
    company: Optional[str] = "unknown"
    category: Optional[str] = "general"

@app.get("/")
def read_root():
    return {
        "message": "Resume Matcher API", 
        "docs": "http://127.0.0.1:8000/docs"
    }

@app.post("/parse-resume")
async def parse_resume_endpoint(request: ResumeRequest):
    try:
        parsed = parse_resume(request.resume_text)
        with get_db() as cur:
            cur.execute(
                "INSERT INTO resumes (id, category, data) VALUES (%s, %s, %s)",
                (parsed.id, request.category, json.dumps(parsed.dict()))
            )
        return parsed.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/parse-jd")
async def parse_jd_endpoint(request: JDRequest):
    try:
        parsed = parse_jd(request.jd_text)
        with get_db() as cur:
            cur.execute(
                "INSERT INTO jds (jd_id, company, category, data) VALUES (%s, %s, %s, %s)",
                (parsed.jd_id, request.company, request.category, json.dumps(parsed.dict()))
            )
        return parsed.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/match/{resume_id}/{jd_id}")
async def match(resume_id: str, jd_id: str):
    print(f"\n--- MATCH REQUEST ---\nResume: {resume_id}\nJD: {jd_id}")  # Debug log
    
    try:
        with get_db() as cur:
            # Debug: Print raw data before processing
            cur.execute("SELECT data FROM resumes WHERE id = %s", (resume_id,))
            resume_data = cur.fetchone()
            print(f"Resume Data: {resume_data[0] if resume_data else 'NOT FOUND'}")
            
            cur.execute("SELECT data FROM jds WHERE jd_id = %s", (jd_id,))
            jd_data = cur.fetchone()
            print(f"JD Data: {jd_data[0] if jd_data else 'NOT FOUND'}")
            
            if not resume_data or not jd_data:
                raise HTTPException(404, "Data not found")
            
            # Add this debug line
            print("Attempting to calculate score...")
            
            resume_dict = resume_data[0] if isinstance(resume_data[0], dict) else json.loads(resume_data[0])
            jd_dict = jd_data[0] if isinstance(jd_data[0], dict) else json.loads(jd_data[0])
            
            resume = ParsedResume(**resume_dict)
            jd = ParsedJD(**jd_dict)
            
            score = calculate_score(resume, jd)
            return {"score": score}
            
    except Exception as e:
        print(f"!!! ERROR: {str(e)}")  # Critical debug line
        raise HTTPException(500, str(e))

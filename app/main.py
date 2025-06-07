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

# Pydantic models for request validation
class ResumeRequest(BaseModel):
    resume_text: str
    category: Optional[str] = "default"

class JDRequest(BaseModel):
    jd_text: str
    company: Optional[str] = "unknown"
    category: Optional[str] = "general"

class MatchRequest(BaseModel):
    resume_text: str
    jd_text: str

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

# Updated Match Endpoint with Enhanced Validation
@app.post("/match")
async def match_direct(request: MatchRequest):
    try:
        # Validate input texts
        if not request.resume_text.strip() or not request.jd_text.strip():
            raise HTTPException(status_code=422, detail="Input texts cannot be empty")

        parsed_resume = parse_resume(request.resume_text)
        parsed_jd = parse_jd(request.jd_text)

        # Final validation on parsed sections
        if not parsed_resume.sections:
            raise HTTPException(status_code=422, detail="No valid sections found in resume")
        if not parsed_jd.sections:
            raise HTTPException(status_code=422, detail="No valid sections found in job description")

        score = calculate_score(parsed_resume, parsed_jd)
        return {"score": float(score)}

    except json.JSONDecodeError:
        raise HTTPException(status_code=422, detail="Failed to parse document structure")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

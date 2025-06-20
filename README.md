
# ResumeMatcherAI

An AI-powered pipeline for **parsing resumes & job descriptions**, then calculating **compatibility scores** using **NLP** and **reinforcement learning**.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68%2B-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)](https://www.docker.com/)

---

## Project Overview

### **What This Does**
This **AI-driven matching system**:
1. **Parses** unstructured **resume/JD text** into structured JSON using **OpenAI GPT**.
2. **Stores** parsed data in a **PostgreSQL database**.
3. **Calculates** matching scores using:
   - **Sentence Transformers (E5-large embeddings)**
   - **BM25 lexical search**
   - **Reinforcement Learning-optimized weights**
4. **Deploys** via **FastAPI + Docker** (local) or **AWS Lambda** (production).

---

## Tech Stack

| Component              | Technology                           |
|------------------------|--------------------------------------|
| **Backend Framework**  | FastAPI                              |
| **Database**          | PostgreSQL                           |
| **NLP Parsing**       | OpenAI GPT-3.5/4                     |
| **Embeddings**       | Sentence Transformers (E5-large)     |
| **Data Validation**   | Pydantic                             |
| **Containerization**  | Docker                               |
| **Deployment**       | AWS Lambda + API Gateway             |
| **CI/CD**            | GitHub Actions                       |

---

## Features
-  **AI-powered resume/JD parsing**
-  **Hybrid scoring (semantic + keyword search)**
-  **RL-optimized section weighting**
-  **Dockerized local development**
-  **REST API endpoints**
-  **Interactive Swagger UI for testing**

---

##  How to Run Locally

### **Prerequisites**
- Python **3.9+**
- **Docker Desktop**
- **OpenAI API key**
- **PostgreSQL** installed or running via **Docker**
  
### **Project Structure**
   ```resume-matcher/
      ├── .env                    # Environment variables (OPENAI_API_KEY)
      ├── requirements.txt        # Python dependencies
      ├── app/                    # Main application code
      │   ├── __init__.py         # Makes app a Python package
      │   ├── main.py             # FastAPI entry point
      │   ├── models.py           # Pydantic models
      │   ├── database.py         # PostgreSQL connection
      │   ├── parsers/            # Parsing logic
      │   │   ├── __init__.py
      │   │   └── resume_parser.py
      │   └── matching/           # Scoring logic
      │       ├── __init__.py
      │       └── scoring.py
      ├── tests/                  # Test scripts
      │   ├── __init__.py
      │   └── test_data.json      # Sample resume/JD data
      ├── data/                   # Optional: Raw data storage
      │   ├── resumes/
      │   └── job_descriptions/
      └── README.md               # Project documentation
   ```

### **Local Setup**
1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/ResumeMatcherAI.git
   cd ResumeMatcherAI
   ```

2. Set environment variables (`.env` file):
   ```ini
   OPENAI_API_KEY=your_openai_key
   POSTGRES_PASSWORD=postgres
   ```

3. Local Database Setup
    ```Start PostgreSQL:
    
    docker run --name resume-db -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
    #if already created
    docker start resume-db
    
    docker exec -it resume-db psql -U postgres  
    \l
    CREATE DATABASE resume_matcher;
    \c resume_matcher
    \q
    ```


5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Run the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

7. Access **Swagger UI** to test endpoints:
   ```
   http://localhost:8000/docs
   ```
8. Run Streamlit Frontend
   ```
   streamlit run streamlit_app/main.py
   ```
Access UI: http://localhost:8501

---

##  Sample API Requests

### **1. Parse Resume**
#### **Request**
```bash
curl -X POST "http://localhost:8000/parse-resume" \
-H "Content-Type: application/json" \
-d '{"resume_text":"John Doe\nEducation: MIT Computer Science\nSkills: Python, SQL"}'
```
#### **Response**
```json
{
  "id": "3dfaa79f-e856-4e2c-a10d-aaa4122efdad",
  "category": "IT",
  "sections": [
    {
      "title": "EDUCATION",
      "content": ["MIT Computer Science"]
    },
    {
      "title": "SKILLS",
      "content": ["Python", "SQL"]
    }
  ]
}
```

### **2. Parse Job Description**
#### **Request**
```bash
curl -X POST "http://localhost:8000/parse-jd" \
-H "Content-Type: application/json" \
-d '{"jd_text":"Software Engineer\nRequirements: Python, CS degree"}'
```
#### **Response**
```json
{
  "jd_id": "-166096542090507509",
  "company": "TechCorp",
  "sections": [
    {
      "title": "REQUIREMENTS",
      "content": ["Python", "CS degree"]
    }
  ]
}
```

### **3. Get Match Score**
#### **Request**
```bash
curl "http://localhost:8000/match/3dfaa79f-e856-4e2c-a10d-aaa4122efdad/-166096542090507509"
```
#### **Response**
```json
{
  "resume_id": "3dfaa79f-e856-4e2c-a10d-aaa4122efdad",
  "jd_id": "-166096542090507509",
  "score": 0.87,
  "category": "IT"
}
```

---

##  Deployment Options

### **AWS Lambda Setup**
1. **Package for Lambda**:
   ```bash
   ./package.sh
   ```
2. **Deploy via AWS SAM**:
   ```bash
   sam deploy --guided
   ```

### **Docker Production Build**
1. **Build Docker image**:
   ```bash
   docker build -t resumematcher .
   ```
2. **Run container**:
   ```bash
   docker run -p 8000:8000 resumematcher
   ```

---

##  License
This project is licensed under the **MIT License** - see the [`LICENSE`](LICENSE) file for details.

---

##  Future Improvements
- Add **vector search** for more precise matching.
- Integrate **AWS Lambda** for lightweight serverless execution.
- Implement **user authentication** to secure API endpoints.
```

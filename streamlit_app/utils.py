import requests
from requests.exceptions import RequestException
import streamlit as st
from typing import Union

def parse_file(file: Union[bytes, str]) -> str:
    """Handle both text and PDF files"""
    if isinstance(file, bytes):
        try:
            return file.decode('utf-8')
        except UnicodeDecodeError:
            return file.decode('latin-1')
    return file

def get_matching_score(resume_text: str, jd_text: str) -> float:
    """Get base score from FastAPI backend with improved validation and error handling"""
    try:
        # Pre-validate inputs
        if not resume_text.strip() or not jd_text.strip():
            st.error("Input texts cannot be empty")
            st.stop()
        
        response = requests.post(
            "http://localhost:8000/match",
            json={"resume_text": resume_text, "jd_text": jd_text},
            headers={"Content-Type": "application/json"},
            timeout=10
        )

        # Handle validation errors
        if response.status_code == 422:
            error_detail = response.json().get("detail", "Validation error")
            st.error(f"Invalid document format: {error_detail}")
            st.stop()

        response.raise_for_status()  # Raises exception for HTTP errors
        return response.json()["score"]
        
    except RequestException as e:
        st.error(f"Connection failed: {str(e)}")
        st.info("Please ensure: 1) FastAPI is running 2) Documents have parsable content")
        st.stop()

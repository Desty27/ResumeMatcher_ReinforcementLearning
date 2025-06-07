import streamlit as st
import pdfplumber
from streamlit_app.feedback_db.feedback_logger import FeedbackLogger
from streamlit_app.rl_model.trainer import RLTrainer
from streamlit_app.utils import parse_file, get_matching_score

# Initialize components
feedback_logger = FeedbackLogger()
rl_trainer = RLTrainer()

def parse_uploaded_file(file):
    """Parse uploaded file, supporting both PDFs and text files."""
    if file.type == "application/pdf":
        try:
            with pdfplumber.open(file) as pdf:
                return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        except ImportError:
            st.error("PDF processing requires pdfplumber: pip install pdfplumber")
            st.stop()
    else:
        return file.getvalue().decode('utf-8')

def main():
    st.title("AI-Powered Resume Matcher ")
    st.markdown("Upload your resume and job description to get started!")
    
    # File uploaders
    col1, col2 = st.columns(2)
    with col1:
        resume_file = st.file_uploader("Upload Resume", type=["pdf", "txt"])
    with col2:
        jd_file = st.file_uploader("Upload Job Description", type=["pdf", "txt"])
    
    if resume_file and jd_file:
        try:
            resume_text = parse_uploaded_file(resume_file)
            jd_text = parse_uploaded_file(jd_file)
            
            # Get base score
            base_score = get_matching_score(resume_text, jd_text)
        except UnicodeDecodeError:
            st.error("Failed to decode files - please use UTF-8 text or PDFs")
            st.stop()

        # Apply RL adjustment
        adjusted_score = base_score
        if rl_trainer.model.is_fitted:
            adjustment = rl_trainer.model.predict_adjustment(base_score)
            adjusted_score = max(0, min(1, base_score + adjustment))
            st.metric("Adjusted Score", f"{adjusted_score*100:.1f}%", 
                      delta=f"{adjustment:.1%} adjustment")
        else:
            st.info("Model needs more feedback to make adjustments")

        # Display results
        st.subheader("Matching Results")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Base Score", f"{base_score*100:.1f}%")
        
        # Feedback system
        st.subheader("Feedback System")
        feedback = st.slider("How accurate is this match? (0 = Wrong, 10 = Perfect)", 0, 10)
        
        if st.button("Submit Feedback"):
            feedback_logger.log_feedback({
                'feedback': feedback,
                'score': base_score,
                'resume_text': resume_text,
                'jd_text': jd_text
            })
            
            if rl_trainer.train():  # Only show message if training occurred
                st.success("Model updated with new feedback!")
            else:
                st.info(f"Collected {len(feedback_logger.get_history())}/{rl_trainer.min_samples} feedback samples needed for training")
            
            st.rerun()

if __name__ == "__main__":
    main()

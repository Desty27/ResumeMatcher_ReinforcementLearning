import csv
import os
from datetime import datetime
import pandas as pd

FEEDBACK_PATH = os.path.join(os.path.dirname(__file__), "feedback.csv")

class FeedbackLogger:
    def __init__(self):
        self._init_csv()
    
    def _init_csv(self):
        if not os.path.exists(FEEDBACK_PATH):
            with open(FEEDBACK_PATH, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 
                    'user_feedback', 
                    'original_score',
                    'resume_text',
                    'jd_text'
                ])
    
    def log_feedback(self, feedback_data: dict):
        with open(FEEDBACK_PATH, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                feedback_data['feedback'],
                feedback_data['score'],
                feedback_data['resume_text'],
                feedback_data['jd_text']
            ])
    
    def get_history(self) -> pd.DataFrame:
        return pd.read_csv(FEEDBACK_PATH)
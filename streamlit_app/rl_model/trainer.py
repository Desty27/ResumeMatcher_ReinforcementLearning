import pandas as pd
from .model import ScoreAdjuster
from streamlit_app.feedback_db.feedback_logger import FeedbackLogger

class RLTrainer:
    def __init__(self):
        self.feedback = FeedbackLogger()
        self.model = ScoreAdjuster()
        self.min_samples = 10  # Minimum feedback samples needed
    
    def train(self):
        df = self.feedback.get_history()
        if len(df) < self.min_samples:
            return False  # Not enough data
        
        X = df[['original_score']]
        y = df['user_feedback'] / 10  # Normalize to 0-1
        
        self.model.update_model(X, y)
        return True

import joblib
import pandas as pd
from sklearn.linear_model import SGDRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

MODEL_PATH = "rl_model/score_predictor.pkl"

class ScoreAdjuster:
    def __init__(self):
        self.model = self._init_model()
        self.is_fitted = False  # Track fitting status
    
    def _init_model(self):
        try:
            return joblib.load(MODEL_PATH)
        except FileNotFoundError:
            return Pipeline([
                ('scaler', StandardScaler()),
                ('regressor', SGDRegressor(
                    loss='epsilon_insensitive',
                    random_state=42
                ))
            ])
    
    def predict_adjustment(self, current_score: float) -> float:
        if not self.is_fitted:
            return 0.0  # Return neutral adjustment if not trained
        return self.model.predict([[current_score]])[0]
    
    def update_model(self, X, y):
        if len(X) < 5:  # Minimum samples needed
            return
        
        if not self.is_fitted:
            self.model.fit(X, y)
            self.is_fitted = True
        else:
            self.model.partial_fit(X, y)
        
        joblib.dump(self.model, MODEL_PATH)

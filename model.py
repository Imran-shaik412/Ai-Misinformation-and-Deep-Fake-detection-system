import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Red-flag keywords that trigger intentional boosts in threat scores (Step 3)
KEYWORDS = [
    "pay", "urgent", "otp", "limited offer", "verify immediately", 
    "click link", "blocked", "vote", "cure instantly",
    "winner", "bank", "prize", "money", "claim", "gift",
    "unauthorized", "locked", "immediately", "account", "login"
]

class ThreatModel:
    def __init__(self):
        # Captures phrases like "bank account" or "verify identity"
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2)) 
        self.model = LogisticRegression()

    def clean(self, text):
        text = text.lower()
        # Keep only letters and spaces for better pattern recognition
        text = re.sub(r'[^a-z ]', '', text)
        return text

    def keyword_boost(self, text):
        score = 0
        t = text.lower()
        for k in KEYWORDS:
            if k in t:
                score += 0.08  # Significant boost for dangerous terms
        return min(score, 0.6) # Capped to ensure ML still plays a role

    def train(self, path):
        df = pd.read_csv(path)
        df["text"] = df["text"].apply(self.clean)
        
        X = self.vectorizer.fit_transform(df["text"])
        y = df["label"]
        
        self.model.fit(X, y)

    def predict(self, text):
        clean_text = self.clean(text)
        vec = self.vectorizer.transform([clean_text])
        
        # Get the probability of the scam (label 1)
        ml_prob = self.model.predict_proba(vec)[0][1]
        
        # Add the heuristic keyword boost
        boost = self.keyword_boost(text)
        
        final_score = min(ml_prob + boost, 1.0)
        return final_score
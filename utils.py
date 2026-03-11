import random
import numpy as np

# ---------- THREAT CLASSIFICATION (Step 4) ----------
def classify(text):
    t = text.lower()
    rules = {
        "Financial Scam": ["money", "pay", "bank", "tax", "lottery", "prize", "reward", "crypto", "gift card"],
        "Job Fraud": ["job", "recruitment", "salary", "hiring", "vacancy", "work from home", "part-time"],
        "Phishing": ["link", "verify", "blocked", "login", "password", "suspended", "account", "security"],
        "Political Manipulation": ["vote", "party", "election", "candidate", "propaganda", "campaign"],
        "Health Misinformation": ["cure", "medicine", "vaccine", "doctor", "virus", "remedy", "covid"],
        "Panic/Emotional": ["urgent", "share", "emergency", "immediately", "warning", "family", "help"]
    }
    
    for cat, keywords in rules.items():
        if any(w in t for w in keywords):
            return cat
            
    return "Social Engineering Attempt"


# ---------- HARM SEVERITY ENGINE (Step 5) ----------
weights = {
    "Financial Scam": 0.9, 
    "Phishing": 0.9, 
    "Health Misinformation": 0.8,
    "Political Manipulation": 1.0, 
    "Job Fraud": 0.7, 
    "Panic/Emotional": 0.6, 
    "Social Engineering Attempt": 0.5
}

def harm_score(prob, emotion, category):
    cat_weight = weights.get(category, 0.5)
    # Formula: (Threat Probability × 0.5) + (Emotional Intensity × 0.3) + (Category Weight × 0.2)
    return (prob * 0.5) + (emotion * 0.3) + (cat_weight * 0.2)

def harm_label(score):
    if score < 0.35: return "LOW", "green"
    elif score < 0.55: return "MEDIUM", "orange"
    elif score < 0.75: return "HIGH", "red"
    else: return "CRITICAL", "darkred"


# ---------- SPREAD RISK PREDICTOR ----------
def spread_prediction(prob, emotion, category):
    # Starting base for spread reach
    base = prob * 50
    
    # Emotional and Political content spreads faster
    boost = 0
    if emotion > 0.5: boost += 20
    if category == "Political Manipulation": boost += 20
    
    # Generate 12 hourly intervals
    x = np.arange(1, 13)
    
    # Sigmoid-like growth simulation
    y = []
    current = base + boost
    for i in x:
        growth = (100 - current) * 0.2 + random.randint(1, 4)
        current = min(100, current + growth)
        y.append(round(current, 1))
        
    return x, y


# ---------- EMOTIONAL INTENSITY ----------
def emotion_score(text):
    high = ["urgent", "immediately", "emergency", "alert", "panic", "warning", "blocked", "stopped"]
    score = sum(0.25 for w in high if w in text.lower())
    return min(score, 1.0)


# ---------- ADAPTIVE ADVISORY (Step 7) ----------
def get_advice(cat):
    advices = {
        "Financial Scam": "🚩 SAFETY PROTOCOL: Detect financial anomaly. Do not share bank details/OTPs. Report number to official bank support.",
        "Political Manipulation": "🗳️ NEUTRAL VERIFICATION: High political bias detected. Check neutral fact-checkers before sharing to prevent manipulation.",
        "Health Misinformation": "🏥 MEDICAL VERIFICATION: Claims regarding health must be verified with official sites (WHO/CDC) before treatment.",
        "Phishing": "🎣 IDENTITY PROTECTION: Hover over links to check real destinations. Never verify identity on unknown portals.",
        "Job Fraud": "💼 CAREER SAFETY: Legitimate companies never ask for 'security deposits' or upfront fees for job processing.",
        "Panic/Emotional": "⏱️ EMOTIONAL GUARD: This message uses urgency to trigger bypass of logic. Pause for 60 seconds before acting.",
        "Social Engineering Attempt": "🛡️ PSYCHOLOGICAL DEFENSE: Be cautious. This message uses engineered triggers to influence your digital behavior."
    }
    return advices.get(cat, "Stay cautious. Do not interact with suspicious elements.")


# ---------- VULNERABILITY CALCULATION (Step 8) ----------
def vulnerability_score(ans):
    # Each 'Yes' (True/1) contributes to the score
    return sum(ans) * 20

def risk_label(score):
    if score <= 20: return "Low Risk", "green"
    elif score <= 60: return "Moderate Risk", "orange"
    else: return "High Risk", "red"
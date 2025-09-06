import streamlit as st
import numpy as np
import joblib
import matplotlib.pyplot as plt
import os
import re
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# -------------------------
# Load ML Model
# -------------------------
@st.cache_resource
def load_model():
    path = os.path.join("Dataset", "log_reg.pkl")  # <-- make sure this path exists
    return joblib.load(path)

model = load_model()

# -------------------------
# NLP Setup
# -------------------------
nlp = spacy.load("en_core_web_sm")
analyzer = SentimentIntensityAnalyzer()

def parse_input(user_text, budget=50000):  # default free-spend budget = 50k
    # 1. Extract price
    price = 0
    match = re.search(r'(\d+\.?\d*)\s*([kK]|lacs?|Lacs?)?', user_text)
    if match:
        price = float(match.group(1))
        if match.group(2):
            if match.group(2).lower() == "k":
                price *= 1000
            elif "lac" in match.group(2).lower():
                price *= 100000

    # 2. Sentiment → Emotion
    sentiment = analyzer.polarity_scores(user_text)['compound']
    emotion = (sentiment + 1) / 2  # scale 0–1

    # 3. Urgency
    urgent_words = ["now", "today", "urgent", "immediately", "limited", "exclusive"]
    urgency_val = 1.0 if any(w in user_text.lower() for w in urgent_words) else 0.3

    # 4. Regret risk
    regret_words = ["regret", "out of my budget", "already have", "waste", "useless"]
    regret_val = 1.0 if any(w in user_text.lower() for w in regret_words) else 0.2

    # 5. Cost ratio
    cost_ratio = price / budget if budget else 0.5

    return [urgency_val, cost_ratio, emotion, regret_val]

# -------------------------
# UI
# -------------------------
st.title("🧠 Pocket Decision Simulator")

st.sidebar.header("Input Mode")
mode = st.sidebar.radio("Choose how to give inputs:", ["Sliders", "Text (NLP)"])

# -------------------------
# Sliders Mode
# -------------------------
if mode == "Sliders":
    urgency = st.slider("Urgency (0 = not urgent, 1 = very urgent)", 0.0, 1.0, 0.5)
    cost = st.slider("Cost ratio", 0.0, 1.5, 0.5)
    emotion = st.slider("Emotion level", 0.0, 1.0, 0.5)
    regret = st.slider("Regret risk", 0.0, 1.0, 0.5)

    if st.button("Simulate Decision"):
        x = np.array([[urgency, cost, emotion, regret]])
        pred = model.predict(x)[0]
        probs = model.predict_proba(x)[0]

        mapping = {
            0: "✅ Do it – looks like a safe choice.",
            1: "⏳ Wait – maybe sleep on it before deciding.",
            2: "❌ Don’t – high risk of regret here."
        }

        st.subheader(f"Recommendation: {mapping[pred]}")

        labels = ["Do it", "Wait", "Don’t"]
        fig, ax = plt.subplots()
        ax.pie(probs, labels=labels, autopct='%1.1f%%')
        st.pyplot(fig)

# -------------------------
# Text (NLP) Mode
# -------------------------
elif mode == "Text (NLP)":
    user_text = st.text_area("Describe your purchase thought in natural language:")

    budget = st.number_input("What’s your free-to-spend monthly budget? (₹)", value=50000, step=1000)

    if st.button("Analyze & Simulate"):
        features = parse_input(user_text, budget=budget)
        x = np.array([features])
        pred = model.predict(x)[0]
        probs = model.predict_proba(x)[0]

        mapping = {
            0: "✅ Do it – looks like a safe choice.",
            1: "⏳ Wait – maybe sleep on it before deciding.",
            2: "❌ Don’t – high risk of regret here."
        }

        st.subheader(f"Recommendation: {mapping[pred]}")

        labels = ["Do it", "Wait", "Don’t"]
        fig, ax = plt.subplots()
        ax.pie(probs, labels=labels, autopct='%1.1f%%')
        st.pyplot(fig)

        st.write("📊 Extracted features:", {
            "Urgency": features[0],
            "Cost Ratio": features[1],
            "Emotion": features[2],
            "Regret Risk": features[3]
        })

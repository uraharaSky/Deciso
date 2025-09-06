# 🧠 Deciso – Pocket Decision Simulator

## 📖 About the Project

**Deciso** is a small but powerful behavioral AI experiment.
It started on a casual weekend when I questioned myself:
*"Should I really spend on this writing tablet… especially after checking my bank balance?"*

That simple thought sparked the idea of **simulating spending decisions** — not just based on math, but also **urgency, emotions, and regret risk**.

---

## 💡 Why This Project

Most expense trackers only **record what you spend**.
Deciso is about **guiding you before you spend** — acting like a reflective friend that asks:

* *“Is this urgent?”*
* *“Can you afford it right now?”*
* *“Will you regret this later?”*

It’s not just about money, but about **behavioral decision-making**.

---

## 🚀 Current Version

Right now, Deciso can:

* Take inputs in **two ways**:

  * 🎚️ Slider Mode – Adjust urgency, cost ratio, emotion, regret.
  * 💬 Text Mode – Write naturally (*“I want to buy new Nike shoes for 25k, but I just bought a watch last week”*).

* Run predictions using **Logistic Regression (main)** and **Naive Bayes (baseline)**.

* Show **recommendations**:

  * ✅ *Do it* – safe choice.
  * ⏳ *Wait* – maybe pause and rethink.
  * ❌ *Don’t* – high risk of regret.

* Visualize results with a **probability pie chart**.

---

## 🔮 Future Scope

The vision is to make Deciso a **daily-use chatbot**:

* Conversational, multi-turn discussions about your purchases.
* Logs and learns from your **behavior over time**.
* More nuanced predictions (e.g., “Okay to buy if it’s for work, but risky if it’s just impulse”).
* Smarter NLP (handling all currency formats like *70k, 2.5L, \$500*).
* Explore models like Random Forest / Gradient Boosting for richer decision boundaries.

---

## 🏗️ System Flow

Here’s how Deciso works under the hood:

```
User Input (Sliders / Text)
          ↓
  [NLP Parser – extracts urgency, cost ratio, emotion, regret]
          ↓
  Feature Vector → [urgency, cost, emotion, regret]
          ↓
    Logistic Regression Model
          ↓
   Prediction (Do it / Wait / Don’t)
          ↓
   Output + Probability Pie Chart
```

*(Think of it like a behavioral filter sitting between you and your wallet 💸)*

---

## ⚙️ Installation

Until the hosted version goes live, you can run Deciso locally:

1. Clone the repo:

   ```bash
   git clone https://github.com/your-username/deciso.git
   cd deciso
   ```

2. Install requirements:

   ```bash
   pip install -r requirements.txt
   ```

3. Download the spaCy English model:

   ```bash
   python -m spacy download en_core_web_sm
   ```

4. Run the Streamlit app:

   ```bash
   streamlit run streamlit_interface.py
   ```

The app will open in your browser at **[http://localhost:8501](http://localhost:8501)**.

---

## ✍️ Closing Note

Deciso isn’t about telling you *what to buy* — it’s about helping you ask the right questions before spending.
This is just the **first step** toward a more human, behavior-aware finance assistant.


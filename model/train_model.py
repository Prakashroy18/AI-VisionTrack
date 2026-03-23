# model/train_model.py

import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# Load CSV data
df = pd.read_csv('../career_recommender.csv')

# Example: Combine relevant columns into a single feature string
feature_cols = [
    "What was your course in UG?",
    "What is your UG specialization? Major Subject (Eg; Mathematics)",
    "What are your interests?",
    "What are your skills ? (Select multiple if necessary)",
    "Did you do any certification courses additionally?",
    "Are you working?",
    "Have you done masters after undergraduation? If yes, mention your field of masters.(Eg; Masters in Mathematics)"
]
label_col = "If yes, then what is/was your first Job title in your current field of work? If not applicable, write NA.               "

# Fill NaNs and combine features
df = df.fillna("")
X_raw = df[feature_cols].apply(lambda row: " ".join(str(x) for x in row), axis=1)
y = df[label_col].replace("NA", "").replace("", None)

# Remove rows with empty labels
mask = y.notnull() & (y != "")
X_raw = X_raw[mask]
y = y[mask]

# Vectorize features
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(X_raw)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# Save model and vectorizer
joblib.dump(model, "career_model.pkl")
joblib.dump(vectorizer, "label_encoder.pkl")

print("✅ Model and label encoder saved using CSV data.")

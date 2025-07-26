import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
import joblib
import os

# Label mapping
LABELS = ["Ham", "Spam", "Spoofed"]
label_map = {"Ham": 0, "Spam": 1, "Spoofed": 2}
inv_label_map = {0: "Ham", 1: "Spam", 2: "Spoofed"}

# --- Training code (run as script) ---
def train_and_save():
    df1 = pd.read_csv("data/training_data.csv")  # Main training set
    df2_path = "data/feedback_data.csv"          # Feedback data from app
    # Combine feedback if available
    if os.path.exists(df2_path):
        df2 = pd.read_csv(df2_path, names=["email", "label"], header=None)
        df = pd.concat([df1, df2], ignore_index=True)
    else:
        df = df1
    df["label_num"] = df["label"].apply(lambda x: label_map.get(x, -1))
    X_train, X_test, y_train, y_test = train_test_split(df["email"], df["label_num"], test_size=0.2, random_state=42)
    vectorizer = TfidfVectorizer(stop_words='english', max_features=3000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_vec, y_train)
    if not os.path.exists("models"):
        os.makedirs("models")
    joblib.dump(model, "models/email_model.pkl")
    joblib.dump(vectorizer, "models/vectorizer.pkl")
    acc = model.score(X_test_vec, y_test)
    y_pred = model.predict(X_test_vec)
    report = classification_report(y_test, y_pred, target_names=LABELS)
    print(f"✅ Model trained. Accuracy: {acc:.2f}")
    print("📊 Classification Report:")
    print(report)

# --- Prediction function for API ---
def predict(email_text):
    model = joblib.load("models/email_model.pkl")
    vectorizer = joblib.load("models/vectorizer.pkl")
    X_vec = vectorizer.transform([email_text])
    pred_num = model.predict(X_vec)[0]
    return [inv_label_map.get(pred_num, "Unknown")]

# --- Optional: retrain function for API ---
def retrain(texts, labels):
    # Append new data to feedback_data.csv
    df2_path = "data/feedback_data.csv"
    new_data = pd.DataFrame({"email": texts, "label": labels})
    if os.path.exists(df2_path):
        new_data.to_csv(df2_path, mode="a", header=False, index=False)
    else:
        new_data.to_csv(df2_path, mode="w", header=False, index=False)
    # Retrain model
    train_and_save()
    return {"status": "Retrained with new data."}

if __name__ == "__main__":
    train_and_save() 
import re
import joblib
from scipy.sparse import hstack

print("Loading Model...")

model = joblib.load("model/phishing_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")

print("Model Loaded Successfully!")

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def count_urls(text):
    urls = re.findall(r"http[s]?://\S+|www\.\S+",text)
    return len(urls)

def predict_email(email):
    url_count = count_urls(email)
    cleaned_email = clean_text(email)
    text_features = vectorizer.transform([cleaned_email])
    X = hstack([text_features, [[url_count]]])
    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0]
    if prediction == 1:
        result = "PHISHING"
    else:
        result = "SAFE"
    confidence = max(probability) * 100
    return result, confidence

print("=" * 60)
print("PHISHING EMAIL DETECTION")
print("=" * 60)

while True:
    print("\nPaste Email Below:")
    email = input("> ")
    result, confidence = predict_email(email)
    print("\nPrediction :", result)
    print(f"Confidence : {confidence:.2f}%")
    choice = input("\nCheck another email? (y/n): ")
    if choice.lower() != "y":
        break
    
print("\nThank You!")
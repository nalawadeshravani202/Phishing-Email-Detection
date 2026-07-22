import re
import joblib
from flask import Flask, render_template, request
from scipy.sparse import hstack

app = Flask(__name__)

model = joblib.load("model/phishing_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def count_urls(text):
    urls = re.findall(r"http[s]?://\S+|www\.\S+", text)
    return len(urls)

@app.route("/", methods=["GET", "POST"])

def home():
    prediction = None
    confidence = None
    url_count = None
    email = ""

    if request.method == "POST":
        email = request.form["email"]
        url_count = count_urls(email)
        cleaned = clean_text(email)
        text_feature = vectorizer.transform([cleaned])
        X = hstack([text_feature, [[url_count]]])
        pred = model.predict(X)[0]
        prob = model.predict_proba(X)[0]
        confidence = round(max(prob) * 100, 2)

        if pred == 1:
            prediction = "PHISHING"
        else:
            prediction = "SAFE"

    return render_template(
        "index.html",
        prediction=prediction,
        confidence=confidence,
        url_count=url_count,
        email=email,
        accuracy=MODEL_ACCURACY
    )

MODEL_ACCURACY = "99.45%"

if __name__ == "__main__":
    app.run(debug=True)
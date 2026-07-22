import os 
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from scipy.sparse import hstack
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import(
    accuracy_score,
    confusion_matrix,
    classification_report
)

print("=" * 60)
print("Loading Dataset...")
print("=" * 60)

df = pd.read_csv("dataset/processed/cleaned_emails.csv")
print("Dataset Loaded Successfully")
print("Dataset Shape :", df.shape)

X_text = df["text"]
X_urls = df["urls"]
y = df["label"]

print("\nSplitting Dataset...")

X_text_train, X_text_test, X_urls_train, X_urls_test, y_train, y_test = train_test_split(
    X_text,
    X_urls,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training Samples :", len(X_text_test))
print("Testing Samples :", len(X_text_test))

print("\nApplying TF-IDF Vectorization...")

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

X_train_text = vectorizer.fit_transform(X_text_train)
X_test_text = vectorizer.transform(X_text_test)

X_urls_train = X_urls_train.values.reshape(-1,1)
X_urls_test = X_urls_test.values.reshape(-1,1)

X_train = hstack([X_train_text, X_urls_train])
X_test = hstack([X_test_text, X_urls_test])

print("Feature Extraction Completed!")

print("\nTraining Logistic Regression Model...")

model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

model.fit(X_train, y_train)

print("Model Training Completed!")

print("\nPredicting Test Data...")

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\n" + "=" * 60)
print("MODEL ACCURACY")
print("=" * 60)

print(f"Accuracy : {accuracy*100:.2f}%")

cm = confusion_matrix(y_test, predictions)
print("\nConfusion Matrix:\n")
print(cm)

print("\nClassification Report :\n")
print(classification_report(
    y_test,
    predictions,
    target_names=["Safe", "Phishing"]
))

os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/phishing_model.pkl")
joblib.dump(vectorizer,"model/vectorizer.pkl")

print("\nModel Saved Successfully!")
print("Vectorizer Saved Successfully!")

os.makedirs("results", exist_ok=True)

plt.figure(figsize=(6, 5))
plt.imshow(cm, interpolation="nearest")
plt.title("Confusion Matrix")
plt.colorbar()

classes = ["Safe", "Phishing"]

plt.xticks([0,1], classes)
plt.yticks([0,1], classes)

plt.xlabel("Predicted Label")
plt.ylabel("True Label")

for i in range(len(classes)):
    for j in range(len(classes)):
        plt.text(
            j,
            i,
            cm[i,j],
            ha="center",
            va="center",
            fontsize=12
        )

plt.tight_layout()
plt.savefig("results/confusion_matrix.png")
plt.show()
print("\nConfusion Matrix Image Saved Successfully!")
print("Location: results/confusion_matrix.png")

print("\n" + "=" * 60)
print("PROJECT PHASE 5 COMPLETED SUCCESSFULLY")
print("=" * 60)
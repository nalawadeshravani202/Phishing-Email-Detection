import pandas as pd
import re

df = pd.read_csv("dataset/emails.csv")

print("=" * 50)
print("Original Dataset Information")
print("=" * 50)

print(df.head())

print("\nDataset Shape:")
print(df.shape)

df["subject"] = df["subject"].fillna("")

df["text"] = df["subject"] + " " + df["body"]

def clean_text(text):
    text = text.lower()
    text = re.sub(r"htpp\S+|www\S+", " ", text)
    text = re.sub(r"\s+@\S+", " ", text)
    text = re.sub(r"\d+", " ", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

df["text"] = df["text"].apply(clean_text)

clean_df = df[["text", "urls", "label"]]

print("\nCleaned Dataset")
print(clean_df.head())

clean_df.to_csv(
    "dataset/processed/cleaned_emails.csv",
    index=False
)

print("\nCleaning Completed Successfully!")
print("Cleaned dataset saved to : dataset/processed/cleaned_emails.csv")
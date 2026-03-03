# Email Spam Classifier

An AI-powered email spam detection system built with **Python, Flask, Scikit-learn, and NLTK**. The classifier uses a **Multinomial Naive Bayes** model trained on TF-IDF features to detect spam emails in real-time through a clean web interface.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Model Training](#model-training)
- [Setup & Running](#setup--running)
- [API Reference](#api-reference)
- [How It Works](#how-it-works)

---

## Overview

Paste any email text into the web interface and get an instant prediction: **SPAM** or **HAM**. The underlying model is trained with a TF-IDF bag-of-words representation and a Multinomial Naive Bayes classifier, achieving high accuracy on typical spam detection benchmarks.

---

## Features

- Real-time email classification via web UI
- Pre-trained model ready to use — no training required
- Custom dataset generation included in `spam_classifier.py`
- Full training pipeline: preprocessing → vectorization → model → evaluation → save
- Model persistence with `pickle`
- Flask REST API

---

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| ML Model | Multinomial Naive Bayes (Scikit-learn) |
| Text Features | TF-IDF Vectorizer (3000 max features) |
| NLP Pre-processing | NLTK (stopwords, Porter stemmer) |
| Frontend | HTML, CSS (templates/ & static/) |

---

## Project Structure

```
email-spam-classifier/
├── app.py                        # Flask web application
├── spam_classifier.py            # EmailSpamClassifier class + training script
├── spam_classifier_model.pkl     # Pre-trained Naive Bayes model + vectorizer
├── requirements.txt              # Python dependencies
├── templates/
│   └── index.html                # Web UI
├── static/                       # CSS / JS assets
├── .gitignore
└── README.md
```

---

## Model Training

The `spam_classifier.py` module contains:

### `EmailSpamClassifier` class

| Method | Description |
|---|---|
| `preprocess_text(text)` | Lowercase → remove special chars → remove stopwords → Porter stem |
| `train(X_train, y_train)` | Vectorizes text with TF-IDF, fits Multinomial NB |
| `predict(X_test)` | Returns `spam` or `ham` predictions |
| `evaluate(X_test, y_test)` | Prints accuracy, confusion matrix, classification report |
| `save_model(filepath)` | Saves model + vectorizer to `.pkl` |
| `load_model(filepath)` | Loads model + vectorizer from `.pkl` |

### Training pipeline

```python
from spam_classifier import EmailSpamClassifier, create_sample_dataset
from sklearn.model_selection import train_test_split

df = create_sample_dataset()
X_train, X_test, y_train, y_test = train_test_split(
    df['email'], df['label'], test_size=0.2, stratify=df['label']
)
clf = EmailSpamClassifier()
clf.train(X_train, y_train)
clf.evaluate(X_test, y_test)
clf.save_model()
```

---

## Setup & Running

```bash
git clone https://github.com/jaideepj2004/email-spam-classifier.git
cd email-spam-classifier
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

### `requirements.txt`
```
flask
scikit-learn
nltk
```

---

## API Reference

### `GET /`
Returns the classification interface.

### `POST /predict`
Classify an email as spam or ham.

**Form body:** `email=<email text>`

**Response:** Renders `index.html` with prediction result.

---

## How It Works

1. User submits email text via the web form.
2. Flask `POST /predict` receives the text.
3. The pre-existing `spam_classifier_model.pkl` is loaded (contains model + vectorizer).
4. Text is pre-processed: lowercase → remove special chars → remove NLTK stopwords → Porter stemming.
5. TF-IDF vectorizer transforms the clean text.
6. Multinomial NB predicts `spam` (1) or `ham` (0).
7. Result is rendered back on the webpage.

---

## Example Predictions

| Email | Result |
|---|---|
| "Congratulations! Click here to claim your $1,000,000 prize!" | **SPAM** |
| "Can we reschedule the meeting to 3pm?" | **HAM** |
| "FREE Viagra! Order now, no prescription needed!" | **SPAM** |
| "Please review the attached quarterly report." | **HAM** |

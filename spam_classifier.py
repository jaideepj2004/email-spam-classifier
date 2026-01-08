import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

class EmailSpamClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=3000)
        self.model = MultinomialNB()
        self.stemmer = PorterStemmer()
        
    def preprocess_text(self, text):
        """Clean and preprocess email text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespaces
        text = ' '.join(text.split())
        
        # Tokenize and remove stopwords
        try:
            stop_words = set(stopwords.words('english'))
            words = text.split()
            words = [self.stemmer.stem(word) for word in words if word not in stop_words]
            text = ' '.join(words)
        except:
            # If stopwords not downloaded, continue without them
            pass
            
        return text
    
    def train(self, X_train, y_train):
        """Train the spam classifier"""
        print("Preprocessing training data...")
        X_train_processed = [self.preprocess_text(text) for text in X_train]
        
        print("Vectorizing text...")
        X_train_vectorized = self.vectorizer.fit_transform(X_train_processed)
        
        print("Training model...")
        self.model.fit(X_train_vectorized, y_train)
        print("Training completed!")
        
    def predict(self, X_test):
        """Predict spam or ham"""
        X_test_processed = [self.preprocess_text(text) for text in X_test]
        X_test_vectorized = self.vectorizer.transform(X_test_processed)
        predictions = self.model.predict(X_test_vectorized)
        return predictions
    
    def evaluate(self, X_test, y_test):
        """Evaluate model performance"""
        predictions = self.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        
        print(f"\n{'='*50}")
        print(f"MODEL EVALUATION")
        print(f"{'='*50}")
        print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"\nConfusion Matrix:")
        print(confusion_matrix(y_test, predictions))
        print(f"\nClassification Report:")
        print(classification_report(y_test, predictions, target_names=['Ham', 'Spam']))
        
        return accuracy
    
    def save_model(self, filepath='spam_classifier_model.pkl'):
        """Save trained model"""
        with open(filepath, 'wb') as f:
            pickle.dump({'model': self.model, 'vectorizer': self.vectorizer}, f)
        print(f"\nModel saved to {filepath}")
    
    def load_model(self, filepath='spam_classifier_model.pkl'):
        """Load trained model"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.vectorizer = data['vectorizer']
        print(f"Model loaded from {filepath}")


def create_sample_dataset():
    """Create a sample dataset for demonstration"""
    spam_emails = [
        "Congratulations! You've won $1,000,000! Click here to claim your prize now!",
        "URGENT: Your account will be closed. Verify your identity immediately!",
        "Get rich quick! Make $5000 per week working from home!",
        "You have been selected for a special offer. Act now!",
        "Hot singles in your area want to meet you!",
        "Buy cheap medications online. No prescription needed!",
        "Claim your free gift card worth $500 now!",
        "Your PayPal account has been limited. Click here to restore access.",
        "Earn money fast with our proven system!",
        "You've been pre-approved for a loan of $50,000!",
        "FREE! FREE! FREE! Click now to get your free iPhone!",
        "Lose 30 pounds in 30 days with this miracle pill!",
        "Make money online from home. No experience required!",
        "Your computer may be infected. Download our antivirus now!",
        "Congratulations! You've been selected as a winner!",
        "Click here for a special discount on luxury watches!",
        "Your package could not be delivered. Update your address now.",
        "Meet beautiful women tonight! Sign up free!",
        "Get Viagra at the lowest prices! Order now!",
        "Your tax refund is ready. Click to claim it!",
    ]
    
    ham_emails = [
        "Hey, are we still on for the meeting tomorrow at 3pm?",
        "Thanks for sending over the report. I'll review it this afternoon.",
        "Can you please send me the project documentation?",
        "The quarterly review is scheduled for next Friday.",
        "I've attached the files you requested in your last email.",
        "Let's schedule a call to discuss the new requirements.",
        "Your order #12345 has been shipped and will arrive in 3-5 business days.",
        "Reminder: Team lunch is this Thursday at noon.",
        "Please find attached the minutes from today's meeting.",
        "Could you review this document and provide your feedback?",
        "Your subscription renewal is coming up next month.",
        "The system maintenance is scheduled for this weekend.",
        "Thanks for your help with the presentation yesterday.",
        "I've updated the spreadsheet with the latest numbers.",
        "Your appointment is confirmed for Monday at 10am.",
        "Can we reschedule our meeting to next week?",
        "The training session has been moved to Room 304.",
        "Please submit your timesheet by end of day Friday.",
        "Your monthly statement is now available online.",
        "Looking forward to working with you on this project.",
    ]
    
    # Create DataFrame
    emails = spam_emails + ham_emails
    labels = ['spam'] * len(spam_emails) + ['ham'] * len(ham_emails)
    
    df = pd.DataFrame({'email': emails, 'label': labels})
    
    # Shuffle the dataset
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    return df


def main():
    print("="*50)
    print("EMAIL SPAM CLASSIFIER")
    print("="*50)
    
    # Download NLTK data
    print("\nDownloading required NLTK data...")
    try:
        nltk.download('stopwords', quiet=True)
        nltk.download('punkt', quiet=True)
        print("NLTK data downloaded successfully!")
    except:
        print("Warning: Could not download NLTK data. Continuing without stopwords...")
    
    # Create sample dataset
    print("\nCreating sample dataset...")
    df = create_sample_dataset()
    print(f"Dataset created with {len(df)} emails")
    print(f"Spam emails: {(df['label'] == 'spam').sum()}")
    print(f"Ham emails: {(df['label'] == 'ham').sum()}")
    
    # Split dataset
    print("\nSplitting dataset into train and test sets...")
    X = df['email'].values
    y = df['label'].values
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training set: {len(X_train)} emails")
    print(f"Test set: {len(X_test)} emails")
    
    # Initialize and train classifier
    classifier = EmailSpamClassifier()
    classifier.train(X_train, y_train)
    
    # Evaluate model
    classifier.evaluate(X_test, y_test)
    
    # Save model
    classifier.save_model()
    
    # Test with custom emails
    print(f"\n{'='*50}")
    print("TESTING WITH CUSTOM EMAILS")
    print(f"{'='*50}")
    
    test_emails = [
        "Hi John, let's meet for coffee tomorrow at 2pm",
        "CLICK HERE NOW! You've won a FREE vacation to Hawaii!",
        "Please review the attached quarterly report",
        "Get rich quick! Make thousands of dollars daily!",
    ]
    
    for email in test_emails:
        prediction = classifier.predict([email])[0]
        print(f"\nEmail: {email[:60]}...")
        print(f"Prediction: {prediction.upper()}")
    
    print(f"\n{'='*50}")
    print("Classifier training and testing completed successfully!")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()

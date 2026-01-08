from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pickle
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

app = Flask(__name__)
CORS(app)

# Download NLTK data
try:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
except:
    pass

# Load the trained model
try:
    with open('spam_classifier_model.pkl', 'rb') as f:
        model_data = pickle.load(f)
        model = model_data['model']
        vectorizer = model_data['vectorizer']
    print("Model loaded successfully!")
except:
    print("Warning: Model not found. Please train the model first by running spam_classifier.py")
    model = None
    vectorizer = None

stemmer = PorterStemmer()

def preprocess_text(text):
    """Clean and preprocess email text"""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = ' '.join(text.split())
    
    try:
        stop_words = set(stopwords.words('english'))
        words = text.split()
        words = [stemmer.stem(word) for word in words if word not in stop_words]
        text = ' '.join(words)
    except:
        pass
        
    return text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        email_text = data.get('email', '')
        
        if not email_text:
            return jsonify({'error': 'No email text provided'}), 400
        
        if model is None or vectorizer is None:
            return jsonify({'error': 'Model not loaded. Please train the model first.'}), 500
        
        # Preprocess and predict
        processed_text = preprocess_text(email_text)
        vectorized_text = vectorizer.transform([processed_text])
        prediction = model.predict(vectorized_text)[0]
        probability = model.predict_proba(vectorized_text)[0]
        
        # Get confidence scores
        spam_confidence = probability[1] * 100
        ham_confidence = probability[0] * 100
        
        return jsonify({
            'prediction': prediction,
            'spam_confidence': round(spam_confidence, 2),
            'ham_confidence': round(ham_confidence, 2),
            'is_spam': prediction == 'spam'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("="*50)
    print("Starting Email Spam Classifier Web App")
    print("="*50)
    print("Open your browser and go to: http://localhost:5000")
    print("="*50)
    app.run(debug=True, port=5000)

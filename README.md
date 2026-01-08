# 📧 Email Spam Classifier

An AI-powered email spam detection system built with Machine Learning and a beautiful web interface.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.0+-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

- 🤖 **Machine Learning Classification** - Uses Multinomial Naive Bayes algorithm
- 🎨 **Beautiful Web Interface** - Modern, responsive UI built with HTML/CSS/JavaScript
- 📊 **Confidence Scores** - Shows probability percentages for spam/legitimate classification
- ⚡ **Real-time Detection** - Instant classification results
- 💾 **Model Persistence** - Save and load trained models
- 🧹 **Text Preprocessing** - Advanced NLP techniques (stemming, stopword removal, TF-IDF)

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/jaideepj2004/email-spam-classifier.git
cd email-spam-classifier
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Train the model (first time only):
```bash
python spam_classifier.py
```

4. Run the web application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## 📁 Project Structure

```
email-spam-classifier/
│
├── app.py                          # Flask web application
├── spam_classifier.py              # ML model training script
├── requirements.txt                # Python dependencies
├── spam_classifier_model.pkl       # Trained model (generated)
│
├── templates/
│   └── index.html                  # Main web interface
│
└── static/
    ├── style.css                   # Styling
    └── script.js                   # Frontend logic
```

## 🎯 How It Works

1. **Text Preprocessing**: 
   - Convert to lowercase
   - Remove special characters and digits
   - Remove stopwords
   - Apply stemming

2. **Feature Extraction**:
   - TF-IDF Vectorization (max 3000 features)

3. **Classification**:
   - Multinomial Naive Bayes classifier
   - Returns spam/ham prediction with confidence scores

## 📊 Model Performance

- **Algorithm**: Multinomial Naive Bayes
- **Accuracy**: ~75% on test set
- **Features**: TF-IDF with 3000 max features
- **Preprocessing**: Stemming + Stopword removal

## 🖼️ Screenshots

The web interface provides:
- Clean, modern design with gradient backgrounds
- Real-time classification results
- Confidence visualization with animated bars
- Quick example buttons for testing
- Responsive design for mobile devices

## 🛠️ Technologies Used

- **Backend**: Python, Flask, Flask-CORS
- **ML Libraries**: Scikit-learn, NLTK, Pandas, NumPy
- **Frontend**: HTML5, CSS3, JavaScript
- **Icons**: Font Awesome

## 📝 Usage Example

```python
from spam_classifier import EmailSpamClassifier

# Initialize classifier
classifier = EmailSpamClassifier()

# Train on your data
classifier.train(X_train, y_train)

# Make predictions
predictions = classifier.predict(X_test)

# Evaluate performance
classifier.evaluate(X_test, y_test)

# Save the model
classifier.save_model('my_model.pkl')
```

## 🔮 Future Enhancements

- [ ] Add more sophisticated algorithms (SVM, Random Forest, Deep Learning)
- [ ] Implement user feedback loop for continuous learning
- [ ] Add email header analysis
- [ ] Support for multiple languages
- [ ] Integration with email clients
- [ ] Batch email processing
- [ ] Export classification reports

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Jaideep Jaiswal**
- GitHub: [@jaideepj2004](https://github.com/jaideepj2004)

## 🙏 Acknowledgments

- Scikit-learn for the amazing ML library
- Flask for the lightweight web framework
- NLTK for natural language processing tools

---

⭐ If you found this project helpful, please give it a star!

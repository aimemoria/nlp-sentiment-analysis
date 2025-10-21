import numpy as np
import pandas as pd
import re
import string
import pickle
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Download NLTK data
for package in ['stopwords', 'punkt', 'wordnet', 'omw-1.4']:
    try:
        nltk.download(package, quiet=True)
    except:
        pass


class SentimentModel:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def preprocess_text(self, text):
        """Clean and preprocess text"""
        if not text:
            return ''

        # Remove HTML tags
        text = BeautifulSoup(text, 'html.parser').get_text()
        text = text.lower()
        text = re.sub(r'http\S+', '', text)
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'\s+', ' ', text).strip()

        # Tokenize and clean
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if word not in self.stop_words and len(word) > 2]
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens]

        return ' '.join(tokens)

    def create_sample_data(self):
        """Create training dataset"""
        positive = [
            "This movie is fantastic! Great acting and amazing story.",
            "I loved it! One of the best films I've ever seen.",
            "Brilliant performances and excellent direction.",
            "Absolutely wonderful! Highly recommended.",
            "Amazing experience. The best movie of the year!",
        ] * 100

        negative = [
            "Terrible movie. Complete waste of time.",
            "Awful acting and boring plot. Very disappointed.",
            "One of the worst films ever. Don't watch this.",
            "Poor quality and ridiculous story.",
            "Horrible experience. I want my money back.",
        ] * 100

        reviews = positive + negative
        sentiments = ['positive'] * len(positive) + ['negative'] * len(negative)

        df = pd.DataFrame({'review': reviews, 'sentiment': sentiments})
        return df.sample(frac=1, random_state=42).reset_index(drop=True)

    def train(self):
        """Train the model"""
        print('Training model...')
        df = self.create_sample_data()
        df['cleaned'] = df['review'].apply(self.preprocess_text)
        df = df[df['cleaned'].str.len() > 0]

        X = df['cleaned']
        y = df['sentiment']

        # Create TF-IDF features
        self.vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
        X_tfidf = self.vectorizer.fit_transform(X)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_tfidf, y, test_size=0.2, random_state=42, stratify=y
        )

        # Train model
        self.model = LogisticRegression(max_iter=1000, random_state=42)
        self.model.fit(X_train, y_train)

        # Calculate accuracy
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        print(f'Model trained! Accuracy: {accuracy:.2%}')
        return accuracy

    def predict(self, review):
        """Predict sentiment of a review"""
        if not self.is_trained():
            raise Exception('Model not trained')

        cleaned = self.preprocess_text(review)
        if not cleaned:
            cleaned = 'empty'

        review_tfidf = self.vectorizer.transform([cleaned])
        prediction = self.model.predict(review_tfidf)[0]
        probabilities = self.model.predict_proba(review_tfidf)[0]

        classes = self.model.classes_
        confidence = {
            classes[0]: float(probabilities[0] * 100),
            classes[1]: float(probabilities[1] * 100)
        }

        return {
            'sentiment': prediction,
            'confidence': confidence
        }

    def is_trained(self):
        """Check if model is trained"""
        return self.model is not None and self.vectorizer is not None

    def save_model(self, filepath):
        """Save model to file"""
        with open(filepath, 'wb') as f:
            pickle.dump({'model': self.model, 'vectorizer': self.vectorizer}, f)

    def load_model(self, filepath):
        """Load model from file"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.vectorizer = data['vectorizer']

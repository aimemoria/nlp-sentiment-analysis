# Sentiment Analysis Web App

A simple React + Flask web application for movie review sentiment analysis.

## Features

- Train ML model (TF-IDF + Logistic Regression)
- Analyze movie reviews
- See sentiment predictions with confidence scores
- Clean, minimal interface

## Quick Start

### Backend Setup

```bash
cd sentiment-analysis-app/backend

# Install dependencies
pip install -r requirements.txt

# Start server
python app.py
```

Backend runs on `http://localhost:5000`

### Frontend Setup

```bash
cd sentiment-analysis-app/frontend

# Install dependencies
npm install

# Start app
npm start
```

Frontend opens at `http://localhost:3000`

## Usage

1. **Train Model**: Click "Train Model" button (takes ~10 seconds)
2. **Enter Review**: Type any movie review in the text box
3. **Analyze**: Click "Analyze" to see sentiment prediction
4. **View Results**: See POSITIVE/NEGATIVE with confidence percentages

## Technology

**Frontend:**
- React 18
- Axios
- Simple CSS

**Backend:**
- Flask
- Scikit-learn
- NLTK
- BeautifulSoup

## API Endpoints

- `GET /api/status` - Check model status
- `POST /api/train` - Train the model
- `POST /api/predict` - Predict sentiment

## Project Structure

```
sentiment-analysis-app/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── SentimentAnalyzer.js
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
└── backend/
    ├── app.py
    ├── sentiment_model.py
    └── requirements.txt
```

## Notes

- Simple implementation for learning purposes
- Uses sample dataset (1,000 reviews)
- Model saves automatically after training
- Clean, minimal UI design

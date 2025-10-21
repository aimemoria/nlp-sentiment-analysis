#!/bin/bash
cd AIT-204-NLP-main/sentiment-analysis-app/backend
python -m nltk.downloader punkt stopwords
gunicorn --bind 0.0.0.0:$PORT app:app

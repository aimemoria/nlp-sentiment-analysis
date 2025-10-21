import React from 'react';
import './App.css';
import SentimentAnalyzer from './components/SentimentAnalyzer';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>IMDB Sentiment Analysis</h1>
        <p>Analyze movie review sentiment using Machine Learning</p>
      </header>
      <main className="App-main">
        <SentimentAnalyzer />
      </main>
      <footer className="App-footer">
        <p>Built with React + Flask + Scikit-learn | TF-IDF + Logistic Regression</p>
      </footer>
    </div>
  );
}

export default App;

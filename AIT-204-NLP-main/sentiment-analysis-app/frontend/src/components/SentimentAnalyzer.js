import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './SentimentAnalyzer.css';

const API_URL = process.env.REACT_APP_API_URL || '';

function SentimentAnalyzer() {
  const [review, setReview] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [modelReady, setModelReady] = useState(false);
  const [error, setError] = useState(null);

  // Example reviews
  const exampleReviews = {
    positive: [
      "This movie was absolutely amazing! Best film I've seen this year! The acting was superb and the plot kept me engaged throughout.",
      "Incredible performances and a gripping storyline. Highly recommend! A masterpiece of cinema.",
      "Fantastic! Every scene was brilliantly executed. The director's vision really shines through."
    ],
    negative: [
      "Terrible movie. Complete waste of time and money. Poor acting and boring plot.",
      "Very disappointed. The story made no sense and the characters were one-dimensional.",
      "Awful film. I couldn't even finish watching it. Absolutely terrible in every aspect."
    ],
    neutral: [
      "It was okay, nothing special. Some good moments but overall average.",
      "Decent movie, had its ups and downs. Not great, not terrible."
    ]
  };

  // Check if model is ready on load
  useEffect(() => {
    axios.get(`${API_URL}/api/status`)
      .then(res => setModelReady(res.data.status === 'ready'))
      .catch(() => setError('Cannot connect to server'));
  }, []);

  const trainModel = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_URL}/api/train`);
      setModelReady(true);
      alert(`Model trained successfully!\nAccuracy: ${(response.data.accuracy * 100).toFixed(2)}%`);
    } catch (err) {
      setError('Training failed: ' + err.message);
    }
    setLoading(false);
  };

  const analyzeSentiment = async () => {
    if (!review.trim()) {
      setError('Please enter a review to analyze');
      return;
    }

    if (review.length > 1000) {
      setError('Review is too long. Maximum 1000 characters.');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${API_URL}/api/predict`, { review });
      setResult(response.data);
    } catch (err) {
      setError('Analysis failed: ' + err.message);
    }
    setLoading(false);
  };

  const loadExample = (text) => {
    setReview(text);
    setResult(null);
    setError(null);
  };

  const handleKeyPress = (e) => {
    if (e.ctrlKey && e.key === 'Enter') {
      analyzeSentiment();
    }
  };

  const clearAll = () => {
    setReview('');
    setResult(null);
    setError(null);
  };

  return (
    <div className="analyzer">
      {/* Model Status Card */}
      {!modelReady && (
        <div className="card status-card">
          <div className="status-icon">⚠️</div>
          <h2>Model Not Ready</h2>
          <p>Train the sentiment analysis model before you can analyze reviews.</p>
          <button onClick={trainModel} disabled={loading} className="btn-primary btn-large">
            {loading ? (
              <>
                <span className="spinner"></span>
                Training Model...
              </>
            ) : (
              'Train Model'
            )}
          </button>
          <p className="hint">This will take about 30-60 seconds</p>
        </div>
      )}

      {/* Main Interface */}
      {modelReady && (
        <>
          {/* Input Section */}
          <div className="card input-card">
            <div className="card-header">
              <h2>📝 Analyze Movie Review</h2>
              <div className="status-badge">
                <span className="status-dot"></span>
                Model Ready
              </div>
            </div>

            <textarea
              value={review}
              onChange={(e) => setReview(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Enter a movie review here...

Example: 'This movie was absolutely fantastic! The acting was superb and the plot kept me engaged throughout.'"
              rows="5"
              maxLength="1000"
              className={review.length > 900 ? 'warning' : ''}
            />

            <div className="input-footer">
              <span className={`char-count ${review.length > 900 ? 'warning' : ''}`}>
                {review.length}/1000 characters
              </span>
              <span className="hint">Press Ctrl+Enter to analyze</span>
            </div>

            <div className="button-group">
              <button
                onClick={analyzeSentiment}
                disabled={loading || !review.trim()}
                className="btn-primary"
              >
                {loading ? (
                  <>
                    <span className="spinner"></span>
                    Analyzing...
                  </>
                ) : (
                  <>
                    <span>🔍</span>
                    Analyze Sentiment
                  </>
                )}
              </button>
              <button onClick={clearAll} className="btn-secondary">
                Clear
              </button>
            </div>

            {error && <div className="error-message">⚠️ {error}</div>}
          </div>

          {/* Results Section */}
          {result && (
            <div className="card results-card animate-fadeIn">
              <div className="card-header">
                <h2>📊 Analysis Results</h2>
              </div>

              <div className="metrics-grid">
                <div className="metric-card sentiment">
                  <div className="metric-icon">{result.sentiment === 'positive' ? '😊' : '😞'}</div>
                  <div className="metric-value">{result.sentiment.toUpperCase()}</div>
                  <div className="metric-label">Sentiment</div>
                </div>

                <div className="metric-card confidence">
                  <div className="metric-icon">🎯</div>
                  <div className="metric-value">
                    {Math.max(result.confidence.positive, result.confidence.negative).toFixed(1)}%
                  </div>
                  <div className="metric-label">Confidence</div>
                </div>

                <div className="metric-card words">
                  <div className="metric-icon">📝</div>
                  <div className="metric-value">{review.split(/\s+/).filter(w => w).length}</div>
                  <div className="metric-label">Words</div>
                </div>
              </div>

              <div className="confidence-breakdown">
                <h3>Confidence Breakdown</h3>
                <div className="confidence-bar-container">
                  <div className="confidence-label">
                    <span>😊 Positive</span>
                    <span className="percentage">{result.confidence.positive.toFixed(1)}%</span>
                  </div>
                  <div className="confidence-bar">
                    <div
                      className="confidence-fill positive"
                      style={{ width: `${result.confidence.positive}%` }}
                    ></div>
                  </div>
                </div>
                <div className="confidence-bar-container">
                  <div className="confidence-label">
                    <span>😞 Negative</span>
                    <span className="percentage">{result.confidence.negative.toFixed(1)}%</span>
                  </div>
                  <div className="confidence-bar">
                    <div
                      className="confidence-fill negative"
                      style={{ width: `${result.confidence.negative}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Examples Section */}
          <div className="card examples-card">
            <div className="card-header">
              <h2>💡 Try These Examples</h2>
            </div>

            <div className="examples-section">
              <div className="example-category">
                <h3 className="example-title positive">😊 Positive Reviews</h3>
                <div className="example-list">
                  {exampleReviews.positive.map((text, idx) => (
                    <button
                      key={idx}
                      onClick={() => loadExample(text)}
                      className="example-button"
                    >
                      <span className="example-icon">➤</span>
                      {text.substring(0, 80)}...
                    </button>
                  ))}
                </div>
              </div>

              <div className="example-category">
                <h3 className="example-title negative">😞 Negative Reviews</h3>
                <div className="example-list">
                  {exampleReviews.negative.map((text, idx) => (
                    <button
                      key={idx}
                      onClick={() => loadExample(text)}
                      className="example-button"
                    >
                      <span className="example-icon">➤</span>
                      {text.substring(0, 80)}...
                    </button>
                  ))}
                </div>
              </div>

              <div className="example-category">
                <h3 className="example-title neutral">😐 Neutral Reviews</h3>
                <div className="example-list">
                  {exampleReviews.neutral.map((text, idx) => (
                    <button
                      key={idx}
                      onClick={() => loadExample(text)}
                      className="example-button"
                    >
                      <span className="example-icon">➤</span>
                      {text.substring(0, 80)}...
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default SentimentAnalyzer;

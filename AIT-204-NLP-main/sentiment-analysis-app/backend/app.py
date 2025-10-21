from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import pickle
from sentiment_model import SentimentModel

app = Flask(__name__)
CORS(app)

model = SentimentModel()
MODEL_FILE = 'model.pkl'

# Load model if exists
if os.path.exists(MODEL_FILE):
    model.load_model(MODEL_FILE)


HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sentiment Analysis App</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 600px;
            width: 100%;
        }
        h1 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
        }
        .status {
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            font-weight: 600;
        }
        .status.ready {
            background: #d4edda;
            color: #155724;
        }
        .status.not-ready {
            background: #fff3cd;
            color: #856404;
        }
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            margin-bottom: 20px;
            transition: all 0.3s;
        }
        button:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            font-family: inherit;
            resize: vertical;
            min-height: 120px;
            margin-bottom: 15px;
            transition: border-color 0.3s;
        }
        textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        .result {
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            font-size: 18px;
            text-align: center;
            font-weight: 600;
        }
        .result.positive {
            background: #d4edda;
            color: #155724;
        }
        .result.negative {
            background: #f8d7da;
            color: #721c24;
        }
        .confidence {
            margin-top: 10px;
            font-size: 14px;
            opacity: 0.8;
        }
        .loading {
            display: none;
            text-align: center;
            color: #667eea;
            margin: 20px 0;
        }
        .loading.active {
            display: block;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Sentiment Analysis</h1>
        <p class="subtitle">Analyze movie review sentiment using NLP</p>

        <div id="status" class="status not-ready">
            Model Status: Not Trained
        </div>

        <button id="trainBtn" onclick="trainModel()">Train Model</button>

        <textarea id="reviewInput" placeholder="Enter a movie review here...

Example: 'This movie was absolutely fantastic! The acting was superb and the plot kept me engaged throughout.'"></textarea>

        <button id="analyzeBtn" onclick="analyzeSentiment()" disabled>Analyze Sentiment</button>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Processing...</p>
        </div>

        <div id="result"></div>
    </div>

    <script>
        let modelReady = false;

        async function checkStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                modelReady = data.status === 'ready';
                updateStatus();
            } catch (error) {
                console.error('Error checking status:', error);
            }
        }

        function updateStatus() {
            const statusDiv = document.getElementById('status');
            const analyzeBtn = document.getElementById('analyzeBtn');

            if (modelReady) {
                statusDiv.className = 'status ready';
                statusDiv.textContent = 'Model Status: Ready';
                analyzeBtn.disabled = false;
            } else {
                statusDiv.className = 'status not-ready';
                statusDiv.textContent = 'Model Status: Not Trained - Click "Train Model" to begin';
                analyzeBtn.disabled = true;
            }
        }

        async function trainModel() {
            const trainBtn = document.getElementById('trainBtn');
            const loading = document.getElementById('loading');

            trainBtn.disabled = true;
            trainBtn.textContent = 'Training...';
            loading.classList.add('active');

            try {
                const response = await fetch('/api/train', {
                    method: 'POST'
                });
                const data = await response.json();

                if (data.accuracy) {
                    alert(`Model trained successfully!\\nAccuracy: ${(data.accuracy * 100).toFixed(2)}%`);
                    modelReady = true;
                    updateStatus();
                } else {
                    alert('Error training model: ' + (data.error || 'Unknown error'));
                }
            } catch (error) {
                alert('Error training model: ' + error.message);
            } finally {
                trainBtn.disabled = false;
                trainBtn.textContent = 'Train Model';
                loading.classList.remove('active');
            }
        }

        async function analyzeSentiment() {
            const review = document.getElementById('reviewInput').value.trim();
            const resultDiv = document.getElementById('result');
            const loading = document.getElementById('loading');

            if (!review) {
                alert('Please enter a review to analyze');
                return;
            }

            loading.classList.add('active');
            resultDiv.innerHTML = '';

            try {
                const response = await fetch('/api/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ review: review })
                });

                const data = await response.json();

                if (data.error) {
                    alert('Error: ' + data.error);
                } else {
                    const sentiment = data.sentiment.toLowerCase();
                    const confidence = (data.confidence * 100).toFixed(2);

                    resultDiv.className = `result ${sentiment}`;
                    resultDiv.innerHTML = `
                        <div style="font-size: 24px;">Sentiment: ${data.sentiment}</div>
                        <div class="confidence">Confidence: ${confidence}%</div>
                    `;
                }
            } catch (error) {
                alert('Error analyzing sentiment: ' + error.message);
            } finally {
                loading.classList.remove('active');
            }
        }

        // Check status on page load
        checkStatus();
    </script>
</body>
</html>
'''


@app.route('/')
def home():
    """Serve the web interface"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/status', methods=['GET'])
def status():
    """Check if model is ready"""
    return jsonify({'status': 'ready' if model.is_trained() else 'not_trained'})


@app.route('/api/train', methods=['POST'])
def train():
    """Train the model"""
    try:
        accuracy = model.train()
        model.save_model(MODEL_FILE)
        return jsonify({'accuracy': accuracy, 'status': 'ready'})
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Training error: {error_details}")
        return jsonify({'error': str(e), 'details': error_details}), 500


@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict sentiment"""
    try:
        review = request.json.get('review', '')
        if not review:
            return jsonify({'error': 'No review provided'}), 400

        if not model.is_trained():
            return jsonify({'error': 'Model not trained'}), 400

        result = model.predict(review)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print('Server running on http://localhost:5000')
    app.run(debug=True, port=5000)

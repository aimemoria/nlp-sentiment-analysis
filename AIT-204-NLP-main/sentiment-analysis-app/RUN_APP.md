# How to Run the Sentiment Analysis App

## Method 1: Using Batch Files (Easiest - Windows)

### Step 1: Start Backend
1. Double-click `START_BACKEND.bat`
2. Wait for "Server running on http://localhost:5000"
3. Leave this window open

### Step 2: Start Frontend
1. Double-click `START_FRONTEND.bat`
2. Wait for npm to install (first time only)
3. Browser opens automatically at http://localhost:3000

## Method 2: Manual Commands

### Terminal 1 - Backend
```bash
cd "F:\PROJECTS\CST 435\WEEK 7\PROJECT\AIT-204-NLP-main\sentiment-analysis-app\backend"
pip install -r requirements.txt
python app.py
```

### Terminal 2 - Frontend
```bash
cd "F:\PROJECTS\CST 435\WEEK 7\PROJECT\AIT-204-NLP-main\sentiment-analysis-app\frontend"
npm install
npm start
```

## What Happens

1. **Backend** starts on http://localhost:5000
2. **Frontend** opens browser at http://localhost:3000
3. Click "Train Model" button
4. Enter a movie review
5. Click "Analyze" to see sentiment

## Troubleshooting

### Backend won't start
- Check Python is installed: `python --version`
- Try: `pip install flask flask-cors pandas scikit-learn nltk beautifulsoup4`

### Frontend won't start
- Check Node.js is installed: `node --version`
- Delete `node_modules` folder and `package-lock.json`
- Run `npm install` again

### Can't connect
- Make sure BOTH backend and frontend are running
- Backend must be on port 5000
- Frontend must be on port 3000

## To Stop

- Press `Ctrl+C` in both terminal windows
- Or close both Command Prompt windows

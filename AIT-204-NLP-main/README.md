# Sentiment Analysis: IMDB Movie Reviews

A comprehensive sentiment analysis project that classifies movie reviews as positive or negative using Natural Language Processing (NLP) and Machine Learning techniques.

## Overview

This project demonstrates a complete sentiment analysis workflow using the IMDB Movie Reviews Dataset. It implements text preprocessing, feature extraction with TF-IDF, and binary classification using Logistic Regression to achieve ~89% accuracy in sentiment prediction.

## Dataset

**IMDB Movie Reviews Dataset**
- 50,000 movie reviews from IMDB
- Binary classification: Positive (25,000) and Negative (25,000)
- Source: https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews

**Note**: Download the dataset and place `IMDB Dataset.csv` in the project root directory. If the file is not found, the notebook will create a sample dataset for demonstration.

## Installation

1. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

Required packages:
- numpy
- pandas
- matplotlib
- seaborn
- beautifulsoup4
- nltk
- scikit-learn

## Usage

Open and run the Jupyter notebook:

```bash
jupyter notebook Sentiment_Analysis_Assignment.ipynb
```

Or use Jupyter Lab:

```bash
jupyter lab Sentiment_Analysis_Assignment.ipynb
```

**To run the complete analysis:**
- Click `Cell → Run All` (or `Kernel → Restart & Run All`)
- The analysis takes approximately 2-5 minutes to complete
- All visualizations and results will be generated automatically

## Project Structure

```
├── Sentiment_Analysis_Assignment.ipynb  # Main assignment notebook
├── requirements.txt                     # Python dependencies
└── README.md                            # This file
```

## Methodology

### 1. Data Preprocessing
- HTML tag removal with BeautifulSoup
- Text normalization (lowercase conversion)
- Punctuation removal
- Stop word removal (NLTK)
- Lemmatization
- Tokenization

### 2. Feature Extraction
- **TF-IDF Vectorization**: Converts text to numerical features by assigning sentiment scores to words based on their importance

### 3. Model Training
- **Algorithm**: Logistic Regression (binary classification)
- **Train-Test Split**: 80% training, 20% testing
- **Performance**: ~89% accuracy on test set

### 4. Evaluation
- Confusion Matrix
- Performance Metrics: Accuracy, Precision, Recall, F1-Score
- Feature Importance Analysis
- Prediction confidence scores

## Results

The model achieves:
- **Accuracy**: 89.45%
- **Precision**: 88.68%
- **Recall**: 90.44%
- **F1-Score**: 89.55%

## Notebook Contents

The Jupyter notebook includes:

1. **Problem Statement**: Background, objectives, and research questions
2. **Algorithm of the Solution**: Detailed step-by-step methodology
3. **Implementation**: Complete code with comments
   - Data loading and exploration
   - Descriptive statistics
   - Missing value handling
   - Text preprocessing
   - TF-IDF vectorization
   - Model training and evaluation
   - Predictions on new text samples
   - Confusion matrix and performance metrics
4. **Analysis of Findings**: Comprehensive discussion of results, strengths, limitations, and recommendations
5. **References**: Academic sources and documentation

## Key Features

- Multiple visualizations (9+ plots)
- Sentiment distribution analysis
- Word count and review length statistics
- Confusion matrix heatmap
- Performance metrics charts
- Feature importance (top positive/negative words)
- Prediction confidence scores
- Professional academic writing throughout

## Example Predictions

```python
# Sample reviews
"This movie was absolutely amazing! I loved every second of it."
→ Predicted: POSITIVE (97.50% confidence)

"Terrible film. Complete waste of time and money."
→ Predicted: NEGATIVE (99.98% confidence)
```

## Requirements

- Python 3.7+
- Jupyter Notebook or JupyterLab
- 4GB+ RAM recommended
- Internet connection (for initial NLTK downloads)

## Notes

- The notebook handles missing data automatically
- NLTK data packages are downloaded automatically on first run
- All outputs and visualizations are included in the notebook
- Code is fully commented for clarity

## License

This project is for educational purposes. The IMDB dataset is publicly available for research and educational use.

---

**Ready for submission after running all cells!**

# HealthAI — Diabetes Risk Prediction

A full-stack machine learning project that predicts diabetes risk using the Pima Indians Diabetes dataset.
This project demonstrates end-to-end development including data preprocessing, model training, Flask API deployment, SQLite storage, and an interactive analytics dashboard.

## Features
- Logistic Regression model with preprocessing pipeline
- Flask REST API for real-time predictions
- Interactive dashboard using HTML/CSS/JavaScript + Chart.js
- SQLite database for prediction history
- High-risk & low-risk prediction cards with probabilities

## Dataset
Pima Indians Diabetes Dataset (768 records, 8 clinical features + label).

## Tech Stack
### Machine Learning
- Python
- scikit-learn
- Logistic Regression
- StandardScaler Pipeline

### Backend
- Flask
- SQLite
- REST API

### Frontend
- HTML, CSS, JavaScript
- Chart.js

## How to Run
```bash
git clone https://github.com/agrim7070/python-project.git
cd python-project
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python train_model.py      # optional
python app.py
```

Open dashboard:
```
http://localhost:5000
```

## API Example
POST /api/predict
```json
{
  "glucose": 120,
  "bloodpressure": 70,
  "skinthickness": 22,
  "insulin": 100,
  "bmi": 28.5,
  "pedigree": 0.45,
  "age": 32
}
```

## Future Work
- Add SHAP explainability
- Train ensembles / neural nets
- Cloud deployment with authentication
- Mobile app development

## Repository
https://github.com/agrim7070/python-project.git

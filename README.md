# AI Health Diagnosis Assistant — Cutie Auto Edition

## How it works
- Run `python app.py` in VS Code.
- If a trained model isn't present, the app will attempt to download the Kaggle dataset (if you've configured kaggle.json).
- If Kaggle is not configured or internet is unavailable, the app will train using the bundled local CSV (offline-safe).
- After training, the app saves `models/model.pkl` and launches the web UI automatically.

## Run
```bash
python -m venv venv
source venv/bin/activate   # or venv\\Scripts\\activate on Windows
pip install -r requirements.txt
python app.py
```

Admin: admin / admin123

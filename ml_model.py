import joblib, os, numpy as np
MODEL_PATH = os.path.join('models','model.pkl')
class HealthModel:
    def __init__(self, model_path=MODEL_PATH):
        if not os.path.exists(model_path):
            raise FileNotFoundError('Model not found. Run training first')
        pkg = joblib.load(model_path)
        self.model = pkg['model']
        self.columns = pkg['columns']
    def predict(self, features_dict):
        arr = np.array([features_dict[c] for c in self.columns], dtype=float).reshape(1,-1)
        proba = float(self.model.predict_proba(arr)[0,1])
        pred = int(self.model.predict(arr)[0])
        return {'prediction': pred, 'probability': proba}

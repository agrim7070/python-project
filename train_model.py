from flask import Flask, render_template, request, redirect, url_for, session
import os
from utils.ml_model import HealthModel
from utils.db_helper import init_db, save_record, verify_user, register_user, get_stats
import webbrowser
from threading import Timer
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET','supersecretkey')

init_db()

MODEL_PATH = os.path.join('models','model.pkl')

# Auto-load model
try:
    model = HealthModel()
except Exception as e:
    print("Model load error:", e)
    model = None


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':

        if model is None:
            return render_template("index.html", error="Model not available")

        form = request.form
        name = form.get('name', 'Patient')

        # Parse features
        try:
            features = {
                'Glucose': float(form.get('glucose')),
                'BloodPressure': float(form.get('bloodpressure')),
                'SkinThickness': float(form.get('skinthickness')),
                'Insulin': float(form.get('insulin')),
                'BMI': float(form.get('bmi')),
                'DiabetesPedigreeFunction': float(form.get('pedigree')),
                'Age': float(form.get('age')),
            }
        except:
            return render_template('index.html', error="Invalid number input")

        # Predict
        res = model.predict(features)

        # Convert prediction into clean natural labels
        label = "Needs Attention" if res['prediction'] == 1 else "All Clear"

        # Save to DB
        record = {
            **features,
            'name': name,
            'diagnosis': label,
            'probability': res['probability'],
            'timestamp': datetime.utcnow().isoformat()
        }
        save_record(record)

        # Pass everything to result page
        return render_template(
            "result.html",
            name=name,
            result=label,
            glucose=features['Glucose'],
            bloodpressure=features['BloodPressure'],
            skinthickness=features['SkinThickness'],
            insulin=features['Insulin'],
            bmi=features['BMI'],
            pedigree=features['DiabetesPedigreeFunction'],
            age=features['Age'],
            timestamp=record['timestamp']
        )

    return render_template('index.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        user = verify_user(u, p)

        if user:
            session['user'] = user
            return redirect(url_for('admin') if user['is_admin'] else url_for('index'))

        return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')

        if register_user(u, p):
            return redirect(url_for('login'))

        return render_template('register.html', error="Registration failed")

    return render_template('register.html')


@app.route('/admin')
def admin():
    user = session.get('user')

    if not user or not user.get('is_admin'):
        return redirect(url_for('login'))

    stats = get_stats()
    return render_template('admin.html', stats=stats)


def open_browser():
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    Timer(1.2, open_browser).start()
    app.run(debug=True, use_reloader=False)

from flask import Flask, render_template, request, redirect, url_for, session
import os
from utils.ml_model import HealthModel
from utils.db_helper import init_db, save_record, verify_user, register_user, get_stats
import webbrowser
from threading import Timer

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'supersecretkey')

# Init DB
init_db()

# Auto-train if no model exists
MODEL_PATH = os.path.join('models', 'model.pkl')
if not os.path.exists(MODEL_PATH):
    print('Model not found — training now...')
    try:
        import train_model as tm
        tm.create_and_train()
    except Exception as e:
        print('Auto-training failed:', e)

# Load Model
try:
    model = HealthModel()
except Exception as e:
    model = None
    print('Model load error:', e)


# -----------------------------------------------------
# MAIN PAGE — SHOW FORM
# -----------------------------------------------------
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


# -----------------------------------------------------
# NEW ROUTE — PROCESS FORM & SHOW RESULT
# (This fixes your Not Found error)
# -----------------------------------------------------
@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return render_template('index.html', error="Model not available")

    form = request.form
    name = form.get('name', "Cutie Patient")

    # Read inputs safely
    try:
        features = {
            'Glucose': float(form.get('glucose', 100.0)),
            'BloodPressure': float(form.get('bloodpressure', 80.0)),
            'SkinThickness': float(form.get('skinthickness', 20.0)),
            'Insulin': float(form.get('insulin', 80.0)),
            'BMI': float(form.get('bmi', 25.0)),
            'DiabetesPedigreeFunction': float(form.get('pedigree', 0.5)),
            'Age': float(form.get('age', 30)),
        }
    except ValueError:
        return render_template('index.html', error="Please enter valid numbers")

    # Predict
    res = model.predict(features)
    label = "Positive" if res["prediction"] == 1 else "Negative"

    # Save to DB
    record = {
        **features,
        "name": name,
        "prediction": res["prediction"],
        "probability": res["probability"]
    }
    save_record(record)

    # Show result
    return render_template(
        "result.html",
        name=name,
        result=label,
        prob=round(res["probability"] * 100, 2)
    )


# -----------------------------------------------------
# LOGIN SYSTEM
# -----------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        user = verify_user(u, p)
        if user:
            session['user'] = user
            return redirect(url_for('admin') if user['is_admin'] else url_for('home'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        u = request.form.get('username')
        p = request.form.get('password')
        ok = register_user(u, p)
        if ok:
            return redirect(url_for('login'))
        return render_template('register.html', error="Registration failed")
    return render_template('register.html')


# -----------------------------------------------------
# ADMIN PAGE
# -----------------------------------------------------
@app.route('/admin')
def admin():
    user = session.get('user')
    if not user or not user.get('is_admin'):
        return redirect(url_for('login'))
    stats = get_stats()
    return render_template('admin.html', stats=stats)


# Auto-open browser
def open_browser():
    webbrowser.open('http://127.0.0.1:5000')


if __name__ == '__main__':
    Timer(1.2, open_browser).start()
    app.run(debug=True, use_reloader=False)

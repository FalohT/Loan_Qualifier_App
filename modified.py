from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from pathlib import Path
import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
import threading
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"

# Ensure the data directory exists and set absolute path for database
BASE_DIR = Path(__file__).parent  # Directory of app.py
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)  # Create data/ if it doesn’t exist
DB_PATH = DATA_DIR / "loan_data.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Cache
db = SQLAlchemy(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Database Models
class Applicant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    credit_score = db.Column(db.Integer)
    debt = db.Column(db.Float)
    income = db.Column(db.Float)
    loan_amount = db.Column(db.Float)
    home_value = db.Column(db.Float)
    risk_score = db.Column(db.Float)
    approval_status = db.Column(db.String)

class BankLoan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_size = db.Column(db.Float)
    credit_score_min = db.Column(db.Integer)
    debt_to_income_max = db.Column(db.Float)
    loan_to_value_max = db.Column(db.Float)

# Utility Functions
def calculate_monthly_payment(loan_amount, interest_rate, term):
    """Calculate monthly payment based on loan amount, interest rate (%), and term (years)."""
    monthly_rate = interest_rate / 100 / 12
    num_payments = term * 12
    if monthly_rate == 0:
        return loan_amount / num_payments
    return loan_amount * monthly_rate * (1 + monthly_rate)**num_payments / ((1 + monthly_rate)**num_payments - 1)

def estimate_interest_rate(credit_score, loan_amount):
    """Estimate interest rate based on credit score and loan amount."""
    if credit_score >= 750:
        return 3.5
    elif credit_score >= 650:
        return 4.0
    else:
        return 5.0

def calculate_monthly_debt_ratio(debt, income):
    """Calculate monthly debt-to-income ratio."""
    return debt / income if income > 0 else float('inf')

def calculate_loan_to_value_ratio(loan_amount, home_value):
    """Calculate loan-to-value ratio."""
    return loan_amount / home_value if home_value > 0 else float('inf')

def calculate_risk_score(credit_score, monthly_debt_ratio, loan_to_value_ratio):
    """Calculate risk score."""
    risk_score = (
        (credit_score / 850) * 40 +
        (1 - monthly_debt_ratio) * 30 +
        (1 - loan_to_value_ratio) * 30
    )
    return round(risk_score, 2)

@cache.cached(timeout=300)  # Cache for 5 minutes
def load_bank_data(file_path):
    """Load bank data from CSV, Excel, or JSON with validation."""
    try:
        ext = Path(file_path).suffix.lower()
        if ext == '.csv':
            df = pd.read_csv(file_path)
        elif ext == '.xlsx':
            df = pd.read_excel(file_path)
        elif ext == '.json':
            df = pd.read_json(file_path)
        else:
            print(f"Error: Unsupported file format {ext}")
            return []
        
        required_cols = ['loan_size', 'credit_score_min', 'debt_to_income_max', 'loan_to_value_max']
        if not all(col in df.columns for col in required_cols):
            print(f"Error: Missing required columns in {file_path}")
            return []
        
        # Save to database if not already populated
        if not BankLoan.query.first():
            with app.app_context():
                for _, row in df.iterrows():
                    loan = BankLoan(
                        loan_size=row['loan_size'],
                        credit_score_min=row['credit_score_min'],
                        debt_to_income_max=row['debt_to_income_max'],
                        loan_to_value_max=row['loan_to_value_max']
                    )
                    db.session.add(loan)
                db.session.commit()
        
        return BankLoan.query.all()
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return []

# Filter Functions (Multithreaded)
def filter_loans(loan_amount, credit_score, monthly_debt_ratio, loan_to_value_ratio, bank_loans):
    """Filter loans using multithreading."""
    results = []
    threads = []

    def filter_task(loan):
        if (loan.loan_size >= loan_amount and
            loan.credit_score_min <= credit_score and
            loan.debt_to_income_max >= monthly_debt_ratio and
            loan.loan_to_value_max >= loan_to_value_ratio):
            results.append(loan)

    for loan in bank_loans:
        t = threading.Thread(target=filter_task, args=(loan,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return results

# Machine Learning Training
def train_ml_model():
    """Train or load ML model."""
    model_path = BASE_DIR / "models" / "loan_approval.pkl"
    model_dir = BASE_DIR / "models"
    model_dir.mkdir(exist_ok=True)
    if not model_path.exists():
        X = pd.DataFrame([
            [700, 500, 2000, 150000, 200000],
            [500, 1000, 1500, 200000, 250000],
            [800, 300, 2500, 100000, 150000]
        ], columns=['credit_score', 'debt', 'income', 'loan_amount', 'home_value'])
        y = [1, 0, 1]
        model = LogisticRegression()
        model.fit(X, y)
        joblib.dump(model, model_path)
    return joblib.load(model_path)

ML_MODEL = train_ml_model()

# Flask Route
@app.route("/", methods=["GET", "POST"])
def index():
    with app.app_context():
        db.create_all()  # Ensure tables exist
        
    if request.method == "POST":
        try:
            # Get form data
            credit_score = int(request.form["credit_score"])
            debt = float(request.form["debt"])
            income = float(request.form["income"])
            loan_amount = float(request.form["loan_amount"])
            home_value = float(request.form["home_value"])
            term = int(request.form["term"])

            # Load bank data
            bank_loans = load_bank_data(BASE_DIR / "data" / "rate_sheet.csv")

            # Calculate financial metrics
            monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
            loan_to_value_ratio = calculate_loan_to_value_ratio(loan_amount, home_value)
            interest_rate = estimate_interest_rate(credit_score, loan_amount)
            monthly_payment = calculate_monthly_payment(loan_amount, interest_rate, term)
            risk_score = calculate_risk_score(credit_score, monthly_debt_ratio, loan_to_value_ratio)

            # Filter loans
            qualifying_loans = filter_loans(loan_amount, credit_score, monthly_debt_ratio, loan_to_value_ratio, bank_loans)

            # Predict approval
            applicant_data = [[credit_score, debt, income, loan_amount, home_value]]
            approval_status = ML_MODEL.predict(applicant_data)[0]

            # Save applicant data
            with app.app_context():
                applicant = Applicant(
                    credit_score=credit_score, debt=debt, income=income,
                    loan_amount=loan_amount, home_value=home_value,
                    risk_score=risk_score, approval_status=str(approval_status)
                )
                db.session.add(applicant)
                db.session.commit()

            # Render results
            return render_template(
                "index.html",
                qualifying_loans=qualifying_loans,
                risk_score=risk_score,
                approval_status="Approved" if approval_status == 1 else "Denied",
                monthly_payment=monthly_payment,
                interest_rate=interest_rate
            )
        except KeyError as e:
            return f"Error: Missing form field {e}", 400
        except ValueError as e:
            return f"Error: Invalid input {e}", 400
        except Exception as e:
            return f"Error: {e}", 500

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
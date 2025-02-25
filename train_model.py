from sklearn.ensemble import RandomForestClassifier
import joblib

# Example: Train a simple model
X = [[700, 1500, 5000, 200000, 300000]]  # Example data
y = [1]  # Example label (1 = approved, 0 = denied)

# Create and train the model
model = RandomForestClassifier()
model.fit(X, y)

# Save the model
joblib.dump(model, "models/loan_approval.pkl")
print("Model trained and saved to 'models/loan_approval.pkl'")

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load the Iris dataset
X, y = load_iris(return_X_y=True)

# Train the machine learning model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Save the trained model
joblib.dump(model, "lab8/model.pkl")

print("Model saved successfully!")

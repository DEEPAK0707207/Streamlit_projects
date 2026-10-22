
import pandas as pd
import joblib

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error


# Load student data
df = pd.read_csv("data/students.csv")

# Features used to predict marks
X = df[["attendance", "study_hours"]]
y = df["marks"]

# Split data for training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)

print("Model training completed!")
print(f"Mean Absolute Error: {mae:.2f}")

# Save the trained model
joblib.dump(model, "model.pkl")

print("Model saved as model.pkl")

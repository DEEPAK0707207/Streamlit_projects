
# Student AI Dashboard

A full-stack student dashboard built using Python and Streamlit.

## Features

- PostgreSQL login and signup
- Password hashing using bcrypt
- Home page with KPI cards
- Student data dashboard with CSV upload, filters, and charts
- Machine learning marks prediction
- Chatbot interface with conversation history
- External API integration and JSON display
- Admin panel for registered users

## Technologies Used

- Python
- Streamlit
- PostgreSQL (Neon)
- Pandas and NumPy
- Scikit-learn
- Joblib
- Requests
- Bcrypt

## Run Locally

1. Install Python.
2. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Create `.streamlit/secrets.toml` and add your Neon connection string:

   ```toml
   DATABASE_URL = "YOUR_NEON_CONNECTION_STRING"
   ```

4. Train the machine learning model:

   ```bash
   python train_model.py
   ```

5. Start the dashboard:

   ```bash
   python -m streamlit run app.py
   ```

## Security

Never commit database credentials or other secrets to GitHub.

## Note

The chatbot currently uses demo responses. The ML model is trained on a small sample dataset and is intended for educational purposes.

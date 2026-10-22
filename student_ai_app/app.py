
import streamlit as st
import pandas as pd
import requests
import joblib
import bcrypt

from pathlib import Path
from db import init_db, create_user, get_user_by_username, get_all_users


# --------------------------------------------------
# APP SETTINGS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "students.csv"
MODEL_PATH = BASE_DIR / "model.pkl"

st.set_page_config(
    page_title="Student AI Dashboard",
    page_icon="🎓",
    layout="wide"
)


# --------------------------------------------------
# DATABASE AND SESSION SETUP
# --------------------------------------------------

@st.cache_resource
def initialize_database():
    init_db()
    return True


try:
    initialize_database()
except Exception as error:
    st.error("Could not connect to the database.")
    st.info(
        "Check your DATABASE_URL in .streamlit/secrets.toml "
        "and confirm that your database is available."
    )
    st.stop()


if "user" not in st.session_state:
    st.session_state.user = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

if "locked" not in st.session_state:
    st.session_state.locked = False


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def hash_password(password):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(password, password_hash):
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8")
        )
    except (ValueError, TypeError, AttributeError):
        return False


def load_student_data():
    if not DATA_PATH.exists():
        st.error(f"Student CSV file not found: {DATA_PATH}")
        return pd.DataFrame()

    return pd.read_csv(DATA_PATH)


def load_prediction_model():
    if not MODEL_PATH.exists():
        st.warning(
            "Model file not found. Run `python train_model.py` "
            "from the student_ai_app folder."
        )
        return None

    try:
        return joblib.load(MODEL_PATH)
    except Exception as error:
        st.error(f"Could not load model: {error}")
        return None


# --------------------------------------------------
# LOGIN AND SIGNUP
# --------------------------------------------------

def show_authentication():
    st.title("🎓 Student AI Dashboard")
    st.write("Login or create an account to continue.")

    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

    with login_tab:
        st.subheader("Login")

        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input(
                "Password",
                type="password"
            )
            login_clicked = st.form_submit_button(
                "Login",
                use_container_width=True
            )

        if login_clicked:
            if st.session_state.locked:
                st.error(
                    "Too many failed attempts. Refreshing this demo "
                    "session is not a secure account lockout system."
                )
            elif not username.strip() or not password:
                st.warning("Enter both username and password.")
            else:
                try:
                    user = get_user_by_username(username.strip())

                    if user and verify_password(
                        password, user["password_hash"]
                    ):
                        st.session_state.user = dict(user)
                        st.session_state.failed_attempts = 0
                        st.rerun()
                    else:
                        st.session_state.failed_attempts += 1
                        remaining = (
                            3 - st.session_state.failed_attempts
                        )

                        if remaining > 0:
                            st.error(
                                "Incorrect username or password. "
                                f"Attempts remaining: {remaining}"
                            )
                        else:
                            st.session_state.locked = True
                            st.error(
                                "Too many failed attempts in this "
                                "session. Please restart the demo."
                            )
                except Exception as error:
                    st.error(f"Login failed: {error}")

    with signup_tab:
        st.subheader("Create Account")

        with st.form("signup_form"):
            new_username = st.text_input("Choose a username")
            new_email = st.text_input("Email address")
            new_password = st.text_input(
                "Choose a password",
                type="password"
            )
            confirm_password = st.text_input(
                "Confirm password",
                type="password"
            )
            signup_clicked = st.form_submit_button(
                "Create Account",
                use_container_width=True
            )

        if signup_clicked:
            username = new_username.strip()
            email = new_email.strip().lower()

            if not username or not email or not new_password:
                st.warning("Please fill in every field.")
            elif "@" not in email or "." not in email.split("@")[-1]:
                st.warning("Enter a valid email address.")
            elif len(username) < 3:
                st.warning("Username must contain at least 3 characters.")
            elif len(new_password) < 8:
                st.warning("Password must contain at least 8 characters.")
            elif new_password != confirm_password:
                st.warning("Passwords do not match.")
            else:
                try:
                    password_hash = hash_password(new_password)
                    create_user(username, email, password_hash)

                    st.success(
                        "Account created successfully! "
                        "You can now log in."
                    )
                except Exception:
                    st.error(
                        "Could not create the account. "
                        "The username or email may already exist."
                    )


# --------------------------------------------------
# HOME
# --------------------------------------------------

def show_home():
    st.title("🏠 Home")
    st.write(
        f"Welcome, **{st.session_state.user['username']}**!"
    )

    df = load_student_data()

    if df.empty:
        st.info("Add student records to data/students.csv.")
        return

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Students", len(df))

    if "cgpa" in df.columns:
        col2.metric("Average CGPA", f"{df['cgpa'].mean():.2f}")

    if "attendance" in df.columns:
        col3.metric(
            "Average Attendance",
            f"{df['attendance'].mean():.1f}%"
        )

    if "marks" in df.columns:
        col4.metric("Average Marks", f"{df['marks'].mean():.1f}")

    st.subheader("About This Project")
    st.write(
        "This dashboard combines student data analysis, "
        "machine-learning predictions, a chatbot interface, "
        "an external API demonstration, and account management."
    )


# --------------------------------------------------
# DATA DASHBOARD
# --------------------------------------------------

def show_data_dashboard():
    st.title("📊 Data Dashboard")

    uploaded_file = st.file_uploader(
        "Upload a student CSV file (optional)",
        type=["csv"]
    )

    try:
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
        else:
            df = load_student_data()
    except Exception as error:
        st.error(f"Could not read the CSV file: {error}")
        return

    if df.empty:
        st.info("No student data available.")
        return

    required_columns = [
        "student_id",
        "name",
        "branch",
        "year",
        "attendance",
        "marks",
        "cgpa"
    ]

    missing = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing:
        st.error(
            "The CSV is missing these required columns: "
            + ", ".join(missing)
        )
        return

    st.subheader("Filter Students")

    col1, col2 = st.columns(2)

    branches = sorted(df["branch"].dropna().astype(str).unique())
    selected_branches = col1.multiselect(
        "Select branch",
        branches,
        default=branches
    )

    years = sorted(pd.to_numeric(
        df["year"], errors="coerce"
    ).dropna().unique())

    selected_years = col2.multiselect(
        "Select year",
        years,
        default=years
    )

    filtered_df = df[
        df["branch"].astype(str).isin(selected_branches)
        & pd.to_numeric(
            df["year"], errors="coerce"
        ).isin(selected_years)
    ].copy()

    st.subheader("Student Records")
    st.dataframe(filtered_df, use_container_width=True)

    st.download_button(
        "Download Filtered CSV",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_students.csv",
        mime="text/csv"
    )

    if filtered_df.empty:
        st.info("No students match the selected filters.")
        return

    st.subheader("Average Marks by Branch")
    marks_by_branch = filtered_df.groupby("branch")["marks"].mean()
    st.bar_chart(marks_by_branch)

    st.subheader("Attendance and Marks")
    st.line_chart(
        filtered_df.set_index("name")[["attendance", "marks"]]
    )

    st.subheader("CGPA Distribution")
    st.bar_chart(filtered_df["cgpa"].value_counts().sort_index())


# --------------------------------------------------
# MACHINE LEARNING PREDICTION
# --------------------------------------------------

def show_prediction():
    st.title("🤖 Student Marks Prediction")
    st.write(
        "Enter attendance and study hours to estimate marks "
        "using the trained model."
    )

    attendance = st.slider(
        "Attendance (%)",
        min_value=0,
        max_value=100,
        value=85
    )

    study_hours = st.slider(
        "Study hours per day",
        min_value=0,
        max_value=12,
        value=5
    )

    if st.button("Predict Marks"):
        model = load_prediction_model()

        if model is not None:
            try:
                input_data = pd.DataFrame(
                    [[attendance, study_hours]],
                    columns=["attendance", "study_hours"]
                )

                prediction = float(model.predict(input_data)[0])
                prediction = max(0.0, min(100.0, prediction))

                st.success(
                    f"Estimated marks: {prediction:.2f} / 100"
                )
                st.caption(
                    "This is a demonstration model trained on a small "
                    "sample dataset. It is not a reliable academic "
                    "assessment or guarantee of actual marks."
                )
            except Exception as error:
                st.error(f"Prediction failed: {error}")


# --------------------------------------------------
# AI CHATBOT DEMO
# --------------------------------------------------

def show_chatbot():
    st.title("💬 AI Chatbot")
    st.write(
        "This is a basic chatbot interface. Its replies are "
        "demonstration responses, not generated by a real AI model."
    )

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input("Ask a question about this dashboard...")

    if prompt:
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })

        answer = (
            "Thanks for your question! This is currently a demo "
            "chatbot and does not connect to a real AI service. "
            "You asked: " + prompt
        )

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer
        })

        st.rerun()

    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()


# --------------------------------------------------
# API DEMO - UPDATED
# --------------------------------------------------

def show_api_demo():
    st.title("🌐 API Demo")
    st.write(
        "Fetch sample post data from an external API and view "
        "the returned JSON response."
    )

    post_id = st.number_input(
        "Enter Post ID (1–100)",
        min_value=1,
        max_value=100,
        value=1,
        step=1
    )

    if st.button("Fetch API Data"):
        api_url = (
            "https://jsonplaceholder.typicode.com/posts/"
            f"{int(post_id)}"
        )

        try:
            with st.spinner("Connecting to the API..."):
                response = requests.get(api_url, timeout=20)

            if response.status_code == 200:
                data = response.json()

                if isinstance(data, dict) and data.get("id"):
                    st.success("API request successful!")

                    col1, col2 = st.columns(2)
                    col1.metric("Post ID", data.get("id", "N/A"))
                    col2.metric("User ID", data.get("userId", "N/A"))

                    st.subheader("Post Details")
                    st.write("**Title:**", data.get("title", "N/A"))
                    st.write("**Body:**", data.get("body", "N/A"))

                    with st.expander("View Raw JSON"):
                        st.json(data)
                else:
                    st.warning("The API returned an unexpected response.")
                    st.json(data)

            elif response.status_code == 404:
                st.error("Post not found. Enter an ID from 1 to 100.")

            else:
                st.error(
                    f"API returned HTTP status {response.status_code}."
                )
                st.code(response.text[:1000])

        except requests.exceptions.Timeout:
            st.error(
                "The API request timed out. Please try again."
            )

        except requests.exceptions.ConnectionError:
            st.error(
                "Could not connect to the API. Check your internet "
                "connection or try again later."
            )

        except requests.exceptions.RequestException as error:
            st.error(f"API request failed: {error}")

        except ValueError:
            st.error("The API response was not valid JSON.")


# --------------------------------------------------
# ADMIN PANEL
# --------------------------------------------------

def show_admin_panel():
    st.title("🔐 Admin Panel")

    current_user = st.session_state.user

    if current_user.get("role") != "admin":
        st.error("Access denied. Only admins can view this page.")
        return

    st.success("Admin access granted.")

    try:
        users = get_all_users()

        if not users:
            st.info("No registered users found.")
            return

        users_df = pd.DataFrame([dict(user) for user in users])

        # Never display password hashes in the admin table.
        if "password_hash" in users_df.columns:
            users_df = users_df.drop(columns=["password_hash"])

        st.subheader("Registered Users")
        st.dataframe(users_df, use_container_width=True)

        st.metric("Total Registered Users", len(users_df))

    except Exception as error:
        st.error(f"Could not load users: {error}")


# --------------------------------------------------
# MAIN APP NAVIGATION
# --------------------------------------------------

def main():
    if st.session_state.user is None:
        show_authentication()
        return

    user = st.session_state.user

    st.sidebar.title("🎓 Student AI Dashboard")
    st.sidebar.write(f"Logged in as: **{user['username']}**")
    st.sidebar.write(f"Role: **{user.get('role', 'user')}**")

    pages = [
        "Home",
        "Data Dashboard",
        "Predict",
        "AI Chatbot",
        "API Demo"
    ]

    if user.get("role") == "admin":
        pages.append("Admin Panel")

    page = st.sidebar.radio("Navigation", pages)

    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.user = None
        st.session_state.chat_history = []
        st.session_state.failed_attempts = 0
        st.session_state.locked = False
        st.rerun()

    # Every page is selected here, so `page` is always defined.
    if page == "Home":
        show_home()

    elif page == "Data Dashboard":
        show_data_dashboard()

    elif page == "Predict":
        show_prediction()

    elif page == "AI Chatbot":
        show_chatbot()

    elif page == "API Demo":
        show_api_demo()

    elif page == "Admin Panel":
        show_admin_panel()


if __name__ == "__main__":
    main()

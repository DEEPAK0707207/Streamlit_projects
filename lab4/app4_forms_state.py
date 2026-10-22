
import streamlit as st

st.set_page_config(page_title="Lab 4 - Forms and Session State")

st.title("Lab 4: Forms and Session State")
st.write("Learn forms and how to preserve values using session state.")

# Initialize session state
if "count" not in st.session_state:
    st.session_state.count = 0

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "todos" not in st.session_state:
    st.session_state.todos = []

# Counter buttons
st.subheader("1. Counter")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Increment"):
        st.session_state.count += 1

with col2:
    if st.button("Add 5"):
        st.session_state.count += 5

with col3:
    if st.button("Reset Counter"):
        st.session_state.count = 0

st.metric("Current Counter", st.session_state.count)

st.divider()

# Login form
st.subheader("2. Login Form")

with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

if submit:
    if username == "admin" and password == "1234":
        st.session_state.logged_in = True
        st.success("Login successful!")
    else:
        st.error("Invalid username or password.")

if st.session_state.logged_in:
    st.info("Welcome, admin! You are now logged in.")

st.caption("Demo login: username admin | password 1234")

st.divider()

# To-do list form
st.subheader("3. To-Do List")

with st.form("todo_form", clear_on_submit=True):
    task = st.text_input("Enter a new task")
    add_task = st.form_submit_button("Add Task")

if add_task:
    if task.strip():
        st.session_state.todos.append(task.strip())
        st.success("Task added successfully!")
    else:
        st.warning("Please enter a task.")

st.write("### Your Tasks")

if st.session_state.todos:
    for i, todo in enumerate(st.session_state.todos, start=1):
        st.write(f"{i}. {todo}")
else:
    st.write("No tasks added yet.")

if st.button("Clear All Tasks"):
    st.session_state.todos = []
    st.rerun()

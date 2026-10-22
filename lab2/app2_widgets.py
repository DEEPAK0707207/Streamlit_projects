
import streamlit as st

st.set_page_config(page_title="Widgets Playground", page_icon="🎮")

st.title("Lab 2: Widgets Playground")
st.write("Explore different Streamlit widgets.")

# Text input
name = st.text_input("Enter your name")

# Number input
age = st.number_input("Enter your age", min_value=1, max_value=100, value=18)

# Slider
marks = st.slider("Select your marks", 0, 100, 50)

# Select box
course = st.selectbox(
    "Choose your course",
    ["CSE", "AIML", "Data Science", "Cyber Security"]
)

# Radio buttons
gender = st.radio("Select your gender", ["Male", "Female", "Other"])

# Checkbox
agree = st.checkbox("I agree to the terms")

# Button
if st.button("Submit"):
    st.success("Details submitted successfully!")
    st.write("Name:", name)
    st.write("Age:", age)
    st.write("Marks:", marks)
    st.write("Course:", course)
    st.write("Gender:", gender)
    st.write("Agreed:", "Yes" if agree else "No")

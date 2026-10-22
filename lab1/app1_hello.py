
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Hello App",
    page_icon="👋",
    layout="centered"
)

# Headings
st.title("Hello Streamlit")
st.header("My First App")
st.subheader("Learning Basics")

# Text
st.write("Streamlit converts Python scripts into web apps.")
st.markdown("**Bold text**, *Italic text*, and `code` work here.")

# Messages
st.success("App loaded successfully!")
st.info("This is an info message.")
st.warning("This is a warning.")
st.error("This is an error.")

# User inputs
name = st.text_input("Enter your name")
age = st.number_input("Enter your age", min_value=1, max_value=100)

# Display sample data
st.write("### Sample Data")

st.table({
    "Name": ["A", "B"],
    "Marks": [85, 90]
})

# Display entered details
if name:
    st.write("Your name:", name)

st.write("Your age:", age)

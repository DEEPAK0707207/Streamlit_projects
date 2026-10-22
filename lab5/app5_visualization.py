
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Lab 5: Data Visualization")

# Generate sample data
df = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["Math", "Science", "English"]
)

# Display the data
st.subheader("Sample Data")
st.dataframe(df)

# Built-in charts
st.subheader("Line Chart")
st.line_chart(df)

st.subheader("Bar Chart")
st.bar_chart(df)

st.subheader("Area Chart")
st.area_chart(df)

# Matplotlib histogram
st.subheader("Matplotlib Chart")

fig, ax = plt.subplots()

ax.hist(df["Math"], bins=10, color="skyblue")
ax.set_title("Math Score Distribution")
ax.set_xlabel("Math Values")
ax.set_ylabel("Frequency")

st.pyplot(fig)

# Exercise: Scatter plot
st.subheader("Scatter Plot")
st.scatter_chart(df, x="Math", y="Science")

# Exercise: Mean metric
st.subheader("Average Math Value")
st.metric("Mean Math", f"{df['Math'].mean():.2f}")

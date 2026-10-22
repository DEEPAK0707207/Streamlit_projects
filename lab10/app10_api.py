
import streamlit as st
import requests

st.title("Weather API Demo")

city = st.text_input("Enter city", "Chennai")

if st.button("Get Weather"):
    # Simulated response from the guide
    resp = {
        "city": city,
        "temperature": 30,
        "condition": "Sunny",
        "humidity": 65
    }

    st.subheader("Weather Details")
    st.json(resp)

    c1, c2, c3 = st.columns(3)

    c1.metric("Temperature", f"{resp['temperature']} °C")
    c2.metric("Condition", resp["condition"])
    c3.metric("Humidity", f"{resp['humidity']}%")

st.markdown("---")
st.subheader("HTTP Methods")

st.markdown("""
- **GET** — Retrieve data
- **POST** — Send data
- **PUT** — Update data
- **DELETE** — Delete data
""")

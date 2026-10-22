
import streamlit as st

# Page title
st.title("Layouts Demo")

# Sidebar settings
st.sidebar.header("Settings")

theme = st.sidebar.selectbox(
    "Theme",
    ["Light", "Dark"]
)

font_size = st.sidebar.slider(
    "Font Size",
    10, 30, 15
)

st.sidebar.write("Selected theme:", theme)
st.sidebar.write("Font size:", font_size)

# Columns
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Sales", "25 Lakh")

with col2:
    st.metric("Customers", "1,200")

# Tabs
tab1, tab2, tab3 = st.tabs(
    ["Overview", "Analysis", "About"]
)

with tab1:
    st.subheader("Overview")
    st.write("Welcome to the dashboard overview.")

with tab2:
    st.subheader("Analysis")
    st.write("Here you can analyze business performance.")

with tab3:
    st.subheader("About")
    st.write("This application demonstrates Streamlit layouts.")

# Container
with st.container():
    st.subheader("Grouped Section")
    st.write("These elements are inside one container.")

# Expander exercise
with st.expander("Details"):
    st.write("This content appears when you expand this section.")

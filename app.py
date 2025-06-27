import streamlit as st
import hashlib
# import subprocess
# subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)

# Local module imports
try:
    from data_preview import data_preview
    from trend_analysis import trend_analysis
    from forecasting import forecast
    from model_accuracy import evaluate_model
except ModuleNotFoundError as e:
    st.error(f"Module import error: {e}")
    st.stop()

st.set_page_config(page_title="FLAVOUR FORECAST - Potato Chips Demand Forecasting Tool", layout="wide")

# Admin credentials
USERNAME = "admin"
PASSWORD_HASH = hashlib.sha256("adminpass".encode()).hexdigest()

# Function for login form
def login():
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username == USERNAME and hashlib.sha256(password.encode()).hexdigest() == PASSWORD_HASH:
            st.session_state.logged_in = True
            st.sidebar.success("Login successful!")
            st.experimental_rerun()
        else:
            st.sidebar.error("Invalid username or password.")

# Logout function
def logout():
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.sidebar.success("Logged out successfully.")
        st.experimental_rerun()

# Session check
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    st.sidebar.title(f"Welcome, {USERNAME}")
    logout()

    st.title("FLAVOUR FORECAST")
    st.subheader("Potato Chips Demand Forecasting Tool")

    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select a Section", ["Home", "Upload Data", "Analyze Data", "Forecast Data", "Model's Accuracy"])

    if page == "Home":
        st.markdown("### Welcome to FLAVOUR FORECAST!")
        st.write("Forecast demand for different potato chip flavors by analyzing key factors like events, promotions, holidays, and weather conditions.")

        st.markdown("#### Get Started:")
        menu_option = st.selectbox(
            "Choose an Action",
            [
                "Upload Data - Upload and preview your dataset to get started.",
                "Analyze Data - Explore historical trends and visualize how events, holidays, and other factors impact sales.",
                "Forecast Data - Use predictive modeling to forecast future demand or sales volume."
            ]
        )

        if menu_option.startswith("Upload Data") and st.button("Go to Upload Data"):
            st.session_state.page = "Upload Data"
            st.experimental_rerun()
        elif menu_option.startswith("Analyze Data") and st.button("Go to Analyze Data"):
            st.session_state.page = "Analyze Data"
            st.experimental_rerun()
        elif menu_option.startswith("Forecast Data") and st.button("Go to Forecast Data"):
            st.session_state.page = "Forecast Data"
            st.experimental_rerun()

    elif page == "Upload Data":
        st.header("Upload Your Dataset")
        st.write("Upload a dataset to begin analyzing trends and forecasting demand.")
        data = data_preview()
        if data is not None:
            st.session_state['data'] = data
            st.success("Data uploaded successfully!")
        else:
            st.warning("Please upload a valid dataset.")

    elif page == "Analyze Data":
        st.header("Data Analysis")
        st.write("Gain insights into historical trends, seasonality, and demand drivers.")
        if 'data' in st.session_state and st.session_state['data'] is not None:
            trend_analysis(st.session_state['data'])
        else:
            st.warning("Please upload a dataset in the 'Upload Data' section first.")

    elif page == "Forecast Data":
        st.header("Demand Forecasting")
        st.write("Predict future demand using historical data and influencing factors.")
        if 'data' in st.session_state and st.session_state['data'] is not None:
            forecast(st.session_state['data'])
        else:
            st.warning("Please upload a dataset in the 'Upload Data' section first.")

    elif page == "Model's Accuracy":
        st.header("Model's Accuracy Evaluation")
        if 'forecast_values' in st.session_state and 'test_data' in st.session_state:
            evaluate_model(st.session_state['forecast_values'], st.session_state['test_data'])
        else:
            st.warning("Please perform forecasting in the 'Forecast Data' section first.")

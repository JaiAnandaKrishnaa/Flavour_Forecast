import streamlit as st
import pandas as pd

def handle_missing_data(data):
    """Handle missing data by filling with appropriate methods."""
    st.markdown("<h4 style='color: #FF7F50;'>Handling Missing Data</h4>", unsafe_allow_html=True)
    
    # Fill missing values
    for column in data.columns:
        if data[column].dtype == "object":  # For categorical data, fill with mode
            data[column].fillna(data[column].mode()[0], inplace=True)
        else:  # For numerical data, fill with mean
            data[column].fillna(data[column].mean(), inplace=True)
    
    # Confirm the missing data has been handled
    st.success("Missing data handled successfully!")
    return data

def data_preview():
    # Title with styling
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>FLAVOUR FORECAST - Data Upload</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Upload and Preview Your Dataset</h4>", unsafe_allow_html=True)
    st.write("---")
    
    # Step 1: Uploading the file
    st.markdown("<h4 style='color: #FF7F50;'>Step 1: Upload Your Dataset</h4>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload your dataset (Excel file - .xlsx)", type=["xlsx"])
    
    if uploaded_file:
        # Success message and progress bar
        st.success("File uploaded successfully!")
        progress = st.progress(0)
        
        # Load data
        data = pd.read_excel(uploaded_file)
        progress.progress(50)
        
        # Display data preview
        st.markdown("<h4 style='color: #FF7F50;'>Step 2: Preview the Uploaded Data</h4>", unsafe_allow_html=True)
        with st.expander("Click to Preview the Dataset", expanded=True):
            st.write(data.head())
        
        # Update progress
        progress.progress(100)
        
        # Insights & Stats
        st.markdown("<h4 style='color: #FF7F50;'>Step 3: Quick Data Insights</h4>", unsafe_allow_html=True)
        if st.button("Show Data Summary"):
            st.write("**Dataset Shape**:", data.shape)
            st.write("**Data Types**:", data.dtypes)
            st.write("**Missing Values**:", data.isnull().sum())
            st.write("**Basic Statistics**:")
            st.write(data.describe())
        
        # Handle missing data button
        if st.button("Handle Missing Data"):
            data = handle_missing_data(data)
            
            # Store the cleaned data into session state
            st.session_state.cleaned_data = data
        
        # After cleaning, show the updated data summary
        if "cleaned_data" in st.session_state:
            st.markdown("<h4 style='color: #FF7F50;'>Updated Data Summary (After Handling Missing Data)</h4>", unsafe_allow_html=True)
            cleaned_data = st.session_state.cleaned_data
            st.write("**Dataset Shape**:", cleaned_data.shape)
            st.write("**Data Types**:", cleaned_data.dtypes)
            st.write("**Missing Values**:", cleaned_data.isnull().sum())
            st.write("**Basic Statistics**:")
            st.write(cleaned_data.describe())
        
        return data
    else:
        st.warning("Please upload a file to proceed.")
        return None

# For standalone running and testing
if __name__ == "__main__":
    data = data_preview()

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="📊 Universal Data Analyzer", layout="wide")
st.title("🧠 Smart Data Analyzer")
st.write("Upload any CSV or Excel file and get instant EDA & insights!")

# Upload file
uploaded_file = st.file_uploader("📁 Upload your dataset (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file:
    # Load based on file type
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    st.subheader("📋 Dataset Overview")
    st.write("**Shape:**", df.shape)
    st.write("**Columns:**", list(df.columns))

    st.subheader("🔢 Data Types")
    st.dataframe(df.dtypes.reset_index().rename(columns={'index': 'Column', 0: 'Data Type'}))

    st.subheader("🧪 Unique Values")
    unique_counts = df.nunique().reset_index()
    unique_counts.columns = ['Column', 'Unique Values']
    st.dataframe(unique_counts)

    st.subheader("📊 Summary Statistics")
    st.write("**Numeric Summary**")
    st.dataframe(df.describe())

    # Include object/categorical summary
    cat_cols = df.select_dtypes(include='object').columns.tolist()
    if cat_cols:
        st.write("**Categorical Summary**")
        st.dataframe(df[cat_cols].describe())

    st.subheader("🧹 Data Quality Checks")
    st.write("**Missing Values:**")
    st.dataframe(df.isnull().sum().reset_index().rename(columns={'index': 'Column', 0: 'Missing Values'}))
    st.write("**Duplicate Rows:**", df.duplicated().sum())

    # Auto plotting
    st.subheader("📈 Column Visualizations")

    num_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    if num_cols:
        st.write("### 🔍 Numeric Column Distributions")
        for col in num_cols:
            fig, ax = plt.subplots()
            sns.histplot(df[col].dropna(), kde=True, ax=ax, color='skyblue')
            ax.set_title(f'Distribution of {col}')
            st.pyplot(fig)

    if cat_cols:
        st.write("### 🧃 Categorical Column Counts")
        for col in cat_cols:
            if df[col].nunique() < 15:
                fig, ax = plt.subplots()
                df[col].value_counts().plot(kind='bar', ax=ax, color='lightcoral')
                ax.set_title(f'Value Counts: {col}')
                st.pyplot(fig)

    st.subheader("📌 Insights Summary")

    st.markdown(f"""
    - Rows: **{df.shape[0]}**
    - Columns: **{df.shape[1]}**
    - Numeric Columns: **{len(num_cols)}**
    - Categorical Columns: **{len(cat_cols)}**
    - Total Missing Values: **{df.isnull().sum().sum()}**
    - Duplicate Rows: **{df.duplicated().sum()}**
    """)

else:
    st.info("👈 Upload your dataset to get started!")


import streamlit as st
import pandas as pd

st.title("Lab 6: Upload CSV and Analyze")

# Upload CSV file
file = st.file_uploader("Upload a CSV file", type=["csv"])

if file is not None:
    try:
        df = pd.read_csv(file)

        if df.empty or len(df.columns) == 0:
            st.warning("The uploaded CSV is empty.")
            st.stop()

        st.subheader("1. Data Preview")
        st.dataframe(df)

        st.subheader("2. Statistics")
        st.write(df.describe(include="all"))

        st.subheader("3. Filter by Column")
        col = st.selectbox("Choose column", df.columns)
        value = st.text_input("Filter value")

        if value:
            filtered = df[
                df[col].astype(str).str.contains(
                    value, case=False, na=False
                )
            ]
            st.write("Filtered Results")
            st.dataframe(filtered)

        st.subheader("4. Sort Data")
        sort_col = st.selectbox(
            "Sort by", df.columns, key="sort_column"
        )
        st.dataframe(df.sort_values(sort_col))

        st.subheader("5. Handle Missing Values")
        st.write("Missing values in each column:")
        st.write(df.isnull().sum())

        option = st.radio(
            "Choose an option",
            ["Keep", "Drop missing rows", "Fill missing with 0"]
        )

        if option == "Drop missing rows":
            processed = df.dropna()
        elif option == "Fill missing with 0":
            processed = df.fillna(0)
        else:
            processed = df

        st.write("Processed Data")
        st.dataframe(processed)

        st.subheader("6. Download Processed CSV")
        csv_data = processed.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="processed.csv",
            mime="text/csv"
        )

        st.subheader("7. Group and Calculate Average")

        group_col = st.selectbox(
            "Group by column",
            df.columns,
            key="group_column"
        )

        numeric_cols = df.select_dtypes(
            include="number"
        ).columns.tolist()

        if numeric_cols:
            selected_num = st.selectbox(
                "Choose numeric column",
                numeric_cols
            )

            result = df.groupby(group_col)[
                selected_num
            ].mean()

            st.dataframe(result)
        else:
            st.info("No numeric columns are available.")

    except Exception as e:
        st.error(f"Could not read this CSV file: {e}")

else:
    st.info("Please upload students.csv to begin.")

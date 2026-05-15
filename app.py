import streamlit as st
import pandas as pd

from src.cleaner import (
    clean_column_names,
    remove_duplicates,
    trim_text_spaces,
    standardize_text_case,
    validate_email_columns,
    validate_phone_columns,
    convert_numeric_columns,
    fix_date_columns,
    handle_missing_values,
    flag_outliers,
)

from src.quality_score import get_quality_metrics
from src.report_generator import create_quality_report


st.set_page_config(
    page_title="DataCleanIQ",
    page_icon="🧹",
    layout="wide"
)


def load_uploaded_file(uploaded_file):
    if uploaded_file.name.endswith(".csv"):
        return pd.read_csv(uploaded_file)

    elif uploaded_file.name.endswith(".xlsx"):
        return pd.read_excel(uploaded_file)

    else:
        st.error("Unsupported file format. Please upload CSV or Excel.")
        return None


def clean_data(df, logs):
    df = clean_column_names(df, logs)
    df = remove_duplicates(df, logs)
    df = trim_text_spaces(df, logs)
    df = standardize_text_case(df, logs)
    df = validate_email_columns(df, logs)
    df = validate_phone_columns(df, logs)
    df = convert_numeric_columns(df, logs)
    df = fix_date_columns(df, logs)
    df = handle_missing_values(df, logs)
    df = flag_outliers(df, logs)

    return df


def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")


def convert_logs_to_txt(logs):
    text = "DataCleanIQ Cleaning Log\n"
    text += "=" * 50
    text += "\n\n"

    for number, log in enumerate(logs, start=1):
        text += f"{number}. {log}\n"

    return text.encode("utf-8")


def get_cleaning_summary(before_metrics, after_metrics):
    return {
        "Rows Removed": int(before_metrics["rows"] - after_metrics["rows"]),
        "Missing Values Fixed": int(before_metrics["missing_values"] - after_metrics["missing_values"]),
        "Duplicates Removed": int(before_metrics["duplicate_rows"] - after_metrics["duplicate_rows"]),
        "Invalid Emails Fixed": int(before_metrics["invalid_emails"] - after_metrics["invalid_emails"]),
        "Invalid Phones Fixed": int(before_metrics["invalid_phones"] - after_metrics["invalid_phones"]),
        "Bad Date Formats Fixed": int(before_metrics["bad_date_formats"] - after_metrics["bad_date_formats"]),
        "Invalid Numeric Values Fixed": int(before_metrics["invalid_numeric_values"] - after_metrics["invalid_numeric_values"]),
        "Risk Flags Created": int(after_metrics["risk_flags"]),
    }


with st.sidebar:
    st.title("DataCleanIQ")
    st.write("Automated data cleaning and quality reporting tool.")

    st.markdown("### Workflow")
    st.write("1. Upload CSV/Excel")
    st.write("2. Review original quality")
    st.write("3. Clean dataset")
    st.write("4. Review quality improvement")
    st.write("5. Download outputs")

    st.markdown("### Detects")
    st.write("- Missing values")
    st.write("- Duplicate rows")
    st.write("- Invalid emails")
    st.write("- Invalid phones")
    st.write("- Bad dates")
    st.write("- Invalid numeric values")
    st.write("- Outliers and risk values")


st.title("🧹 DataCleanIQ")
st.subheader("Clean, validate, score, and export messy CSV/Excel datasets.")

st.write(
    "Designed for analysts working with messy business data: missing values, duplicates, "
    "bad formats, invalid emails, phone numbers, dates, numeric errors, and outliers."
)

uploaded_file = st.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    df = load_uploaded_file(uploaded_file)

    if df is not None:
        st.success("File uploaded successfully.")

        before_metrics = get_quality_metrics(df)

        st.subheader("Before Cleaning Overview")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("Rows", int(before_metrics["rows"]))

        with col2:
            st.metric("Missing Values", int(before_metrics["missing_values"]))

        with col3:
            st.metric("Duplicate Rows", int(before_metrics["duplicate_rows"]))

        with col4:
            st.metric("Invalid Values", int(
                before_metrics["invalid_emails"]
                + before_metrics["invalid_phones"]
                + before_metrics["bad_date_formats"]
                + before_metrics["invalid_numeric_values"]
            ))

        with col5:
            st.metric("Quality Score", before_metrics["quality_score"])

        with st.expander("View Original Dataset Preview"):
            st.dataframe(df.head(30), use_container_width=True)

        clean_button = st.button("Clean Data", type="primary")

        if clean_button:
            logs = []

            logs.append(f"Uploaded file: {uploaded_file.name}")
            logs.append(f"Initial rows: {df.shape[0]}")
            logs.append(f"Initial columns: {df.shape[1]}")

            cleaned_df = clean_data(df.copy(), logs)

            after_metrics = get_quality_metrics(cleaned_df)

            logs.append(f"Before quality score: {before_metrics['quality_score']}")
            logs.append(f"After quality score: {after_metrics['quality_score']}")
            logs.append(
                f"Quality score improvement: {after_metrics['quality_score'] - before_metrics['quality_score']}"
            )
            logs.append(f"Risk flags after cleaning: {after_metrics['risk_flags']}")
            logs.append(f"Final rows: {cleaned_df.shape[0]}")
            logs.append(f"Final columns: {cleaned_df.shape[1]}")
            logs.append(f"Final duplicate rows: {cleaned_df.duplicated().sum()}")
            logs.append(f"Final missing values: {cleaned_df.isnull().sum().sum()}")

            quality_report = create_quality_report(
                before_metrics,
                after_metrics,
                output_path=None
            )

            st.session_state["cleaned_df"] = cleaned_df
            st.session_state["logs"] = logs
            st.session_state["quality_report"] = quality_report
            st.session_state["before_metrics"] = before_metrics
            st.session_state["after_metrics"] = after_metrics

if "cleaned_df" in st.session_state:
    cleaned_df = st.session_state["cleaned_df"]
    logs = st.session_state["logs"]
    quality_report = st.session_state["quality_report"]
    before_metrics = st.session_state["before_metrics"]
    after_metrics = st.session_state["after_metrics"]

    st.divider()

    st.subheader("After Cleaning Overview")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Rows",
            int(after_metrics["rows"]),
            int(after_metrics["rows"] - before_metrics["rows"])
        )

    with col2:
        st.metric(
            "Missing Values",
            int(after_metrics["missing_values"]),
            int(after_metrics["missing_values"] - before_metrics["missing_values"])
        )

    with col3:
        st.metric(
            "Duplicate Rows",
            int(after_metrics["duplicate_rows"]),
            int(after_metrics["duplicate_rows"] - before_metrics["duplicate_rows"])
        )

    with col4:
        st.metric(
            "Risk Flags",
            int(after_metrics["risk_flags"])
        )

    with col5:
        st.metric(
            "Quality Score",
            after_metrics["quality_score"],
            round(after_metrics["quality_score"] - before_metrics["quality_score"], 2)
        )

    st.subheader("Cleaning Summary")

    summary = get_cleaning_summary(before_metrics, after_metrics)

    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.metric("Missing Fixed", summary["Missing Values Fixed"])

    with s2:
        st.metric("Invalid Values Fixed", (
            summary["Invalid Emails Fixed"]
            + summary["Invalid Phones Fixed"]
            + summary["Bad Date Formats Fixed"]
            + summary["Invalid Numeric Values Fixed"]
        ))

    with s3:
        st.metric("Duplicates Removed", summary["Duplicates Removed"])

    with s4:
        st.metric("Risk Flags Created", summary["Risk Flags Created"])

    st.info(
        "Quality Score measures structural data quality such as missing values, duplicates, "
        "invalid emails, phones, dates, and numeric errors. Risk Flags highlight business anomalies "
        "such as outliers, negative sales, or suspicious quantities."
    )

    cleaned_csv = convert_df_to_csv(cleaned_df)
    log_txt = convert_logs_to_txt(logs)
    report_csv = convert_df_to_csv(quality_report)

    st.subheader("Download Outputs")

    d1, d2, d3 = st.columns(3)

    with d1:
        st.download_button(
            label="Download Cleaned CSV",
            data=cleaned_csv,
            file_name="cleaned_sales_data.csv",
            mime="text/csv"
        )

    with d2:
        st.download_button(
            label="Download Cleaning Log",
            data=log_txt,
            file_name="cleaning_log.txt",
            mime="text/plain"
        )

    with d3:
        st.download_button(
            label="Download Quality Report",
            data=report_csv,
            file_name="data_quality_report.csv",
            mime="text/csv"
        )

    with st.expander("View Cleaned Dataset Preview"):
        st.dataframe(cleaned_df.head(50), use_container_width=True)

    st.subheader("Data Quality Report")
    st.dataframe(quality_report, use_container_width=True)

    flag_columns = [
        column for column in cleaned_df.columns
        if column.lower().endswith("_flag")
    ]

    if len(flag_columns) > 0:
        st.subheader("Risk Flag Summary")

        risk_summary = []

        for column in flag_columns:
            counts = cleaned_df[column].value_counts().reset_index()
            counts.columns = ["flag_value", "count"]
            counts.insert(0, "flag_column", column)
            risk_summary.append(counts)

        risk_summary_df = pd.concat(risk_summary, ignore_index=True)

        st.dataframe(risk_summary_df, use_container_width=True)

    with st.expander("View Cleaning Log"):
        for log in logs:
            st.write("-", log)
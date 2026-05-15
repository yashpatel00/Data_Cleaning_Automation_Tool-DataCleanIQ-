import pandas as pd

from src.profiler import profile_data

from src.cleaner import (
    add_default_headers,
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
    save_cleaned_file,
    save_cleaning_log,
)

from src.quality_score import get_quality_metrics
from src.report_generator import create_quality_report


def looks_like_missing_headers(df):
    columns = list(df.columns)
    bad_header_count = 0

    for column in columns:
        column_text = str(column).strip().lower()

        if column_text.startswith("unnamed"):
            bad_header_count += 1

        elif column_text.isdigit():
            bad_header_count += 1

        elif column_text.replace(".", "", 1).isdigit():
            bad_header_count += 1

    return bad_header_count >= len(columns) / 2


def load_data(file_path, logs):
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)

        if looks_like_missing_headers(df):
            logs.append("No proper headers detected. Reloading CSV file without headers.")
            df = pd.read_csv(file_path, header=None)
            df = add_default_headers(df, logs)

    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)

        if looks_like_missing_headers(df):
            logs.append("No proper headers detected. Reloading Excel file without headers.")
            df = pd.read_excel(file_path, header=None)
            df = add_default_headers(df, logs)

    else:
        print("Unsupported file format. Please use CSV or Excel.")
        return None

    logs.append(f"Data loaded from: {file_path}")
    logs.append(f"Initial rows: {df.shape[0]}")
    logs.append(f"Initial columns: {df.shape[1]}")

    return df


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


file_path = "sample_data/messy_sales_data.csv"

cleaned_output_path = "outputs/cleaned_sales_data.csv"
log_output_path = "outputs/cleaning_log.txt"
quality_report_path = "outputs/data_quality_report.csv"

logs = []

df = load_data(file_path, logs)

if df is not None:
    print("\nDATA LOADED SUCCESSFULLY")
    print("=" * 50)

    print("\nBEFORE CLEANING")
    print("=" * 50)
    profile_data(df)

    before_metrics = get_quality_metrics(df)

    df = clean_data(df, logs)

    after_metrics = get_quality_metrics(df)

    logs.append(f"Before quality score: {before_metrics['quality_score']}")
    logs.append(f"After quality score: {after_metrics['quality_score']}")
    logs.append(f"Quality score improvement: {after_metrics['quality_score'] - before_metrics['quality_score']}")
    logs.append(f"Risk flags after cleaning: {after_metrics['risk_flags']}")
    logs.append(f"Final rows: {df.shape[0]}")
    logs.append(f"Final columns: {df.shape[1]}")
    logs.append(f"Final duplicate rows: {df.duplicated().sum()}")
    logs.append(f"Final missing values: {df.isnull().sum().sum()}")

    print("\nAFTER CLEANING")
    print("=" * 50)
    profile_data(df)

    save_cleaned_file(df, cleaned_output_path, logs)
    save_cleaning_log(logs, log_output_path)

    quality_report = create_quality_report(
        before_metrics,
        after_metrics,
        quality_report_path
    )

    print("\nDATA QUALITY REPORT")
    print("=" * 50)
    print(quality_report)
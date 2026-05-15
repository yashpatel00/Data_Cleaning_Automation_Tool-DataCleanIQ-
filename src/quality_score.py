import pandas as pd
import re
from datetime import datetime


def count_invalid_emails(df):
    invalid_count = 0
    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    for column in df.columns:
        if "email" in column.lower():
            for value in df[column]:
                if pd.isna(value):
                    continue

                value_text = str(value).strip().lower()

                if value_text == "unknown":
                    continue

                if not re.match(email_pattern, value_text):
                    invalid_count += 1

    return invalid_count


def count_invalid_phones(df):
    invalid_count = 0
    phone_pattern = r"^\d{3}-\d{3}-\d{4}$"

    for column in df.columns:
        if "phone" in column.lower():
            for value in df[column]:
                if pd.isna(value):
                    continue

                value_text = str(value).strip()

                if value_text == "Unknown":
                    continue

                if not re.match(phone_pattern, value_text):
                    invalid_count += 1

    return invalid_count


def is_valid_clean_date(value):
    if pd.isna(value):
        return True

    value_text = str(value).strip()

    if value_text in ["Unknown", "Invalid Date"]:
        return True

    try:
        datetime.strptime(value_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def count_bad_date_formats(df):
    bad_count = 0

    for column in df.columns:
        if "date" in column.lower():
            for value in df[column]:
                if not is_valid_clean_date(value):
                    bad_count += 1

    return bad_count


def count_invalid_numeric_values(df):
    invalid_count = 0
    numeric_keywords = ["amount", "sales", "price", "quantity", "total"]

    for column in df.columns:
        column_lower = column.lower()

        if column_lower.endswith("_flag"):
            continue

        if any(keyword in column_lower for keyword in numeric_keywords):
            for value in df[column]:
                if pd.isna(value):
                    continue

                try:
                    float(value)
                except ValueError:
                    invalid_count += 1

    return invalid_count


def count_risk_flags(df):
    flag_count = 0

    for column in df.columns:
        if column.lower().endswith("_flag"):
            flag_count += int((df[column] != "Normal").sum())

    return flag_count


def calculate_quality_score(df):
    total_cells = df.shape[0] * df.shape[1]

    if total_cells == 0:
        return 0

    missing_values = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()
    invalid_emails = count_invalid_emails(df)
    invalid_phones = count_invalid_phones(df)
    bad_dates = count_bad_date_formats(df)
    invalid_numeric_values = count_invalid_numeric_values(df)

    score = 100

    score -= (missing_values / total_cells) * 40
    score -= duplicate_rows * 5
    score -= invalid_emails * 3
    score -= invalid_phones * 3
    score -= bad_dates * 2
    score -= invalid_numeric_values * 3

    if score < 0:
        score = 0

    return round(score, 2)


def get_quality_metrics(df):
    return {
        "rows": float(df.shape[0]),
        "columns": float(df.shape[1]),
        "total_cells": float(df.shape[0] * df.shape[1]),
        "missing_values": float(df.isnull().sum().sum()),
        "duplicate_rows": float(df.duplicated().sum()),
        "invalid_emails": float(count_invalid_emails(df)),
        "invalid_phones": float(count_invalid_phones(df)),
        "bad_date_formats": float(count_bad_date_formats(df)),
        "invalid_numeric_values": float(count_invalid_numeric_values(df)),
        "risk_flags": float(count_risk_flags(df)),
        "quality_score": float(calculate_quality_score(df)),
    }
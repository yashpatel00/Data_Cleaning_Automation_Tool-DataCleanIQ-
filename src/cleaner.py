import pandas as pd
import re
from datetime import datetime


def add_log(logs, message):
    logs.append(message)
    print(message)


def add_default_headers(df, logs):
    df = df.copy()
    df.columns = [f"column_{i + 1}" for i in range(df.shape[1])]
    add_log(logs, "Default headers added.")
    return df


def clean_column_names(df, logs):
    df = df.copy()

    old_columns = list(df.columns)

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    new_columns = list(df.columns)

    add_log(logs, "Column names cleaned.")
    add_log(logs, f"Old columns: {old_columns}")
    add_log(logs, f"New columns: {new_columns}")

    return df


def remove_duplicates(df, logs):
    before_rows = df.shape[0]

    df = df.drop_duplicates().copy()

    after_rows = df.shape[0]
    removed_rows = before_rows - after_rows

    add_log(logs, f"Duplicate rows removed: {removed_rows}")

    return df


def trim_text_spaces(df, logs):
    df = df.copy()

    text_columns = df.select_dtypes(include="object").columns

    for column in text_columns:
        df[column] = df[column].apply(
            lambda value: value.strip() if isinstance(value, str) else value
        )

    add_log(logs, "Extra spaces removed from text columns.")

    return df


def standardize_text_case(df, logs):
    df = df.copy()

    text_columns = df.select_dtypes(include="object").columns
    changed_columns = []

    for column in text_columns:
        column_lower = column.lower()

        if "email" in column_lower:
            df[column] = df[column].apply(
                lambda value: value.lower() if isinstance(value, str) else value
            )
            changed_columns.append(column)

        elif "phone" in column_lower:
            continue

        elif "date" in column_lower:
            continue

        else:
            df[column] = df[column].apply(
                lambda value: value.title() if isinstance(value, str) else value
            )
            changed_columns.append(column)

    add_log(logs, f"Text case standardized for columns: {changed_columns}")

    return df


def validate_email_columns(df, logs):
    df = df.copy()

    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    for column in df.columns:
        if "email" in column.lower():
            invalid_count = 0

            def clean_email(value):
                nonlocal invalid_count

                if pd.isna(value):
                    return pd.NA

                value = str(value).strip().lower()

                if re.match(email_pattern, value):
                    return value

                invalid_count += 1
                return pd.NA

            df[column] = df[column].apply(clean_email)

            add_log(logs, f"Email column validated: {column}")
            add_log(logs, f"Invalid emails found: {invalid_count}")

    return df


def validate_phone_columns(df, logs):
    df = df.copy()

    for column in df.columns:
        if "phone" in column.lower():
            invalid_count = 0
            formatted_count = 0

            def clean_phone(value):
                nonlocal invalid_count, formatted_count

                if pd.isna(value):
                    return pd.NA

                digits = re.sub(r"\D", "", str(value))

                if len(digits) == 10:
                    formatted_count += 1
                    return f"{digits[0:3]}-{digits[3:6]}-{digits[6:10]}"

                invalid_count += 1
                return pd.NA

            df[column] = df[column].apply(clean_phone)

            add_log(logs, f"Phone column validated: {column}")
            add_log(logs, f"Phone numbers formatted: {formatted_count}")
            add_log(logs, f"Invalid phone numbers found: {invalid_count}")

    return df


def words_to_number(value):
    if pd.isna(value):
        return value

    if not isinstance(value, str):
        return value

    text = value.strip().lower()

    number_words = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
    }

    if text in number_words:
        return number_words[text]

    parts = text.split()

    if len(parts) == 2 and parts[1] == "hundred" and parts[0] in number_words:
        return number_words[parts[0]] * 100

    return value


def convert_numeric_columns(df, logs):
    df = df.copy()

    numeric_keywords = ["amount", "sales", "price", "quantity", "total"]

    for column in df.columns:
        column_lower = column.lower()

        if any(keyword in column_lower for keyword in numeric_keywords):
            before_missing = df[column].isnull().sum()
            before_values = df[column].copy()

            df[column] = df[column].apply(words_to_number)
            df[column] = pd.to_numeric(df[column], errors="coerce")

            after_missing = df[column].isnull().sum()
            invalid_values = after_missing - before_missing

            converted_word_count = 0

            for old_value in before_values:
                if isinstance(old_value, str):
                    converted_value = words_to_number(old_value)

                    if converted_value != old_value:
                        converted_word_count += 1

            add_log(logs, f"Numeric column converted: {column}")
            add_log(logs, f"Number-word values converted: {converted_word_count}")
            add_log(logs, f"Invalid numeric values found: {invalid_values}")

    return df


def parse_mixed_date(value):
    if pd.isna(value):
        return "Unknown"

    value_text = str(value).strip()

    if value_text == "":
        return "Unknown"

    date_formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%m/%d/%Y",
        "%m-%d-%Y",
        "%d/%m/%Y",
        "%d-%m-%Y",
    ]

    for date_format in date_formats:
        try:
            parsed_date = datetime.strptime(value_text, date_format)
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            pass

    return "Invalid Date"


def fix_date_columns(df, logs):
    df = df.copy()

    for column in df.columns:
        if "date" in column.lower():
            invalid_count = 0
            missing_count = 0

            def clean_date(value):
                nonlocal invalid_count, missing_count

                result = parse_mixed_date(value)

                if result == "Unknown":
                    missing_count += 1

                elif result == "Invalid Date":
                    invalid_count += 1

                return result

            df[column] = df[column].apply(clean_date)

            add_log(logs, f"Date column fixed: {column}")
            add_log(logs, f"Missing dates found: {missing_count}")
            add_log(logs, f"Invalid dates found: {invalid_count}")

    return df


def handle_missing_values(df, logs):
    df = df.copy()

    for column in df.columns:
        column_lower = column.lower()
        missing_before = df[column].isnull().sum()

        if missing_before == 0:
            continue

        if "id" in column_lower:
            df[column] = df[column].fillna("Unknown")

            add_log(logs, f"Missing ID values filled with Unknown in column: {column}")
            add_log(logs, f"Values filled: {missing_before}")

        elif pd.api.types.is_numeric_dtype(df[column]):
            median_value = df[column].median()
            df[column] = df[column].fillna(median_value)

            add_log(logs, f"Missing numeric values filled in column: {column}")
            add_log(logs, "Fill method: median")
            add_log(logs, f"Median value used: {median_value}")
            add_log(logs, f"Values filled: {missing_before}")

        else:
            df[column] = df[column].fillna("Unknown")

            add_log(logs, f"Missing text values filled with Unknown in column: {column}")
            add_log(logs, f"Values filled: {missing_before}")

    add_log(logs, "Missing values handled.")

    return df


def flag_outliers(df, logs):
    df = df.copy()

    numeric_columns = df.select_dtypes(include="number").columns
    flagged_columns = []

    for column in numeric_columns:
        column_lower = column.lower()

        if "id" in column_lower:
            continue

        flag_column = f"{column}_flag"
        df[flag_column] = "Normal"

        if (
            "amount" in column_lower
            or "sales" in column_lower
            or "price" in column_lower
            or "total" in column_lower
        ):
            df.loc[df[column] < 0, flag_column] = "Suspicious Negative Value"

        if "quantity" in column_lower:
            df.loc[df[column] <= 0, flag_column] = "Suspicious Quantity"

        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1

        lower_limit = q1 - 1.5 * iqr
        upper_limit = q3 + 1.5 * iqr

        df.loc[df[column] > upper_limit, flag_column] = "High Outlier"

        df.loc[
            (df[column] < lower_limit) & (df[flag_column] == "Normal"),
            flag_column
        ] = "Low Outlier"

        flagged_count = (df[flag_column] != "Normal").sum()

        if flagged_count > 0:
            flagged_columns.append(flag_column)
            add_log(logs, f"Outlier flag added: {flag_column}")
            add_log(logs, f"Flagged values in {column}: {flagged_count}")
            add_log(logs, f"IQR lower limit for {column}: {lower_limit}")
            add_log(logs, f"IQR upper limit for {column}: {upper_limit}")
        else:
            df = df.drop(columns=[flag_column])

    if len(flagged_columns) == 0:
        add_log(logs, "No numeric outliers found.")
    else:
        add_log(logs, f"Outlier flag columns created: {flagged_columns}")

    return df


def save_cleaned_file(df, output_path, logs):
    df.to_csv(output_path, index=False)
    add_log(logs, f"Cleaned file saved to: {output_path}")


def save_cleaning_log(logs, log_path):
    with open(log_path, "w", encoding="utf-8") as file:
        file.write("DataCleanIQ Cleaning Log\n")
        file.write("=" * 50)
        file.write("\n\n")

        for number, log in enumerate(logs, start=1):
            file.write(f"{number}. {log}\n")

    print("Cleaning log saved to:", log_path)
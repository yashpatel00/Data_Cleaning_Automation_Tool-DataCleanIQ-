# DataCleanIQ

**DataCleanIQ** is an automated data cleaning and quality reporting tool built with **Python, Pandas, and Streamlit**.

It allows users to upload messy CSV or Excel files, clean common data quality issues, generate a cleaning log, calculate before-and-after quality scores, flag suspicious values, and download cleaned outputs.

## Live Demo

[View DataCleanIQ App](https://data-clean-iq-yash.streamlit.app/)

## Problem

Raw business datasets often contain missing values, duplicates, invalid emails, bad phone numbers, inconsistent dates, text stored as numbers, and outliers.

DataCleanIQ automates these cleaning tasks and gives users a clear before-and-after quality report.

## Features

- Upload CSV or Excel files
- Preview original and cleaned data
- Clean column names
- Remove duplicates
- Trim extra spaces
- Standardize text formatting
- Validate emails and phone numbers
- Convert numeric text values such as `five hundred → 500`
- Standardize date formats
- Handle missing values
- Flag outliers and suspicious values
- Generate cleaning log
- Generate data quality report
- Download cleaned CSV, log, and report

## Tech Stack

| Tool | Use |
|---|---|
| Python | Core logic |
| Pandas | Data cleaning and validation |
| Streamlit | Interactive dashboard |
| Regex | Email and phone validation |
| OpenPyXL | Excel file support |

## Results

| Metric | Before | After |
|---|---:|---:|
| Missing Values | 17 | 0 |
| Duplicate Rows | 1 | 0 |
| Invalid Emails | 1 | 0 |
| Invalid Phones | 5 | 0 |
| Bad Date Formats | 3 | 0 |
| Invalid Numeric Values | 1 | 0 |
| Quality Score | 64.42 | 100.00 |

## Example Cleaning Transformations

| Original | Cleaned |
|---|---|
| ` toronto ` | `Toronto` |
| `COMPLETED` | `Completed` |
| `9051113344` | `905-111-3344` |
| `noemail` | `Unknown` |
| `five hundred` | `500` |
| `2024/02/10` | `2024-02-10` |
| `not a date` | `Invalid Date` |

## Outlier Flagging

The tool does not delete suspicious values automatically. It flags them for review.

| Value | Flag |
|---|---|
| `sales_amount = -50` | Suspicious Negative Value |
| `sales_amount = 99999` | High Outlier |
| `quantity = 0` | Suspicious Quantity |

## Screenshots

### Dashboard Overview

![Dashboard Overview](screenshots/Dashboard%20Overview.png)

### Before Cleaning View

![Before Cleaning View](screenshots/Before%20Cleaning%20View.png)

### Cleaning Summary

![Cleaning Summary](screenshots/Cleaning%20Summary.png)

### Data Quality Report

![Data Quality Report](screenshots/Data%20Quality%20Report.png)

## Project Structure

```text
data-cleaning-automation-tool/
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── screenshots/
│   ├── Dashboard Overview.png
│   ├── Before Cleaning View.png
│   ├── Cleaning Summary.png
│   └── Data Quality Report.png
└── src/
    ├── cleaner.py
    ├── profiler.py
    ├── quality_score.py
    └── report_generator.py
```

## Run Locally

Clone the repository:

```bash
git clone https://github.com/yashpatel00/data-cleaning-automation-tool.git
cd data-cleaning-automation-tool
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the Streamlit app:

```bash
python -m streamlit run app.py
```

## Requirements

```text
streamlit
pandas
openpyxl
```

## Outputs

The app generates:

- `cleaned_sales_data.csv`
- `cleaning_log.txt`
- `data_quality_report.csv`

## Skills Demonstrated

- Python
- Pandas
- Streamlit
- Data cleaning
- Data validation
- Regex
- Missing value handling
- Date parsing
- Outlier detection
- Data quality scoring
- Business reporting

## Author

**Yash Patel**

- GitHub: [github.com/yashpatel00](https://github.com/yashpatel00)
- LinkedIn: [linkedin.com/in/yashpatel100](https://www.linkedin.com/in/yashpatel100/)

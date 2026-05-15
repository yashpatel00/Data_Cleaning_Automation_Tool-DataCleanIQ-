def show_basic_info(df):
    print("\nBASIC DATASET INFO")
    print("-" * 40)
    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])
    print("Total Cells:", df.shape[0] * df.shape[1])


def show_column_names(df):
    print("\nCOLUMN NAMES")
    print("-" * 40)
    print(list(df.columns))


def show_missing_values(df):
    print("\nMISSING VALUES")
    print("-" * 40)
    print(df.isnull().sum())


def show_duplicate_rows(df):
    print("\nDUPLICATE ROWS")
    print("-" * 40)
    print("Duplicate rows:", df.duplicated().sum())


def show_data_types(df):
    print("\nDATA TYPES")
    print("-" * 40)
    print(df.dtypes)


def show_preview(df):
    print("\nDATA PREVIEW")
    print("-" * 40)
    print(df.head())


def profile_data(df):
    show_preview(df)
    show_basic_info(df)
    show_column_names(df)
    show_missing_values(df)
    show_duplicate_rows(df)
    show_data_types(df)
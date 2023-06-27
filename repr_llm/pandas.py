"""Summarizing Pandas DataFrames and Series for Large Language Models."""

# This module is an optional import due to importing numpy and pandas

PANDAS_INSTALLED = False

try:
    import numpy as np
    import pandas as pd

    PANDAS_INSTALLED = True
except ImportError:
    pass


def summarize_dataframe(df, sample_rows=5, sample_columns=20):
    """Create a summary of a Pandas DataFrame for Large Language Model Consumption.

    Args:
        df (Pandas DataFrame): The dataframe to be summarized.
        sample_rows (int): The number of rows to sample
        sample_columns (int): The number of columns to sample

    Returns:
        A markdown string with a summary of the dataframe
    """
    if not PANDAS_INSTALLED:
        raise ImportError("Pandas must be installed to use summarize_dataframe")

    num_rows, num_cols = df.shape

    # # Column Summary
    # ## Missing value summary for all columns
    missing_values = pd.DataFrame(df.isnull().sum(), columns=["Missing Values"])
    missing_values["% Missing"] = missing_values["Missing Values"] / num_rows * 100

    # ## Data type summary for all columns
    column_info = pd.concat([df.dtypes, missing_values], axis=1).reset_index()
    column_info.columns = ["Column Name", "Data Type", "Missing Values", "% Missing"]
    column_info["Data Type"] = column_info["Data Type"].astype(str)

    # TODO: Bring these back once we can ensure `describe` does not fail on some tables
    # # Basic summary statistics for numerical and categorical columns
    # # get basic statistical information for each column
    # numerical_summary = df.describe(include=[np.number]).T.reset_index().rename(columns={'index': 'Column Name'})

    has_categoricals = any(df.select_dtypes(include=['category', 'datetime', 'timedelta']).columns)

    if has_categoricals:
        categorical_describe = df.describe(include=['category', 'datetime', 'timedelta'])
        categorical_summary = categorical_describe.T.reset_index().rename(columns={'index': 'Column Name'})
    else:
        categorical_summary = pd.DataFrame(columns=['Column Name'])

    sample_columns = min(sample_columns, df.shape[1])
    sample_rows = min(sample_rows, df.shape[0])
    sampled = df.sample(sample_columns, axis=1).sample(sample_rows, axis=0)

    tablefmt = "github"

    # create the markdown string for output
    output = (
        f"## Dataframe Summary\n\n"
        f"Number of Rows: {num_rows:,}\n\n"
        f"Number of Columns: {num_cols:,}\n\n"
        f"### Column Information\n\n{column_info.to_markdown(tablefmt=tablefmt)}\n\n"
        # f"### Numerical Summary\n\n{numerical_summary.to_markdown(tablefmt=tablefmt)}\n\n"
        f"### Categorical Summary\n\n{categorical_summary.to_markdown(tablefmt=tablefmt)}\n\n"
        f"### Sample Data ({sample_rows}x{sample_columns})\n\n{sampled.to_markdown(tablefmt=tablefmt)}"
    )

    return output


def summarize_series(series, sample_size=5):
    """Create a summary of a Pandas Series for Large Language Model Consumption.

    Args:
        series (pd.Series): The series to be summarized.
        sample_size (int): The number of values to sample

    Returns:
        A markdown string with a summary of the series
    """
    if not PANDAS_INSTALLED:
        raise ImportError("Pandas must be installed to use summarize_series")

    # Get basic series information
    num_values = len(series)
    data_type = series.dtype
    num_missing = series.isnull().sum()
    percent_missing = num_missing / num_values * 100

    # Get summary statistics based on the data type
    if np.issubdtype(data_type, np.number):
        summary_statistics = series.describe().to_frame().T
    elif pd.api.types.is_string_dtype(data_type):
        summary_statistics = series.describe(datetime_is_numeric=True).to_frame().T
    else:
        summary_statistics = series.describe().to_frame().T

    # Sample data
    sampled = series.sample(min(sample_size, num_values))

    tablefmt = "github"

    # Create the markdown string for output
    output = (
        f"## Series Summary\n\n"
        f"Number of Values: {num_values:,}\n\n"
        f"Data Type: {data_type}\n\n"
        f"Missing Values: {num_missing:,} ({percent_missing:.2f}%)\n\n"
        f"### Summary Statistics\n\n{summary_statistics.to_markdown(tablefmt=tablefmt)}\n\n"
        f"### Sample Data ({sample_size})\n\n{sampled.to_frame().to_markdown(tablefmt=tablefmt)}"
    )

    return output


def format_dataframe_for_llm(df):
    """Format a dataframe for Large Language Model Consumption.

    Args:
        df (Pandas DataFrame): The dataframe to be formatted.

    Returns:
        A markdown string with a formatted dataframe
    """
    if not PANDAS_INSTALLED:
        raise ImportError("Pandas must be installed to use format_dataframe_for_llm")

    with pd.option_context('display.max_rows', 5, 'display.html.table_schema', False, 'display.max_columns', 20):
        num_columns = min(pd.options.display.max_columns, df.shape[1])
        num_rows = min(pd.options.display.max_rows, df.shape[0])
        return summarize_dataframe(df, sample_rows=num_rows, sample_columns=num_columns)


def format_series_for_llm(series):
    """Format a series for Large Language Model Consumption.

    Args:
        series (Pandas Series): The series to be formatted.

    Returns:
        A markdown string with a formatted series
    """
    if not PANDAS_INSTALLED:
        raise ImportError("Pandas must be installed to use format_series_for_llm")

    with pd.option_context('display.max_rows', 5, 'display.html.table_schema', False, 'display.max_columns', 20):
        num_cols = min(pd.options.display.max_columns, series.shape[0])
        return summarize_series(series, sample_size=num_cols)

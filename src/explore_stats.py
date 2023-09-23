import pandas as pd
import numpy as np

def calculate_stats_within_date_range(
    df: pd.DataFrame, 
    column_name: str, 
    date_column: str = 'date', 
    start_date: str = None, 
    end_date=None
    ) -> tuple:
    
    """
    Calculate the number of non-null values, the percentage of missing values, the average, and the standard deviation
    of a DataFrame column within a specified date range. If no date range is specified (start_date and end_date are None),
    the calculations are performed on the entire column.

    Parameters:
        df (pandas.DataFrame): The DataFrame containing the column and the date column.
        column_name (str): The name of the DataFrame column for which you want to calculate statistics.
        start_date (str or None): The start date of the date range. Default is None.
        end_date (str or None): The end date of the date range. Default is None.

    Returns:
        tuple: A tuple containing the number of non-null values, the percentage of missing values,
        the average (mean), and the standard deviation of the specified column within the specified date range.
    """
    date_column = df[date_column]
    column = df[column_name]

    if start_date is not None and end_date is not None:
        # Filter the DataFrame based on the date range
        mask = (date_column >= start_date) & (date_column <= end_date)
        column = column[mask]

    total_values = len(column)
    non_null_count = column.count()  # Count of non-null values
    missing_count = total_values - non_null_count  # Count of missing (null) values
    missing_percentage = (missing_count / total_values) * 100.0
    average = column.mean()
    std_deviation = column.std()  # Standard deviation

    # Format the mean and standard deviation with a specific number of decimal places
    average_formatted = round(average, 2)
    std_deviation_formatted = round(std_deviation, 2)

    return non_null_count, missing_percentage, average_formatted, std_deviation_formatted
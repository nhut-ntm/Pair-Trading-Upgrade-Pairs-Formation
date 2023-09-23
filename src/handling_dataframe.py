import pandas as pd 


def reformat_dataframe(
    df: pd.DataFrame, 
    index_col: str, 
    columns_col: str, 
    values_col: str, 
    prefix: str=''
    ) -> pd.DataFrame:
    
    """
    Reformat a DataFrame by pivoting it, flattening the column index, and resetting the index.

    Parameters:
        df (pandas.DataFrame): The DataFrame to be reformatted.
        index_col (str): The name of the column to use as the index in the pivoted DataFrame.
        columns_col (str): The name of the column to use for column names in the pivoted DataFrame.
        values_col (list of str): The names of the columns to use as values in the pivoted DataFrame.
        prefix (str, optional): Prefix to add to the column names in the reformatted DataFrame. Default is ''.

    Returns:
        pandas.DataFrame: The reformatted DataFrame.
    """
    # Pivot the DataFrame
    pivoted_df = df.pivot(index=index_col, columns=columns_col, values=values_col)

    # Flatten the multi-level column index
    pivoted_df.columns = [f'{prefix}{col[0]}_{col[1]}' for col in pivoted_df.columns]

    # Reset the index to make the specified column a regular column
    pivoted_df.reset_index(inplace=True)

    return pivoted_df



def calculate_missing_percentage(df: pd.DataFrame) -> pd.DataFrame:
    # Calculate missing percentage for each column
    missing_count = (df.isnull() | df.isna()).sum()
    missing_percentage = (missing_count * 100 / df.index.size)
    
    # Create a DataFrame to store the results
    missing_percentage_df = pd.DataFrame(
        {
            'column': missing_percentage.index, 
            'percentage': missing_percentage.values,
            'count': missing_count.values
        }
    )
    
    return missing_percentage_df


def calculate_duplicate_percentage(df: pd.DataFrame) -> pd.DataFrame:
    # Calculate duplicated percentage for each column
    duplicated_count = df.duplicated().sum()
    duplicated_percentage = (duplicated_count * 100 / df.shape[0])

    # Create a DataFrame to store the results
    duplicated_percentage_df = pd.DataFrame(
        {
            'column': ['Duplicated'],
            'percentage': [duplicated_percentage],
            'count': [duplicated_count]
        }
    )

    return duplicated_percentage_df


def resample_dataframe(
    df: pd.DataFrame, 
    date_column: str,
    space_freq: str = 'D'
    ):

    # Ensure the date column is in datetime format
    df[date_column] = pd.to_datetime(df[date_column])
    
    # Resample the DataFrame at the specified frequency
    resampled_df = df.set_index(date_column).resample(space_freq).asfreq()
    
    return resampled_df
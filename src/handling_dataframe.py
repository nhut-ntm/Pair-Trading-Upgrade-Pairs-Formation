import pandas as pd 
import itertools
from itertools import combinations


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


def pairs_formation_result_summary(
    gatev_pairs_list: list,
    eg_pairs_list: list,
    eg_pairs_swap_list: list,
    johansen_pairs_list: list
) -> pd.DataFrame:
    
    # Combine all four lists into a single list
    all_pairs = gatev_pairs_list + eg_pairs_list + eg_pairs_swap_list + johansen_pairs_list

    # Use a set to store unique values
    unique_values = set()

    # Iterate through the lists and add their elements to the set
    for pair in all_pairs:
        unique_values.update(pair)

    # Convert the set back to a list
    unique_values_list = list(unique_values)

    # Sort the list if needed
    unique_values_list.sort()
    
    # Create a list to store the combinations
    combinations_list = []

    # Use itertools.combinations to generate the combinations
    for combo in combinations(unique_values_list, 2):
        combinations_list.append(combo)
    
    # Create an empty DataFrame with the specified columns
    columns = ['Stock A', 'Stock B', 'Gatev Pairs', 'EG Pairs', 'EG Pairs Swap', 'Johansen Pairs']
    df = pd.DataFrame(columns=columns)
    
    # Create an empty list of dictionaries
    data = []

    # Iterate through combinations and check if they appear in the given lists
    for combo in combinations_list:
        stock_a, stock_b = combo
        row = {'Stock A': stock_a, 'Stock B': stock_b}

        count_x = 0  # Initialize the count of 'x' marks for this combination

        for pair in gatev_pairs_list:
            if [stock_a, stock_b] == pair or [stock_b, stock_a] == pair:
                row['Gatev Pairs'] = 'x'
                count_x += 1

        for pair in eg_pairs_list:
            if [stock_a, stock_b] == pair or [stock_b, stock_a] == pair:
                row['EG Pairs'] = 'x'
                count_x += 1

        for pair in eg_pairs_swap_list:
            if [stock_a, stock_b] == pair or [stock_b, stock_a] == pair:
                row['EG Pairs Swap'] = 'x'
                count_x += 1

        for pair in johansen_pairs_list:
            if [stock_a, stock_b] == pair or [stock_b, stock_a] == pair:
                row['Johansen Pairs'] = 'x'
                count_x += 1

        row['Count'] = count_x  # Add the count of 'x' marks for this combination
        data.append(row)

    # Create the DataFrame from the list of dictionaries
    df = pd.DataFrame(data)

    # Create an additional row at the end that counts the number of 'x' marks
    count_row = {'Stock A': 'Count', 'Stock B': ''}
    for col in df.columns[2:]:
        count_row[col] = (df[col] == 'x').sum()

    df = df.append(count_row, ignore_index=True)

    # Reorder the columns to have 'Count' as the last column
    df = df[['Stock A', 'Stock B', 'Gatev Pairs', 'EG Pairs', 'EG Pairs Swap', 'Johansen Pairs', 'Count']]

    # Fill NaN values with an empty string for better representation
    df = df.fillna('')   
    
    # Select pairs that satisfy more than one of the tests
    df_pairs = df[df['Count']>0]
    df_pairs = df_pairs.reset_index(drop=True)
    
    return df_pairs
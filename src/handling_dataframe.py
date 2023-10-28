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
    columns = ['Stock A', 'Stock B', 'Gatev Pairs', 'EG Pairs', 'EG Pairs Swap', 'Johansen Pairs', 'Count']
    df = pd.DataFrame(columns=columns)
    
    # Create an empty list of dictionaries
    data = []

    # Iterate through combinations and check if they appear in the given lists
    for combo in combinations_list:
        stock_a, stock_b = combo
        row = {'Stock A': stock_a, 'Stock B': stock_b, 'Count': 0}

        if gatev_pairs_list:
            for pair in gatev_pairs_list:
                if [stock_a, stock_b] == pair or [stock_b, stock_a] == pair:
                    row['Gatev Pairs'] = 'x'
                    row['Count'] += 1

        if eg_pairs_list:
            for pair in eg_pairs_list:
                if [stock_a, stock_b] == pair or [stock_b, stock_a] == pair:
                    row['EG Pairs'] = 'x'
                    row['Count'] += 1

        if eg_pairs_swap_list:
            for pair in eg_pairs_swap_list:
                if [stock_a, stock_b] == pair or [stock_b, stock_a] == pair:
                    row['EG Pairs Swap'] = 'x'
                    row['Count'] += 1

        if johansen_pairs_list:
            for pair in johansen_pairs_list:
                if [stock_a, stock_b] == pair or [stock_b, stock_a] == pair:
                    row['Johansen Pairs'] = 'x'
                    row['Count'] += 1

        data.append(row)

    # Create the DataFrame from the list of dictionaries
    df = pd.DataFrame(data)

    # Fill NaN values with an empty string for better representation
    df = df.fillna('')   
    
    count_element_in_list = [
        len(gatev_pairs_list), 
        len(eg_pairs_list), 
        len(eg_pairs_swap_list), 
        len(johansen_pairs_list)]
    
    if 0 not in count_element_in_list: 
        # Define the desired column order as a list
        desired_column_order = ['Stock A', 'Stock B', 'Gatev Pairs', 'EG Pairs', 'EG Pairs Swap', 'Johansen Pairs', 'Count']
    
         # Reorder the DataFrame based on the desired column order
        df = df[desired_column_order]
    else:
        # Define the name of the column you want to move to the last position
        column_name_to_move = 'Count'

        # Check if the column exists in the DataFrame
        if column_name_to_move in df.columns:
            # Get the list of column names, excluding the one you want to move
            column_order = [col for col in df.columns if col != column_name_to_move]
            # Add the column at the last position
            column_order.append(column_name_to_move)
            # Reorder the DataFrame based on the new column order
            df = df[column_order]

    # Select pairs that satisfy more than one of the tests
    df_pairs = df[df['Count'] > 0]
    
    df_pairs = df_pairs.reset_index(drop=True)
    
    return df_pairs
import pandas as pd 


def splitting_data_by_ratio(
    df: pd.DataFrame,
    split_ratio: float
) -> tuple:
    # Calculate the split point based on the ratio
    split_point = int(len(df) * split_ratio)

    # Split the DataFrame into training and test sets
    train_df = df.iloc[:split_point]
    test_df = df.iloc[split_point:]

    return train_df, test_df


def splitting_data_by_date(
    df: pd.DataFrame, 
    train_period: list,
    test_period: list
) -> tuple:
    
    # Select the data for training from Start Date to End Date 
    train_set = df[train_period[0]:train_period[1]]
    
    # Select the data for testing from Start Date to End Date 
    test_set = df[test_period[0]:test_period[1]]
    
    return train_set, test_set
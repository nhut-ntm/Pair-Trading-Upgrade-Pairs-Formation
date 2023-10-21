import pandas as pd 
from statsmodels.tsa.stattools import adfuller

def find_integration_order(
    df: pd.DataFrame, 
    significance_level=0.05
) -> pd.DataFrame:
    
    results = []

    # Perform ADF Test over and over again until the time series is stationary 
    # The order of integration is the number of times ADF needs to be performed to make the time series stationary
    for col in df.columns:
        series = df[col]
        order = 0

        while True:
            result_adf = adfuller(series)
            p_value = result_adf[1]

            if p_value <= significance_level:
                break
            else:
                series = series.diff().dropna()  # Differencing to make it stationary
                order += 1

        # Summarize the result into a table 
        results.append({'Column Name': col, 'Integration Order': order})

    result_df = pd.DataFrame(results)
    
    return result_df
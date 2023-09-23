import pandas as pd 
import explore_stats as xstats


def stock_exploration(
    df: pd.DataFrame
    ) -> pd.DataFrame:

  lst_stock_code = []
  lst_floor = []
  lst_start_date = []
  lst_end_date = []
  lst_number_of_days = []
  lst_vol_non_null_all = []
  lst_vol_missing_pct_all = []
  lst_vol_avg_all = []
  lst_vol_std_all = []
  lst_adclose_non_null_all = []
  lst_adclose_missing_pct_all = []

  # Iterate each stock in the code column
  for code in df['code'].unique():

    lst_stock_code.append(code)

    # Select the subdataframe based on the current stock code
    df_stock_temp = df[df['code'] == code]

    # Add the floor which the stock is listed to the lst_floor
    lst_floor.append(df_stock_temp['floor'].unique()[0])

    # Sort the date column
    df_stock_temp_sorted = df_stock_temp.sort_values(by='date')

    # Datetime -----------------------------------------
    # Select the first date and last date
    first_date = df_stock_temp_sorted['date'].min()
    last_date = df_stock_temp_sorted['date'].max()
    number_of_days = len(df_stock_temp_sorted['date'])

    lst_start_date.append(first_date)
    lst_end_date.append(last_date)
    lst_number_of_days.append(number_of_days)

    # Volume Stats -----------------------------------------
    # The number of non-null values and the missing value percentages of volume
    non_null_count_vol_all, missing_pct_vol_all, average_vol_all, std_vol_all = xstats.calculate_stats_within_date_range(
        df_stock_temp_sorted, column_name = 'nmVolume'
    )
    lst_vol_non_null_all.append(non_null_count_vol_all)
    lst_vol_missing_pct_all.append(missing_pct_vol_all)
    lst_vol_avg_all.append(average_vol_all)
    lst_vol_std_all.append(std_vol_all)

    # adClose Stats -----------------------------------------
    # The number of non-null values and the missing value percentages of adClose
    non_null_count_adclose_all, missing_pct_adclose_all, _, _ = xstats.calculate_stats_within_date_range(
        df_stock_temp_sorted, column_name = 'adClose'
    )
    lst_adclose_non_null_all.append(non_null_count_adclose_all)
    lst_adclose_missing_pct_all.append(missing_pct_adclose_all)


  result_df = pd.DataFrame({
      'code': lst_stock_code,
      'floor': lst_floor,
      'start_date': lst_start_date,
      'end_date': lst_end_date,
      'number_of_days': lst_number_of_days,
      'vol_non_null_all': lst_vol_non_null_all,
      'vol_missing_pct_all': lst_vol_missing_pct_all,
      'vol_avg_all': lst_vol_avg_all,
      'vol_std_all': lst_vol_std_all,
      'adclose_non_null_all': lst_adclose_non_null_all,
      'adclose_missing_pct_all': lst_adclose_missing_pct_all
  })

  return result_df

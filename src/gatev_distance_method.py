import pandas as pd
import plotly.express as px
import numpy as np
import itertools
from heapq import nsmallest, nlargest

def gatev_data_normalize(
    df: pd.DataFrame, 
    visualize=True
) -> pd.DataFrame:
    
    # Compute daily returns using pandas pct_change()
    df_daily_returns = df.pct_change()
    
    # Skip first row with NA 
    df_daily_returns = df_daily_returns[1:]
    
    # Calculate the cumulative daily returns
    df_cum_daily_returns = (1 + df_daily_returns).cumprod() - 1
    
    
    df_cum_daily_returns_pct = df_cum_daily_returns.copy()
    df_cum_daily_returns_pct = df_cum_daily_returns_pct*100
    
    if visualize:
        fig = px.line(df_cum_daily_returns_pct,
              title='Performance - Daily Cumulative Returns', 
              width=1000, height=600,
              )
        fig.update_layout(yaxis_title="Daily Cumulative returns (%)")
        fig.show()
    
    return df_cum_daily_returns_pct


def gatev_distance_matrix(df: pd.DataFrame) -> None:
    
    col =  df.columns.tolist()
    
    dist_gatev = np.zeros((len(col), len(col)))
    
    keys = df.keys()
    for i in range(len(col)):
        for j in range(i+1, len(col)):
            S1 = df[keys[i]]
            S2 = df[keys[j]]
            dist = round(np.linalg.norm(S1 - S2),1)
            dist_gatev[i,j] = dist

    fig = px.imshow(dist_gatev,
                    labels=dict(x="Stock", y="Stock", color="Distance"),
                    x=col,
                    y=col,  color_continuous_scale='reds',
                width=1000, height=600)
    fig.update_xaxes(side="top")
    fig.show()
    
    
def gatev_distance_smallest(
    df: pd.DataFrame, 
    top_values: int = 10
) -> tuple:
    
    # Lấy tổ hợp chập 2 các phần tử trong danh sách các cột 
    col_combi = list(itertools.combinations(df.columns.tolist(), 2))

    # Tính khoảng cách euclide của từng cặp 
    value_list = [] 
    for col in col_combi:
        dist = round(np.linalg.norm(
            df[col[0]] - df[col[1]]), 1)
        
        value_list.append(dist)

    # Chọn ra các cặp có giá trị khoảng cách nhỏ nhất 
    top_smallest = nsmallest(top_values, value_list)
    
    # List các tổ hợp các gặp có khoảng cách ngắn nhất 
    list_smallest_pair_gatev = []
    
    # List kết quả của các cặp có khoảng cách ngắn nhất 
    list_result_smallest_dist = []
    
    for col in col_combi:
        dist = round(np.linalg.norm(
            df[col[0]] - df[col[1]]), 1)
        
        if dist in top_smallest:
            pair = [col[0], col[1]]
            list_smallest_pair_gatev.append(pair)
            list_result_smallest_dist.append(f"Khoảng cách Euclide của {col[0]} và {col[1]}: {dist}")

    return list_smallest_pair_gatev, list_result_smallest_dist
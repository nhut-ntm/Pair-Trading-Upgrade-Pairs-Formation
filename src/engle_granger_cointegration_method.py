import pandas as pd
from statsmodels.tsa.stattools import coint, adfuller
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def find_cointegrated_pairs(
    df: pd.DataFrame, 
    visualize: bool = True
) -> tuple:
    
    # Find the cointegrated pairs 
    n = df.shape[1]
    
    # Establish a zero-containing matrix 
    score_matrix = np.zeros((n, n))
    pvalue_matrix = np.ones((n, n))
    
    keys = df.keys()
    pairs = []
    
    for i in range(n):
        for j in range(i+1, n):
            
            S1 = df[keys[i]]
            S2 = df[keys[j]]
            
            result = coint(S1, S2)
            score = result[0]
            pvalue = result[1]
            score_matrix[i, j] = score
            pvalue_matrix[i, j] = pvalue
            
            if pvalue < 0.05:
                pairs.append([keys[i], keys[j]])
                
    # Visualize the pairs
    if visualize:
        tickers = df.columns.tolist()

        fig, ax = plt.subplots(figsize=(20,10))
        sns.heatmap(
            pvalue_matrix, 
            xticklabels = tickers, 
            yticklabels = tickers,
            cmap = 'RdYlGn_r',
            mask = (pvalue_matrix >= 0.05), 
            annot = True
        )

        plt.title('Engle - Granger Cointegration Test', fontsize = 20)
        plt.show()
                
    return score_matrix, pvalue_matrix, pairs

def find_cointegrated_pairs_swap(
    df: pd.DataFrame,
    visualize: bool = True
) -> tuple:
    
    # Find the cointegrated pairs 
    n = df.shape[1]
    
    score_matrix = np.zeros((n, n))
    pvalue_matrix = np.ones((n, n))
    
    keys = df.keys()
    pairs = []
    
    for i in range(n):
        for j in range(i+1, n):
            
            S1 = df[keys[i]]
            S2 = df[keys[j]]
            
            result = coint(S2, S1)
            score = result[0]
            pvalue = result[1]
            score_matrix[i, j] = score
            pvalue_matrix[i, j] = pvalue
            
            if pvalue < 0.05:
                pairs.append([keys[i], keys[j]])
    
    # Visualize the pairs
    if visualize:
        tickers = df.columns.tolist()            
        fig, ax = plt.subplots(figsize=(20,10))
        sns.heatmap(pvalue_matrix, 
                    xticklabels = tickers, 
                    yticklabels = tickers, 
                    cmap = 'RdYlGn_r', 
                    mask = (pvalue_matrix >= 0.05),
                    annot = True
                    )

        plt.title('Engle - Granger Cointegration Test (Swap)', fontsize = 20)
        plt.show()
    
    return score_matrix, pvalue_matrix, pairs
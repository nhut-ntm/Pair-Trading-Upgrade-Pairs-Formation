import pandas as pd
import seaborn as sns 
import numpy as np

def dist_stock_visualization(df: pd.DataFrame) -> None:
    
    # List các cột của dataframe 
    column_name = df.columns.tolist()
    
    # Visualize phân phối dữ liệu từng cột 
    for column in column_name:
        sns.displot(df[column], kde=True, color='purple') 
        
        
def df_natural_log_transformed(df: pd.DataFrame) -> pd.DataFrame:
    
    # Dataframe tạm: copy từ dataframe input 
    df_transformed = df.copy()
    
    # Biến đổi log cho từng cột và overwrite vào dataframe tạm 
    for column in df_transformed.columns.tolist():
        df_transformed[column] = df_transformed[column].astype(float)
        df_transformed[column] = np.log(df_transformed[column])
    
    return df_transformed
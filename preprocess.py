import pandas as pd
def dtypes_and_unique(df):
    dtypes = df.dtypes  # Store the data types of each column in a variable
    n_uniq = df.nunique()  # Count the number of unique values in each column
    
    return pd.DataFrame({'dtypes': dtypes, 'n_uniq': n_uniq}) .T  # Create a new DataFrame with the data types and number of unique values of each column
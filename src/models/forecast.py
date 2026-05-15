import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def forecast_future(df, target_col, years=5):
    # Simple forecast function
    X = df[['year']].values
    y = df[target_col].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    last_year = df['year'].max()
    future_years = np.arange(last_year + 1, last_year + years + 1)
    predictions = model.predict(future_years.reshape(-1, 1))
    
    return predictions, model.score(X, y)
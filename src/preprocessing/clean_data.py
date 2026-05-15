import pandas as pd

def load_and_clean_data():
    # Load your CSV file - fix the path
    df = pd.read_csv('data/raw/pakistan_tourism_dataset.csv')
    
    # Basic cleaning
    df = df.drop_duplicates()
    
    return df
# convenience_store.py

import pandas as pd

# Load the convenience store dataset
convenience_store_data = pd.read_csv('pharmacy.csv')

# Perform any necessary preprocessing steps
convenience_store_data['Date'] = pd.to_datetime(convenience_store_data['Date'])
convenience_store_data['Product'] = convenience_store_data['Product'].apply(eval)

# Print the first few rows of the dataset
print("Convenience Store Dataset:")
print(convenience_store_data.head())
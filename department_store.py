# convenience_store.py

import pandas as pd

# Load the convenience store dataset
department_store_data = pd.read_csv('department_store.csv')
import syft as sy
import torch

hook = sy.TorchHook(torch)
department_store_party = hook.local_worker

# Perform any necessary preprocessing steps
department_store_data['Date'] = pd.to_datetime(department_store_data['Date'])
department_store_data['Product'] = department_store_data['Product'].apply(eval)

convenience_store_ptr = department_store_party.send(department_store_data, worker=hook.get_worker('coordinator'))


# Print the first few rows of the dataset
print("Convenience Store Dataset:")
print(convenience_store_data.head())

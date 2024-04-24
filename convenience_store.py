# convenience_store.py
from phe import paillier
import pandas as pd
import numpy as np
from collections import Counter
from tno.mpc.encryption_schemes.paillier import Paillier

store_data = pd.read_csv('pharmacy.csv')

store_data['Product'] = store_data['Product'].apply(eval)
store_data = store_data['Product']
consolidated_list = []
for product_list in store_data:

    for product in product_list:
        consolidated_list.append(product.strip())
scheme_paillier = Paillier.from_security_parameter(key_length=2048)
consolidated_list = np.array(consolidated_list)
product_counts = Counter(consolidated_list)
unique_products = dict(product_counts)

print(unique_products['Hair Gel'])











import asyncio

from tno.mpc.communication import Pool
import pandas as pd
import numpy as np
from collections import Counter

async def async_main():
    # Create the pool for Alice.
    # Alice listens on port 61001 and adds Bob as client.
    pool = Pool()
    pool.add_http_server(addr="127.0.0.1", port=61001)
    pool.add_http_client("Bob", addr="127.0.0.1", port=61002)


    store_data = pd.read_csv('../convenience_store.csv')

    store_data['Product'] = store_data['Product'].apply(eval)
    store_data = store_data['Product']
    consolidated_list = []
    for product_list in store_data:

        for product in product_list:
            consolidated_list.append(product.strip())

    consolidated_list = np.array(consolidated_list)
    product_counts = (Counter(consolidated_list))
    unique_products = {str(key): value for key, value in product_counts.items()}
    print(unique_products)


    # Alice sends a message to Bob and waits for a reply.
    # She prints the reply and shuts down the pool
    await pool.send("Bob",unique_products)
    reply = await pool.recv("Bob")
    print(reply)
    await pool.shutdown()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main())
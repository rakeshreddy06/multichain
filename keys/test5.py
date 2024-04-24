import argparse
import asyncio
from typing import List, Tuple

from tno.mpc.communication import Pool

from tno.mpc.protocols.distributed_keygen import DistributedPaillier
import pandas as pd
import numpy as np
from collections import Counter
corruption_threshold = 1  # corruption threshold
key_length = 128  # bit length of private key
prime_thresh = 2000  # threshold for primality check
correct_param_biprime = 40  # correctness parameter for biprimality test
stat_sec_shamir = (
    40  # statistical security parameter for secret sharing over the integers
)


def setup_local_pool(server_port: int, others: List[Tuple[str, int]]) -> Pool:
    pool = Pool()
    pool.add_http_server(server_port)
    for client_ip, client_port in others:
        print(f"client_{client_port}", client_ip, client_port)
        pool.add_http_client(
            f"client_{client_port}", client_ip, client_port
        )
    return pool


# REGION EXAMPLE SETUP
# this region contains code that is used for the toy example, but can be deleted when the `others`
# variable underneath the region is set to the proper values.

parser = argparse.ArgumentParser(description="Set the parameters to run the protocol.")

parser.add_argument(
    "--party",
    type=int,
    help="Identifier for this party. This should be different for all scripts but should be in the "
         "set [0, ..., nr_of_parties - 1].",
)

parser.add_argument(
    "--nr_of_parties",
    type=int,
    help="Total number of parties involved. This should be the same for all scripts.",
)

parser.add_argument(
    "--base-port",
    type=int,
    default=8888,
    help="port first player used for communication, incremented for other players"
)

args = parser.parse_args()
party_number = args.party
nr_of_parties = args.nr_of_parties

base_port = args.base_port
# ENDREGION

# Change this to the ips and server ports of the other machines
others = [
    ("localhost", base_port + i) for i in range(nr_of_parties) if i != party_number
]

# Change this to the port you want this machine to listen on (note that this should correspond
# to the port of this party in the scripts on the other machines)
server_port = base_port + party_number
pool = setup_local_pool(server_port, others)

loop = asyncio.get_event_loop()


async def main(pool):
    distributed_paillier = await DistributedPaillier.from_security_parameter(
        pool,
        corruption_threshold,
        key_length,
        prime_thresh,
        correct_param_biprime,
        stat_sec_shamir,
        precision=8,
        distributed=True,
    )
    # Party 3
    # Party 2
    store_data = pd.read_csv(r'C:\Users\rakes\PycharmProjects\DPS-project\pharmacy.csv')

    store_data['Product'] = store_data['Product'].apply(eval)
    store_data = store_data['Product']
    consolidated_list = []
    for product_list in store_data:

        for product in product_list:
            consolidated_list.append(product.strip())

    consolidated_list = np.array(consolidated_list)
    product_counts = Counter(consolidated_list)
    current_unique_products = dict(product_counts)
    for key, value in current_unique_products.items():
        current_unique_products[key] = distributed_paillier.encrypt(value)

    # The assumption here is that this code is placed inside an async method
    unique_products = await distributed_paillier.pool.recv("client_8889",
                                                            msg_id="step2")  # receive the ciphertext from party 1

    for key, value in current_unique_products.items():
        if key in unique_products:
            unique_products[key] += value
        else:
            unique_products[key] = value



    # send the ciphertext to multiple parties (we cannot use `pool.send` now).
    await distributed_paillier.pool.broadcast(unique_products, msg_id="step3",
                                              handler_names=["client_8888",
                                                             "client_8889"])  # receivers=None does the same

    decrypted_values = {}
    for key, encrypted_value in unique_products.items():
        decrypted_value = await distributed_paillier.decrypt(encrypted_value)
        decrypted_values[key] = decrypted_value

    print(decrypted_values)


distributed_paillier_scheme = loop.run_until_complete(main(pool))

from phe import paillier

def encrypt_dict(public_key, dictionary):
    encrypted_dict = {}
    for key, value in dictionary.items():
        encrypted_dict[key] = public_key.encrypt(value)
    return encrypted_dict

def merge_encrypted_dicts(public_key, dict1, dict2):
    merged_dict = {}
    for key in set(dict1.keys()) | set(dict2.keys()):
        encrypted_value1 = dict1.get(key, public_key.encrypt(0))
        encrypted_value2 = dict2.get(key, public_key.encrypt(0))
        merged_dict[key] = encrypted_value1 + encrypted_value2
    return merged_dict

def partial_decrypt(private_key_share, encrypted_dict):
    partially_decrypted_dict = {}
    for key, value in encrypted_dict.items():
        partially_decrypted_dict[key] = private_key_share.decrypt(value)
    return partially_decrypted_dict

def merge_partially_decrypted_dicts(dict1, dict2):
    merged_dict = {}
    for key in set(dict1.keys()) | set(dict2.keys()):
        value1 = dict1.get(key, 0)
        value2 = dict2.get(key, 0)
        merged_dict[key] = value1 * value2
    return merged_dict

def find_highest_count_item(merged_dict):
    return max(merged_dict, key=merged_dict.get)

# Generate Paillier key pair
public_key, private_key = paillier.generate_paillier_keypair(n_length=2048)

# Split the private key into two shares
private_key_shares = private_key.split(2, 2)

# Distribute the private key shares to the parties
private_key_share1 = private_key_shares[0]
private_key_share2 = private_key_shares[1]

# Example dictionaries for each party
dict_party1 = {'apple': 3, 'banana': 2, 'orange': 1}
dict_party2 = {'apple': 2, 'banana': 4, 'grape': 3}

# Encrypt the dictionaries for each party using the public key
encrypted_dict_party1 = encrypt_dict(public_key, dict_party1)
encrypted_dict_party2 = encrypt_dict(public_key, dict_party2)

# Merge the encrypted dictionaries
merged_encrypted_dict = merge_encrypted_dicts(public_key, encrypted_dict_party1, encrypted_dict_party2)

# Partial decryption by each party using their respective private key shares
partially_decrypted_dict1 = partial_decrypt(private_key_share1, merged_encrypted_dict)
partially_decrypted_dict2 = partial_decrypt(private_key_share2, merged_encrypted_dict)

# Merge the partially decrypted dictionaries
merged_dict = merge_partially_decrypted_dicts(partially_decrypted_dict1, partially_decrypted_dict2)

# Find the item with the highest count
highest_count_item = find_highest_count_item(merged_dict)

print("Item with the highest count:", highest_count_item)
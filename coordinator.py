from phe import paillier

def encrypt_dict(public_key, dictionary):
    encrypted_dict = {}
    for key, value in dictionary.items():
        encrypted_dict[key] = public_key.encrypt(value)
    return encrypted_dict

def merge_encrypted_dicts(dict1, dict2):
    merged_dict = {}
    for key in set(dict1.keys()) | set(dict2.keys()):
        merged_dict[key] = dict1.get(key, 0) + dict2.get(key, 0)
    return merged_dict

def find_highest_count_item(private_key, encrypted_dict):
    decrypted_dict = {}
    for key, encrypted_value in encrypted_dict.items():
        decrypted_dict[key] = private_key.decrypt(encrypted_value)
    return max(decrypted_dict, key=decrypted_dict.get)

# Generate Paillier key pair
public_key, private_key = paillier.generate_paillier_keypair()

# Example dictionaries
dict1 = {'apple': 3, 'banana': 2, 'orange': 1}
dict2 = {'apple': 2, 'banana': 4, 'grape': 3}

# Encrypt the dictionaries
encrypted_dict1 = encrypt_dict(public_key, dict1)
encrypted_dict2 = encrypt_dict(public_key, dict2)

# Merge the encrypted dictionaries
merged_encrypted_dict = merge_encrypted_dicts(encrypted_dict1, encrypted_dict2)

# Find the item with the highest count
highest_count_item = find_highest_count_item(private_key, merged_encrypted_dict)

print("Item with the highest count:", highest_count_item)
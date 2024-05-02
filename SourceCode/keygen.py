import shamirs
from phe import paillier
from pyshamir import split, combine

import sympy

# Generate a large prime number of approximately 2048 bits in size
large_prime = sympy.randprime(2**2047, 2**2048)


# Example secret to split (in practice, this would be a critical part of your private key)
public_key, private_key = paillier.generate_paillier_keypair(n_length=1024)
print(private_key.p)


ss = shamirs.shares(private_key.p, quantity=3,modulus=large_prime,threshold=2)
ss=list(ss)
print(ss[0])

print(shamirs.interpolate(ss))




#!/usr/bin/env python3
import ecdsa
from hashlib import sha256, new
import codecs
# https://github.com/warner/python-ecdsa this is the ecdsa library, since pycrypto doesn't have it
# helpful https://medium.freecodecamp.org/how-to-create-a-bitcoin-wallet-address-from-a-private-key-eca3ddd9c05f

# from https://github.com/Destiner/blocksmith/blob/master/blocksmith/bitcoin.py
def base58(address_hex):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    b58_string = ''
    leading_zeros = len(address_hex) - len(address_hex.lstrip('0'))
    address_int = int(address_hex, 16)
    while address_int > 0:
        digit = address_int % 58
        digit_char = alphabet[digit]
        b58_string = digit_char + b58_string
        address_int //= 58
    # Adding '1' for each 2 leading zeros
    ones = leading_zeros // 2
    for one in range(ones):
        b58_string = '1' + b58_string
    return b58_string

# SECP256k1 is the Bitcoin elliptic curve
key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
#print(key.to_der())
key = key.to_der()

# If you already have a compressed key:
# key = bytearray.fromhex('02f273a2050dce3b71b406a096b2ac33827eeb0663082ad920102eb006149716fe')

ripe_fruit = new('ripemd160', sha256(key).digest())

ripe_fruit = b'00' + codecs.encode(ripe_fruit.digest(), 'hex')
ripe_fruit += codecs.encode(sha256(sha256(codecs.decode(ripe_fruit, 'hex')).digest()).digest(), 'hex')[:8]
print(base58(ripe_fruit.decode('utf-8')))
# It actually works!!! Finally!

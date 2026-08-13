import os
from Crypto.Cipher import AES

flag_charset = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz{}_"
flag = os.environ.get("FLAG", "Alpaca{_________DUMMY_________}").encode()

assert flag.startswith(b"Alpaca{") and flag.endswith(b"}")
assert len(flag) == 31
assert all(c in flag_charset for c in flag)

key = os.urandom(16)
iv = os.urandom(16)
cipher = AES.new(key, AES.MODE_CBC, iv)


msg = b"FLAG IS:" + flag
msg_16 = msg * 16

ciphertext = cipher.encrypt(msg_16)
print(f"iv(hex): {cipher.iv.hex()}")
print(f"ciphertext(hex): {ciphertext.hex()}")

while True:
    user_input = bytes.fromhex(input("plaintext to encrypt (hex): "))

    if len(user_input) != 16:
        print("Input must be 16 bytes (32 hex characters).")
        continue

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(user_input)
    print(f"iv(hex): {cipher.iv.hex()}")
    print(f"ciphertext(hex): {ciphertext.hex()}")

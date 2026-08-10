from pwn import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-R", action="store_true")
args = parser.parse_args()

REMOTE_HOST = "34.170.146.252"
REMOTE_PORT = 57189
LOCAL_HOST = "localhost"
LOCAL_PORT = 1337

if args.R:
    r = remote(REMOTE_HOST, REMOTE_PORT)
else:
    r = process(["python3", "server.py"])

flag_charset = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz{}_"

r.recvuntil(b"iv(hex): ")
iv = bytes.fromhex(r.recvline().strip())

r.recvuntil(b"ciphertext(hex): ")
ct = bytes.fromhex(r.recvline().strip())

target_blocks = [ct[i:i+16] for i in range(0, len(ct), 16)]

H, W = 39, 16
blocks_end_idx = []
for i in range(H):
    blocks_end_idx.append(((i + 1) * W - 1) % H)
print (f"blocks_end_idx: {blocks_end_idx}")

def get_block_index(idx):
    for i in range(H):
        if blocks_end_idx[i] == idx:
            return i
    return -1

print(f"iv: {iv.hex()}")
print(f"ciphertext: {ct.hex()}")

flag = b"Alpaca{"

while len(flag) < 31:
    current = b"FLAG IS:" + flag

    idx = len(current) # 何文字目を特定するか 0-indexed
    block_idx = get_block_index(idx) # 今回検証に使うブロック番号

    prev_block = target_blocks[block_idx - 1] if block_idx > 0 else iv
    target_block = target_blocks[block_idx]

    ok = False
    for char in flag_charset:
        guess_char = bytes([char])

        guess = current[-15:] + guess_char

        p = xor(xor(guess, prev_block), iv)

        print(f"Trying character: {guess_char.decode()} -> plaintext: {p.hex()}")
        r.sendlineafter(b"plaintext to encrypt (hex): ", p.hex().encode())

        r.recvuntil(b"ciphertext(hex): ")
        res = bytes.fromhex(r.recvline().strip())

        if res == target_block:
            flag += guess_char
            print(f"Found character: {guess_char.decode()}")
            ok = True
            break

    if not ok:
        print("No matching character found, something went wrong.")
        break

print(f"Recovered flag: {flag.decode()}")

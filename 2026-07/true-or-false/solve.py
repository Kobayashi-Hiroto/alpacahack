from pwn import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-R", action="store_true")
args = parser.parse_args()

REMOTE_HOST = "34.170.146.252"
REMOTE_PORT = 33037
LOCAL_HOST = "localhost"
LOCAL_PORT = 1337

if args.R:
    r = remote(REMOTE_HOST, REMOTE_PORT)
else:
    r = remote(LOCAL_HOST, LOCAL_PORT)

MAX_EVALS = 28
min = 0
max = 2**44

for _ in range(MAX_EVALS):
    r.recvuntil(b"Eval > ")

    m1 = min + (max - min) // 3
    m2 = min + 2 * (max - min) // 3

    input = f"2/((a<{m1})+(a<{m2}))-1"
    # [0...m1) -> 2, [m1..m2) -> 1, [m2..max) -> 0
    # [0...m1) -> 1, [m1..m2) -> 2, [m2..max) -> error
    # [0...m1) -> 0, [m1..m2) -> 1, [m2..max) -> error
    # [0...m1) -> False, [m1..m2) -> True, [m2..max) -> error

    print(f"Sending: {input}")
    r.sendline(input.encode())
    res = r.recvline().strip()
    print(res.decode())

    if res == b"True":
        min = m1
        max = m2
    elif res == b"False":
        max = m1
    elif res == b"Error":
        min = m2

    print(f"m1: {m1}, m2: {m2} New range: [{min}, {max})")

r.recvuntil(b"Guess > ")
r.sendline(str(min).encode())
res = r.recvline().strip()
print(res.decode())

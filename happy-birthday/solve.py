#!/usr/bin/env python3
from hashlib import sha256


def H(m: bytes) -> bytes:
    return sha256(m).digest()[:5]


def find_collision(prefix_a=b"user=", prefix_b=b"admin=", limit=1_000_000):
    seen = {}

    for i in range(limit):
        payload = prefix_a + str(i).encode()
        h = H(payload)
        seen.setdefault(h, payload)

    for i in range(limit):
        payload = prefix_b + str(i).encode()
        h = H(payload)
        if h in seen:
            return seen[h], payload, h

    return None


def main():
    result = find_collision(limit=1_000_000)
    if result is None:
        print("collision not found")
        return

    a, b, h = result
    print(f"hash={h.hex()}")
    print(f"a={a!r}")
    print(f"b={b!r}")


if __name__ == "__main__":
    main()

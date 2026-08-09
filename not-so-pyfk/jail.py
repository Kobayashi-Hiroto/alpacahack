code = input("jail > ")

if not code.isascii():
    # Why? Because https://alpacahack.com/daily/challenges/super-short-system-exit
    print("Not ascii")
    exit()

if len(set(c for c in code if c.isalpha())) > 3:
    print("Too many alphabets")
    exit()

eval(code)
import secrets

FLAG = "Alpaca{REDACTED}"
MAX_EVALS = 28

ALLOWED_CHARS = (
    "0123456789"
    "a"
    "+-*/()<>="
)

a = secrets.randbelow(2**44)

for _ in range(MAX_EVALS):
    code = input("Eval > ")

    if any(c not in ALLOWED_CHARS for c in code):
        print("Not allowed")
        continue

    try:
        print(bool(eval(code, {"a": a, "__builtins__": {}})))
    except Exception:
        print("Error")

guess = int(input("Guess > "))

if guess == a:
    print(f"Well done! Here's your flag: {FLAG}")
else:
    print("Wrong")
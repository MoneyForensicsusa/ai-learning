import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv('GITHUB_TOKEN')
headers = {'Authorization': f'token {token}'}

try:
    response = requests.get('https://api.github.com/users/torvalds')
    if response.status_code == 200:
        data = response.json()
        print(f'Name: {data["name"]}')
        print(f'Repos: {data["public_repos"]}')
    else:
        print(f'Error Code: {response.status_code}')
except requests.exceptions.ConnectionError:
    print("Cannot connect - check your internet")

try:
    params = {'q': 'python fastapi', 'sort': 'stars', 'per_page': 3}
    response = requests.get('https://api.github.com/search/repositories', params=params, headers=headers)
    if response.status_code == 200:
        results = response.json()
        for repo in results['items']:
            print(f'{repo["name"]}: {repo["stargazers_count"]} stars')
    else:
        print(f'Error Code: {response.status_code}')
except requests.exceptions.ConnectionError:
    print("Cannot connect - check your internet")

try:
    payload = {'title': 'Test Post', 'body': 'Hello API', 'userId': 1}
    response = requests.post('https://jsonplaceholder.typicode.com/posts', json=payload)
    if response.status_code == 201:
        print(f'Created: {response.status_code}')
    else:
        print(f'Unexpected status: {response.status_code}')
except requests.exceptions.ConnectionError:
    print("Cannot connect - check your internet")
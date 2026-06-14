import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv('GITHUB_TOKEN')
headers = {'Authorization': f'token {token}'}

def get_repo(owner, repo):
    try:
        response = requests.get(f"https://api.github.com/repos/{owner}/{repo}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            return {
                'name': data.get('name', 'No name'),
                'description': data.get('description', 'No description'),
                'stars': data.get('stargazers_count', 0)
            }
        else:
            print(f"Error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print('Cannot connect - check your internet')
repo_info = get_repo("MoneyForensicsusa", "ai-learning")
print(repo_info) 

try:
    response = requests.get('https://jsonplaceholder.typicode.com/posts?userId=1')
    if response.status_code == 200:
        data = response.json()
        post_count = (len(data))
        print(post_count)
    else:
        print(f"Error: {response.status_code}")
except requests.exceptions.ConnectionError:
    print('Cannot Connect - check your internet')

def store_github_info(usernames):
    profiles = []
    for username in usernames:
        try:
            response = requests.get(f'https://api.github.com/users/{username}')
            if response.status_code == 200:
                data = response.json()
                profiles.append({
                    "name": data.get("name", "No name"),
                    "bio": data.get("bio", "No bio"),
                    "follower count": data.get("followers", 0)
            })
        except requests.exceptions.ConnectionError:
            print(f"Cannot connect for {username}")
    with open('github_profiles.json', 'w') as f:
        json.dump(profiles, f, indent=2)
    return profiles
usernames = ['torvalds', 'gvanrossum', 'tiangolo', 'yoheinakajima', 'MoneyForensicsusa']
store_github_info(usernames)
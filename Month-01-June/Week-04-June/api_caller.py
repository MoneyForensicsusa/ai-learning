import requests

def get_github_user(username):
    url = f"https://api.github.com/users/{username}"
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        return f"Network error - check your connection"
    
    if response.status_code != 200:
        return f"Error: status code {response.status_code}"

    data = response.json()
    return {
        "name": data.get("name", "No name set"),
        "public_repos": data.get("public_repos", 0),
        "followers": data.get("followers", 0)
    }

usernames = ["torvalds","MoneyForensicsusa", "gssu"]

for username in usernames:
    user = get_github_user(username)
    if isinstance(user, dict):
         print(f"Name:    {user['name']}")
         print(f"Repos:    {user['public_repos']}")
         print(f"Followers:    {user['followers']}")
    else:
        print(user)
    print("-------")

import requests

def profile_page_generator(username):
    url = f"https://api.github.com/users/{username}"
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        return f"Error: Could not connect to GitHub"
    
    if response.status_code != 200:
        return f"Error : status code {response.status_code}"
    
    data = response.json()
    user = {
        "name": data.get("name", "no name set"),
        "bio": data.get("bio", "no bio"),
        "repo count": data.get("public_repos", 0)
    }

    with open("profiles.txt","a") as p:
        p.write(f"Name: {user['name']}\n")
        p.write(f"Bio: {user['bio']}\n")
        p.write(f"Repos: {user['repo count']}\n")
        p.write("---------\n")
    
usernames = ["torvalds", "MoneyForensicsusa", "gvanrossum"]
for username in usernames:
    profile_page_generator(username)

with open("profiles.txt", "r") as p:
        text = p.read()
        print(text)
    


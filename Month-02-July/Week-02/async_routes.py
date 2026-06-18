from fastapi import FastAPI
import httpx
import asyncio

app = FastAPI()

@app.get('/health')
def health_check():
    return {'status': 'ok'}

@app.get('/github/{username}')
async def get_github_profile(username: str):
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get(f'https://api.github.com/users/{username}')
            if response.status_code != 200:
                return {'error': 'User not found'}
            data = response.json()
            return {
                'name': data.get('name'),
                'repos': data.get('public_repos'),
                'followers': data.get('followers')
            }
    except httpx.TimeoutException:
        return{'Error': 'Server took too long'}

@app.get('/compare/{user1}/{user2}')
async def compare_users(user1: str, user2: str):
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            r1, r2 = await asyncio.gather(
                client.get(f'https://api.github.com/users/{user1}'),
                client.get(f'https://api.github.com/users/{user2}')
            )
            d1, d2 = r1.json(), r2.json()
            return {
                user1 : {'repos': d1.get('public_repos'), 'followers': d1.get('followers')},
                user2 : {'repos': d2.get('public_repos'), 'followers': d2.get('followers')}
            }
    except httpx.TimeoutException:
        return {'Error': 'Server took too long'}

@app.get('/compare-sync/{user1}/{user2}')
def compare_sync(user1: str, user2: str):
        import requests
        r1 = requests.get(f'https://api.github.com/users/{user1}')
        r2 = requests.get(f'https://api.github.com/users/{user2}')
        d1 = r1.json()
        d2 = r2.json()
        return {
            user1: d1.get('public_repos'),
            user2: d2.get('public_repos')
        }
    

@app.get('/github/{username}/repos')
async def get_user_repos_more_than_100_stars(username: str):
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get(f'https://api.github.com/users/{username}/repos')
            repos = response.json()
            result = []
            for repo in repos:
                if repo['stargazers_count'] > 100:
                    result.append({'name': repo.get('name', 'No name')})
            return result
    except httpx.TimeoutException:
        return {'error': 'server took too long'}
        
@app.get('/batch/{users}')
async def get_github_profiles(users: str):
    try:
        users_list = [user.strip() for user in users.split(',')]
        async with httpx.AsyncClient(timeout=3.0) as client:
            tasks = []
            for user in users_list:
                tasks.append(client.get(f'https://api.github.com/users/{user}'))
            responses = await asyncio.gather(*tasks)
        result = []
        for response in responses:
            if response.status_code == 200:
                data = response.json()
                result.append({'username': data.get('login'), 'repos': data.get('public_repos')})
        return result
    except httpx.TimeoutException:
        return {'user': 'server took too long'}
            






            
from fastapi import FastAPI
import httpx
import asyncio

app = FastAPI()

@app.get('/health')
def health_check():
    return {'status': 'ok'}

@app.get('/github/{username}')
async def get_github_profile(username: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'https://api.github.com/users/{username}')
        if response.status_code != 200:
            return {'error': 'User not found'}
        data = response.json()
        return {
            'name': data.get('name'),
            'repos': data.get('public_repos'),
            'followers': data.get('followers')
        }

@app.get('/compare/{user1}/{user2}')
async def compare_users(user1: str, user2: str):
    async with httpx.AsyncClient() as client:
        r1, r2 = await asyncio.gather(
            client.get(f'https://api.github.com/users/{user1}'),
            client.get(f'https://api.github.com/users/{user2}')
        )
        d1, d2 = r1.json(), r2.json()
        return {
            user1 : {'repos': d1.get('public_repos'), 'followers': d1.get('followers')},
            user2 : {'repos': d2.get('public_repos'), 'followers': d2.get('followers')}
        }

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
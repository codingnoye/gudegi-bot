import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs
import json
from typing import List, Dict

async def getSolvedProblems(handle: str) -> List[str]:
    # Cost: 1 boj request
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://www.acmicpc.net/user/{handle}') as res:
            soup = bs(await res.text(), 'html.parser')

    elems = soup.select('.panel:first-child a')
    problems = set(int(elem.text) for elem in elems)
    return problems

async def getProblemData(problemId: int) -> dict:
    # Cost: 1 solved.ac request
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://solved.ac/api/v3/search/problem?query={problemId}&page=1') as res:
            data = json.loads(await res.text())

    for problem in data['items']:
        if problem['problemId'] == problemId:
            return problem
    return None

async def getUserData(handle: str) -> dict:
    # Cost: 1 solved.ac request
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://solved.ac/api/v3/user/show?handle={handle}') as res:
            data = await res.text()
    try:
        data = json.loads(data)
        return data
    except:
        return None

async def getSolvedCount(handle: str) -> int:
    # Cost: 1 solved.ac request
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://solved.ac/api/v3/search/problem?query=solved_by:{handle}&page=1') as res:
            data = await res.text()
    try:
        data = json.loads(data)
        return data['count']
    except:
        return None

if __name__ == '__main__':
    async def main():
        #print(await getSolvedProblems('noye'))
        #print(await getUserData('cod3holic'))
        print(await getProblemData(1234))
    asyncio.run(asyncio.wait([main()]))
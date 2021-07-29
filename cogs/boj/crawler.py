import asyncio
from asyncio.tasks import Task
from cogs.boj.user import User
from typing import Callable, Dict
from cogs.boj.parsers import getSolvedCount, getUserData, getSolvedProblems

class Crawler:
    task: Task
    users: Dict[str, User] 
    callback: Callable
    def start(self, users, callback: Callable):
        self.users = users
        self.callback = callback
        loop = asyncio.get_event_loop()
        self.task = loop.create_task(self.crawling())

    async def crawling(self):
        while True:
            for handle in self.users:
                user: User = self.users[handle]
                userdata = await getUserData(user.handle)
                if userdata is None: continue
                print(f'{user.handle}: solved {userdata["solvedCount"]} problems')
                if userdata['solvedCount'] != user.solved_count:
                    solved_problems = await getSolvedProblems(user.handle)
                    if len(solved_problems) == 0: continue
                    for prob_num in solved_problems^user.solved_problems:
                        await self.callback(user, prob_num)
                    user.solved_problems = solved_problems
                    user.solved_count = userdata['solvedCount']
                await asyncio.sleep(20)
            
            await asyncio.sleep(300)

    def stop(self):
        self.task.cancel()
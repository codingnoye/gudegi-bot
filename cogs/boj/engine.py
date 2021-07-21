from discord import Embed
from discord.ext.commands.bot import Bot
from discord_slash.model import ButtonStyle
from discord_slash.utils import manage_components
from cogs.boj.crawler import Crawler
from typing import List, Set, Dict
from cogs.boj.parsers import getProblemData, getSolvedProblems, getUserData
import asyncio
import os, pickle
from cogs.boj.user import User
import cogs.boj.tiers as tiers

class Engine:
    bot: Bot
    users: Dict[str, User]
    fdir: str
    def __init__(self, bot: Bot):
        self.bot = bot
        self.fdir = f'{os.path.dirname(os.path.abspath(__file__))}/data/user'
        if os.path.isfile(self.fdir):
            with open(self.fdir, 'rb') as f:
                self.users = pickle.load(f)
        else:
            self.users = dict()
    
    def __del__(self):
        with open(self.fdir, 'wb') as f:
            pickle.dump(self.users, f)

    def start_crawling(self):
        crawl = Crawler()
        async def callback(user:User, prob_id:int):
            problem = await getProblemData(prob_id)
            tier, number, color = tiers.level_to_tier(problem['level'])
            emoji = tiers.find_emoji(self.bot, problem['level'])
            embed = Embed(title=f'{user.handle}님이 문제를 풀었습니다!',
                description=f'**#{prob_id}** {problem["titleKo"]} {emoji}',
                color=color)
            embed.add_field(name='푼 사람 수', value=f'{problem["acceptedUserCount"]:,}명')
            embed.add_field(name='나도 풀러 가기', value=f'[https://www.acmicpc.net/problem/{prob_id}](https://www.acmicpc.net/problem/{prob_id})', inline=False)
            for channel in user.channels:
                await self.bot.get_channel(id=channel).send(embed=embed)
                
        crawl.start(self.users, callback)

    async def adduser(self, handle:str, channel:str):
        if handle in self.users:
            self.users[handle].channels.add(channel)
        else:
            userdata, solved_problems = await asyncio.gather(getUserData(handle), getSolvedProblems(handle))
            self.users[handle] = User(handle, {channel}, userdata['solvedCount'], solved_problems)
        with open(self.fdir, 'wb') as f:
            pickle.dump(self.users, f)
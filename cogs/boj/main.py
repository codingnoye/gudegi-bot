from logging import disable
from discord import Embed, User, user
from discord_slash import cog_ext, SlashContext
from discord_slash.cog_ext import cog_component
from discord_slash.context import ComponentContext
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils import manage_commands, manage_components
from discord_slash.utils.manage_components import wait_for_component
from discord_slash.model import ButtonStyle
from discord.ext import commands
import os
from cogs.boj.engine import Engine
import cogs.boj.tiers as tiers

from cogs.boj.parsers import getProblemData, getSolvedProblems, getUserData

TEST_GUILD_IDS = list(map(int, os.getenv('TEST_GUILD_IDS').split()))

class Boj(commands.Cog):
    engine: Engine
    def __init__(self, bot):
        self.bot = bot
        self.engine = Engine(bot)

    @commands.Cog.listener()
    async def on_ready(self):
        self.engine.start_crawling()

    @cog_ext.cog_subcommand(base='boj',
        name='user',
        description='사용자 정보를 가져옵니다.',
        guild_ids=TEST_GUILD_IDS, options=[
            create_option(
                name = 'handle',
                description = '사용자명',
                option_type = 3,
                required = True
            )
        ]
    )
    async def _user(self, ctx: SlashContext, handle: str):
        userdata = await getUserData(handle)
        if userdata is None:
            embed = Embed(title = f'{handle}')
            embed.add_field(name='오류', value='사용자를 찾을 수 없습니다.')
            await ctx.send(embed=embed)
        else:
            tier, number, color = tiers.level_to_tier(userdata['tier'])
            emoji = tiers.find_emoji(ctx.bot, userdata['tier'])
            embed = Embed(title = f'**{handle}** {emoji}',
                color=color
                )
            if userdata['bio'] != '':
                embed.description = f'"{userdata["bio"]}"'
            if userdata['badge'] is not None:
                embed.set_thumbnail(url=userdata['badge']['badgeImageUrl'])
            embed.add_field(name='AC rating', value=f'**{userdata["rating"]:,}** (#{userdata["rank"]:,})')
            embed.add_field(name='푼 문제 수', value=f'{userdata["solvedCount"]:,} 문제')

            disabled_btn = manage_components.create_button(
                style=ButtonStyle.success,
                label=f'{handle} 알림 등록 완료',
                custom_id=f'addUser',
                disabled=True
            )
            btns = []
            btns.append(manage_components.create_button(
                style=ButtonStyle.blurple,
                label=f'이 채널에서 {handle} 알림 등록',
                custom_id=f'addUser'
            ))
            btns.append(manage_components.create_button(
                style=ButtonStyle.URL,
                label=f'{handle} on BOJ',
                url=f'https://www.acmicpc.net/user/{handle}'
            ))
            btns.append(manage_components.create_button(
                style=ButtonStyle.URL,
                label=f'{handle} on solved.ac',
                url=f'https://solved.ac/profile/{handle}'
            ))
            if handle in self.engine.users and ctx.channel.id in self.engine.users[handle].channels:
                btns[0] = disabled_btn
            await ctx.send(embed=embed, components=manage_components.spread_to_rows(*btns, max_in_row=3))
            req = await wait_for_component(ctx.bot, components=btns[0])
            btns[0] = disabled_btn
            await self.engine.adduser(handle, req.channel.id)
            await req.edit_origin(components=manage_components.spread_to_rows(*btns, max_in_row=3))

    @cog_ext.cog_subcommand(base='boj',
        name='problem',
        description='문제 정보를 가져옵니다.',
        guild_ids=TEST_GUILD_IDS, options=[
            create_option(
                name = 'id',
                description = '문제 id',
                option_type = 4,
                required = True
            )
        ])
    async def _prob(self, ctx: SlashContext, id: int):
        problem = await getProblemData(id)
        if problem is None:
            embed = Embed(title = f'#{id}')
            embed.add_field(name='오류', value='문제를 찾을 수 없습니다.')
        else:
            tier, number, color = tiers.level_to_tier(problem['level'])
            emoji = tiers.find_emoji(ctx.bot, problem['level'])
            embed = Embed(title = f'{problem["titleKo"]} {emoji}',
                description=f'#{id}',
                color=color
            )
            embed.add_field(name='푼 사람 수', value=f'{problem["acceptedUserCount"]:,}명')
            btn = manage_components.create_button(
                style=ButtonStyle.URL,
                label=f'{problem["titleKo"]} on BOJ',
                url=f'https://www.acmicpc.net/problem/{id}'
            )
            await ctx.send(embed=embed, components=manage_components.spread_to_rows(btn))

def setup(bot):
    bot.add_cog(Boj(bot))
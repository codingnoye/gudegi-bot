import discord
from discord_slash import SlashCommand
from discord.ext import commands

from dotenv import load_dotenv
import os
load_dotenv(verbose=True)
APP_ID = os.getenv('APP_ID')
BOT_TOKEN = os.getenv('BOT_TOKEN')
TEST_GUILD_ID = int(os.getenv('TEST_GUILD_ID'))

bot = commands.Bot(
    command_prefix="",
    intents=discord.Intents.all(),
    allowed_mentions=discord.AllowedMentions(everyone=True),
    help_command=None,
)
slash = SlashCommand(bot, sync_commands=True)

@bot.event
async def on_ready():
    print("Ready!")

@slash.slash(name="ping", guild_ids=[TEST_GUILD_ID])
async def _ping(ctx):
    await ctx.send(f"Pong! ({bot.latency*1000}ms)")

bot.load_extension("cogs.boj.main")
bot.run(BOT_TOKEN)
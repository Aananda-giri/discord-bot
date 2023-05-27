import interactions
import discord
from discord.ext import commands
import config, asyncio
from cogs.functions import get_embeded_message
config.init()

bot = commands.Bot(command_prefix="!", description="The description", intents=config.intents)
# bot = discord.Client()

@bot.event
async def  on_ready():
    print("Ready !")
    # await bot.interactions.sync_all_commands()
    await bot.tree.sync() # sync CommandTree in order for slash commands to appear : https://discordpy.readthedocs.io/en/v2.2.2/ext/commands/commands.html#hybrid-commands

import math, asyncpraw, asyncprawcore


@bot.hybrid_command(name='ping', description='test')
async def ping(ctx, what='pong'):
    await ctx.send(embed= get_embeded_message(ctx, 'ping-pong', f'this is body, what:{what}', author=False))
    # await ctx.send('**pong**: The silent reply',  silent=True)

# hybrid command groups and sub-commands
@bot.hybrid_group(fallback="get")
async def tag(ctx, name, myself):
    await ctx.send(f"Showing tag: {name} {myself}")

@tag.command()
async def create(ctx, name):
    await ctx.send(f"Created tag: {name}")


# testing aliases and name
@bot.hybrid_group(fallback="get", aliases=["t"], name='tage', command_prefix='!')
async def tage(ctx, name, myself):
    await ctx.send(f"Showing tag: {name} {myself}")

@tage.command()
async def create(ctx, name):
    await ctx.send(f"Created tag: {name}")

bot.run(config.DISCORD_TEST_BOT_TOKEN)
import discord
from discord.ext import commands
import config, asyncio
# from cogs.functions import get_embeded_message
config.init()

bot = commands.Bot(command_prefix="!", description="The description", intents=config.intents)
# bot = discord.Client()

@bot.event
async def  on_ready():
    print("Ready !")

import math, asyncpraw, asyncprawcore


def get_embeded_message(context, title, description='', author=True):
    print(f'\n embed_title: {title}\n')
    embed = discord.Embed(
            title=title,
            description=description,
            color=0x00FF00
        )
    
    embed.add_field(
            name="Over!",
            #value=":ping_pong:",
            value=":pizza:",
            inline=True
        )
    if author: #author=False for perodic unleash/subscription
        print(f'avatar:{context.author.avatar}')
        embed.set_footer(text=f'{context.author}',icon_url=context.author.avatar)
        #embed.set_author(name=context.message.author)
        #embed.set_thumbnail(url=context.author.avatar_url)
    return(embed)


@bot.command()
async def ping(ctx):
    await ctx.send(embed= get_embeded_message(ctx, 'ping-pong', 'this is body', author=False), silent=True)
    # await ctx.send('**pong**: The silent reply',  silent=True)

@bot.command()
async def redit(ctx):
    print(f'\n\nchk{0}\n\n')
    await unleash_reddit(ctx.channel, 'memes', 5, author=False, last_sub=False)

bot.run(config.DISCORD_TEST_BOT_TOKEN)

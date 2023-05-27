import os, sys, discord, platform, random, aiohttp, json, datetime, requests
from discord.ext import commands
from multiprocessing import context
from cogs.functions import db

if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config

class AdminCog(commands.Cog, name="admin"):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.is_owner()
    @commands.hybrid_command(name="die", aliases=["logout"])
    async def die(self, context):
        await context.send("Beep boop boop beep!! logging out!!..")
        await context.bot.logout()
        

async def setup(bot):
    await bot.add_cog(AdminCog(bot))

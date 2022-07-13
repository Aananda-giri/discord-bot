# import discord, os
# import math, asyncpraw, asyncprawcore
# from cogs.functions import YTDLSource, download_from_youtube, get_embeded_message

from discord.ext import commands
from cogs.functions import get_embeded_message
# from replit import db
from database import db


class Commands(commands.Cog, name="reddit_commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ready', aliases=['is_reddit_up', 'red'], brief='unleahes the subreddit to the channel', help='e.g.To unleash r/jokes `.unleash jokes`')
    async def ready(self, context, *args):
        embed = get_embeded_message(context, "Yes Boss, I am ready!")
        await context.send(embed=embed)

    @commands.command(name='unleashed', aliases=['list_unleashed'], brief='list of unleashed channels', help='e.g.To unleash r/jokes `.unleash jokes`')
    async def unleashed(self, context, *args):
        print('backtrack list unleashed')
        channel_id = str(context.channel.id)
        print(channel_id)
        try:
            reddit_db = db('subreddit')
            subreddits_list = reddit_db.get_one(str(channel_id))
            # subreddits_list = list(list(db['unleash'][channel_id]))
        except:
            subreddits_list = []
        ioe_db = db('ioe_notifications')
        ioe_db.get_all()
        if channel_id in ioe_db:
            subreddits_list += 'ioe_notifications'
        if subreddits_list == []:
            embed = get_embeded_message(context, "Nothing unleashed")
        else:
            embed = get_embeded_message(context, "Unleashed", subreddits_list)
        await context.send(embed=embed)

    @commands.command(name='anon',
                      brief='to send message anonymously',
                      help='e.g. `.anon Guess who!`')
    async def anon(self, context, *, message='please provide a message'):
        msg = str(message)
        # print(msg)
        await context.message.delete()
        id = context.channel.id
        a = {'anon': ''}
        a['anon'] = MySchedule()
        await a['anon'].schedule_message('anonymous', msg, id)
        print(
            f'\ncogs.commands.anon sent anonymous message channel:{context.channel.id}\n')
        # print(msg, id)
        # await schedule_message(author='', message=msg, id=id)

    @commands.command(name='vent', aliases=[], brief='make a vent channel (anynomus messenging channel)', help='vent_channels make every message anonymous by deleting and re-posting user\'s messages \n e.g. `.vent` To to make or unmake a vent channel')
    async def vent(self, context, *args):

        print('\n\n vent invoked \n\n')
        vent_db = db('vent')
        vent_channels = vent_db.get_all()

        if int(context.channel.id) not in vent_channels:
            print('\n\n adding channel \n\n')
            # enabling a vent channel
            vent_db.add_one(context.channel.id)
            response_message = """
        \n**vent channel enabled...**
        vent_channels make every message anonymous by deleting and re-posting user\'s messages
        please enter: `.vent` To to enable/disable a vent channel\n
        """
        else:
            print('\n\n removing vent channel \n\n')
            # disabling a vent channel
            vent_db.remove_one(str(context.channel.id))
            response_message = """
        \n**vent channel disabled...**
        vent_channels make every message anonymous by deleting and re-posting user\'s messages
        please enter `.vent` To to enable/disable a vent channel
        """
        await context.send(response_message)


def setup(bot):
    bot.add_cog(Commands(bot))

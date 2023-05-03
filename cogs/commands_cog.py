# import discord, os
# import math, asyncpraw, asyncprawcore
# from cogs.functions import YTDLSource, download_from_youtube, get_embeded_message

import discord
from discord.ext import commands
from cogs.functions import get_embeded_message
# from replit import db
from database import db


class Commands(commands.Cog, name="general_commands"):
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


    @commands.command(name="whois")
    async def whois(self, ctx, member:discord.Member =  None):

        if member is None:
            member = ctx.author
            roles = [role for role in ctx.author.roles]

        else:
            roles = [role for role in member.roles]

        embed = discord.Embed(title=f"{member}", colour=member.colour, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_author(name="About user:")#"درباره یوزر: ")
        embed.add_field(name="Individual ID:", value=member.id, inline=False)
        #embed.add_field(name="آی دی فرد:", value=member.id, inline=False)
        
        embed.add_field(name="Username: ",value=member.display_name, inline=False)
        #embed.add_field(name="یوزر نیم:",value=member.display_name, inline=False)
        
        embed.add_field(name="User half code:",value=member.discriminator, inline=False)
        #embed.add_field(name="کد یوزر نیم:",value=member.discriminator, inline=False)
        
        embed.add_field(name="current situation:", value=str(member.status).title(), inline=False)
        #embed.add_field(name="وضعیت فعلی:", value=str(member.status).title(), inline=False)
        
        embed.add_field(name="Last visit:", value=f"{str(member.activity.type).title().split('.')[1]} {member.activity.name}" if member.activity is not None else "None", inline=False)
        #embed.add_field(name="آخرین بازدید:", value=f"{str(member.activity.type).title().split('.')[1]} {member.activity.name}" if member.activity is not None else "None", inline=False)
        
        embed.add_field(name="Account creation date:", value=member.created_at.strftime("%a, %d, %B, %Y, %I, %M, %p UTC"), inline=False)
        #embed.add_field(name="تاریخ ساخت اکانت:", value=member.created_at.strftime("%a, %d, %B, %Y, %I, %M, %p UTC"), inline=False)
        
        embed.add_field(name="Join date to server:", value=member.joined_at.strftime("%a, %d, %B, %Y, %I, %M, %p UTC"), inline=False)
        #embed.add_field(name="تاریخ جوین به سرور:", value=member.joined_at.strftime("%a, %d, %B, %Y, %I, %M, %p UTC"), inline=False)
        
        embed.add_field(name=f"Individual rolls [{len(roles)}]", value=" **|** ".join([role.mention for role in roles]), inline=False)
        #embed.add_field(name=f"رول های فرد [{len(roles)}]", value=" **|** ".join([role.mention for role in roles]), inline=False)
        
        embed.add_field(name="Top person roll:", value=member.top_role, inline=False)
        #embed.add_field(name="بالا ترین رول فرد:", value=member.top_role, inline=False)
        
        embed.add_field(name="robot:", value=member.bot, inline=False)
        #embed.add_field(name="ربات:", value=member.bot, inline=False)
        await ctx.send(embed=embed)
        return



async def setup(bot):
    await bot.add_cog(Commands(bot))

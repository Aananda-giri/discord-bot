import discord, asyncio
import math, asyncpraw, asyncprawcore
from discord.ext import commands
from cogs.functions import get_embeded_message
# from replit import db
from database import db
import config

class IoeCommands(commands.Cog, name="reddit_commands"):
    def __init__(self, bot):
        self.bot = bot    

    @commands.hybrid_group(name='ioe_notice',
                 aliases=['ioe_noti', 'ioe_notification', 'ioe_notifications', 'ioenoti', 'ioenotification', 'ioenotifications'],
                 brief='unleahes the subreddit to the channel',
                 help='e.g.To unleash r/jokes `.unleash jokes`',
                 fallback="start")
    async def ioe_notice(self, context):
        print('\n\n ------------- IOE-Notice initiated ------------- \n\n')
        ioe_db = db('ioe_notifications')
        message = ioe_db.add_one(str(context.channel.id))
        embed = get_embeded_message(context, 'unleashing ioe_notifications: {message}')
        await context.send(embed=embed)

    @ioe_notice.command(name='stop_ioe_notice',
                 brief='to contain/stop unleashed  subreddit message',
                 help='e.g. `.contain jokes`')
    async def stop(self, context):
            # stop ioe notification from channel
            ioe_db = db('ioe_notifications')
            if int(context.channel.id) in ioe_db.get_all():
                
                channel_id = str(context.channel.id)
                message = ioe_db.remove_one(channel_id)
                
                embed = get_embeded_message(context, f'stopped ioe_notifications: {message}')
            else:
                embed = get_embeded_message(context, 'ioe_notifications not started to {}'.format(context.channel))
            await context.send(embed=embed,empheral=True)
            
async def setup(bot):
    await bot.add_cog(IoeCommands(bot))

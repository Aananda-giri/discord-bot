import discord, asyncio
import math, asyncpraw, asyncprawcore
from discord.ext import commands
from cogs.functions import get_embeded_message
# from replit import db
from database import db
import config

async def sub_exists(subreddit_name):
    reddit = asyncpraw.Reddit(
        client_id= config.RD_CLIENT_ID,# os.environ['RD_CLIENT_ID'],
        client_secret= config.RD_CLIENT_SECRET, # os.environ['rd_client_secret'],
        password= config.RD_PASS,    # os.environ['rd_pass'],
        user_agent="praw_test",
        username="Alternative-Ad-8849",
    )
    exists = True
    try:
        subreddit = await reddit.subreddit(subreddit_name, fetch=True)     # by default Async PRAW doesn't make network requests when subreddit is called
        # do something with subreddit
    except asyncprawcore.Redirect: 
        exists=False
    return(exists)
    # Reddit will redirect to reddit.com/search if the subreddit doesn't exist
    #await ctx.send(f"Subreddit {subreddit_name} doesn't exist.")


async def unleash_reddit(channel, subreddit, no_of_posts=5, author=False, last_sub=False):
    reddit = asyncpraw.Reddit(
        client_id= config.RD_CLIENT_ID,# os.environ['RD_CLIENT_ID'],
        client_secret= config.RD_CLIENT_SECRET, # os.environ['rd_client_secret'],
        password= config.RD_PASS,    # os.environ['rd_pass'],
        user_agent="praw_test",
        username="Alternative-Ad-8849",
    )
    #print(channel_id)  
    #channel = bot.get_channel(id=int(channel_id.strip()))
    #channel = bot
    submissions = await reddit.subreddit(subreddit)
    donot_proceed = 0
    #To display hot post if only one is to be fetched
    if no_of_posts == 1:
        donot_proceed = 1
        no_of_posts = 2
    try:
        async for submission in submissions.hot(limit=int(no_of_posts / 4)):
            # print('Unleash for loop:{}'.format(0))
            title = submission.title
            body = submission.selftext
            embed = discord.Embed(title=title,
                                url=submission.url,
                                description=body,
                                colour=discord.Color.red())
            embed.set_image(url=submission.url)
            #To set subreddit name in footer
            embed.set_footer(text="subreddit: \"r/{}\"".format(subreddit))#, icon_url=submissions.icon_img)#subreddit.icon_img)#, subreddit.banner_imgand subreddit.header_img )
            # print('Submission_url: ', submission.url)
            try:
                #To filter lenthy messages > 2500 letters
                if len(str(body)) < 2500:
                    image_formats = ['jpg', 'jpeg', 'png']

                    #checks if image_format in submission.url
                    if sum([(i in str(submission.url)) for i in image_formats]):
                        await channel.send(embed=embed, silent=True)
                    else:
                        await channel.send(submission.url, silent=True)
            except:
                pass
    except Exception as e:
        print(f'\n error in sending content from subreddit:{subreddit} to channel:{channel}\n, error:{e} \n')


    if donot_proceed != 1:
        try:
            async for submission in submissions.top('day',
                                                    limit=int(no_of_posts / 2)):
                # print('Unleash for loop:{}'.format('n'))
                title = submission.title
                body = submission.selftext
                embed = discord.Embed(title=title,
                                    url=submission.url,
                                    description=body,
                                    colour=discord.Color.red())
                embed.set_image(url=submission.url)
                #To set subreddit name in footer
                embed.set_footer(text="subreddit: \"r/{}\"".format(subreddit))
                # print('Submission_url: \"', submission.url, '\"')
                if submission.url == '':
                    print('\nreddit.unleash_reddit:Guess What: empty submission url\n')
                try:
                    if len(str(body)) < 2500:
                        image_formats = ['jpg', 'jpeg', 'png']
                        #checks if image_format in submission.url
                        if sum([(i in str(submission.url))
                                for i in image_formats]):
                            
                            await channel.send(embed=embed, silent=True)
                    else:
                        await channel.send(submission.url, silent=True)
                except:
                    pass
        except Exception as e:
            print(f'\n error in sending content from subreddit:{subreddit} to channel:{channel}\n, error:{e}')
        try:
            async for submission in submissions.new(limit=no_of_posts -
                                                    math.ceil(no_of_posts / 4)):
                # print('Unleash for loop:{}'.format(0))
                title = submission.title
                body = submission.selftext
                embed = discord.Embed(title=title,
                                    url=submission.url,
                                    description=body,
                                    colour=discord.Color.red())
                embed.set_image(url=submission.url)
                #To set subreddit name in footer
                embed.set_footer(text="subreddit: \"r/{}\"".format(subreddit))
                # print('Submission_url: ', submission.url)
                try:
                    if len(str(body)) < 2500:
                        image_formats = ['jpg', 'jpeg', 'png']
                        #checks if image_format in submission.url
                        if sum([(i in str(submission.url))
                                for i in image_formats]):
                            await channel.send(embed=embed, silent=True)
                    else:
                        await channel.send(submission.url, silent=True)
                except:
                    pass
        except Exception as e:
            print(f'\n error in sending content from subreddit:{subreddit} to channel:{channel}, error:{e} \n')
    if last_sub:
      # send unleashed list at the end of sending posts
      try:
        reddit_db = db('subreddit')
        subreddits = reddit_db.get_one(str(channel.id))
        embed=get_embeded_message(channel, 'Unleashed List:', subreddits, author=False)
        await channel.send(embed=embed, silent=True)
      except Exception as e:
        print(f'\n error sending last sub channel:{channel}  subreddit:{subreddit}\n, error:{e}')

class RedditCommands(commands.Cog, name="reddit_commands"):
    def __init__(self, bot):
        self.bot = bot    
    
    @commands.command(name='unleash', aliases=['unleash_reddit'],
                 brief='unleahes the subreddit to the channel',
                 help='e.g.To unleash r/jokes `.unleash jokes`')
    async def unleash(self, context, *args):
        
        what = ' '.join(args)
        subreddit = what.strip().split(' ')[0]
        print('\n\nreddit.unleash: subreddit:{subreddit}, args:{args}\n\n')
        try:
            how_many = int(subreddit[-1])
        except:
            how_many = 8
        print('\n Unleash initiated\n subreddit:{} \n'.format(subreddit))
        if subreddit == '':
            embed = get_embeded_message(context, 'Please enter the subreddit to be unleashed')
        elif subreddit == 'ioe_noti' or subreddit == 'ioe_notification' or subreddit == 'ioe_notifications' or subreddit == 'ioenoti' or subreddit == 'ioenotification' or subreddit == 'ioenotifications':
            ioe_db = db('ioe_notifications')
            message = ioe_db.add_one(str(context.channel.id))
            embed = get_embeded_message(context, 'unleashing ioe_notifications: {message}')
        else:
            reddit_db = db('subreddit')
            channel_id = str(context.channel.id)
            
            if subreddit.startswith(('/r/', 'r/')):
              subreddit = subreddit.split('r/')[-1]
              # -1 gets the last element in the list
            print(context.channel.id)
            #if "unleash" not in db.keys():db['unleash']={}
            if await sub_exists(subreddit):
                print('\n sub_exists : {}\n'.format(subreddit))
                

                # Add to database
                reddit_db.add_one(channel_id = str(channel_id), subreddit = subreddit, how_many=how_many)

                print(f'\n database.get_all:{reddit_db.get_all()}')
                
                embed = get_embeded_message(context, 'r/{subreddit} already unleashed to {}'.format(subreddit, context.channel))
                print(f'embed:{embed}')
                await unleash_reddit(context.channel, subreddit, 15)
            else:
                print(f'\n reddit.unleash: sub_doesnt_exists : {subreddit}\n')
                embed = get_embeded_message(context, 'Error', 'subreddit  r/{} doesnot exists.'.format(subreddit))
        await context.send(embed=embed)
                
    
    
    @commands.command(name='contain',
                 brief='to contain/stop unleashed  subreddit message',
                 help='e.g. `.contain jokes`')
    async def contain(self, context, *args):
        subreddit = ' '.join(args)
        if subreddit == '':
            embed = get_embeded_message(context, 'Please enter the subreddit to be unleashed')
        elif subreddit == 'ioe_noti' or subreddit == 'ioe_notification' or subreddit == 'ioe_notifications' or subreddit == 'ioenoti' or subreddit == 'ioenotification' or subreddit == 'ioenotifications':
            # contain ioe notification from channel
            ioe_db = db('ioe_notifications')
            if int(context.channel.id) in ioe_db.get_all():
                
                channel_id = str(context.channel.id)
                message = ioe_db.remove_one(channel_id)
                
                embed = get_embeded_message(context, f'contained ioe_notifications: {message}')
            else:
                embed = get_embeded_message(context, 'ioe_notifications not unleashed to {}'.format(context.channel))
              
        else:
            # contain subreddit from a channel
            # print(context.channel.id)
            reddit_db = db('subreddit')
            channel_id = str(context.channel.id)
            message = reddit_db.remove_one(channel_id, subreddit)
            embed = get_embeded_message(context, f'contain r/{subreddit} message: {message}')
        await context.send(embed=embed)
          #print(context.channel.id)
            #await context.send(context.channel.id)

async def setup(bot):
    await bot.add_cog(RedditCommands(bot))

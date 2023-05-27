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

import math, asyncpraw, asyncprawcore


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
    print(f'\n\nchk{1}\n\n')
    submissions = await reddit.subreddit(subreddit)
    donot_proceed = 0
    #To display hot post if only one is to be fetched
    print(f'\n\nchk{2}\n\n')
    # reddit = asyncpraw.Reddit(
    #     client_id= config.RD_CLIENT_ID,# os.environ['RD_CLIENT_ID'],
    #     client_secret= config.RD_CLIENT_SECRET, # os.environ['rd_client_secret'],
    #     password= config.RD_PASS,    # os.environ['rd_pass'],
    #     user_agent="praw_test",
    #     username="Alternative-Ad-8849",
    # )
    print(f'\n\nchk{3}\n\n')
    try:
        # submissions = await reddit.subreddit('memes')
        print(f'\n\nchk{4}\n\n')
        async for submission in submissions.hot(limit=5):
            print(f'\n\nchk{53}\n\n')
            # print('Unleash for loop:{}'.format(0))
            title = submission.title
            print(f'\n\nchk{4}\n\n')
            print('\n\n', submission.title)
            print('\n\n', submission.url)
            body = submission.selftext
            print(f'\n\nchk{5}\n\n')
            embed = discord.Embed(title=title,
                                url=submission.url,
                                description=body,
                                colour=discord.Color.red())
            print(f'\n\nchk{6}\n\n')
            embed.set_image(url=submission.url)
            print(f'\n\nchk{7}\n\n')
            #To set subreddit name in footer
            embed.set_footer(text="subreddit: \"r/{}\"".format(subreddit))#, icon_url=submissions.icon_img)#subreddit.icon_img)#, subreddit.banner_imgand subreddit.header_img )
            print(f'\n\nchk{8}\n\n')
            # print('Submission_url: ', submission.url)
            try:
                print(f'\n\nchk{9}\n\n')
                #To filter lenthy messages > 2500 letters
                if len(str(body)) < 2500:
                    print(f'\n\nchk{10}\n\n')
                    image_formats = ['jpg', 'jpeg', 'png']

                    #checks if image_format in submission.url
                    if sum([(i in str(submission.url)) for i in image_formats]):
                        print(f'\n\nchk{11}\n\n')
                        await channel.send(embed=embed, silent=True)
                    else:
                        print(f'\n\nchk{12}\n\n')
                        await channel.send(submission.url, silent=True)
            except:
                pass
    except Exception as e:
        print(f'\n error in sending content from subreddit:{subreddit} to channel:{channel}\n, error:{e} \n')


@bot.command()
async def ping(ctx):
    await ctx.send(embed= get_embeded_message(ctx, 'ping-pong', 'this is body', author=False), silent=True)
    # await ctx.send('**pong**: The silent reply',  silent=True)

@bot.command()
async def redit(ctx):
    print(f'\n\nchk{0}\n\n')
    await unleash_reddit(ctx.channel, 'memes', 5, author=False, last_sub=False)

bot.run(config.DISCORD_TEST_BOT_TOKEN)

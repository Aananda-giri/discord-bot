# replit version
""""
Copyright © Krypton 2020 - https://github.com/kkrypt0nn
Description:
This is a template to create your own discord bot in python.

Version: 2.0
"""

# import json, random,
# from discord.ext import commands
# from discord import Member
# from discord.ext.commands import has_permissions, MissingPermissions
# from prawcore import NotFound
# from discord import FFmpegPCMAudio
#from cogs.music import get_stream, get_embed
# from cogs.functions import YTDLSource, download_from_youtube, get_embeded_message
import discord, asyncio, os, platform, sys, requests, json, threading
from discord.ext.commands import Bot

if not os.path.isfile("config.py"):
  sys.exit("'config.py' not found! Please add it and try again.")
else:
  import config
config.init()

# replit db import method
# from os import environ
# environ["REPLIT_DB_URL"] = "https://kv.replit.com/v0/eyJhbGciOiJIUzUxMiIsImlzcyI6ImNvbm1hbiIsImtpZCI6InByb2Q6MSIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjb25tYW4iLCJleHAiOjE2NTExNDExMDAsImlhdCI6MTY1MTAyOTUwMCwiZGF0YWJhc2VfaWQiOiIwZDNkZTY3My04ZjM3LTQ4ZjktOGFmNS00OWU2MWUyNTMzMGYifQ.CpVO558CCW0s7b9C3rH6m77hW_ybOqHzVJVFwhf8fcv0sebcg5D26CiAilVybi5pfYVUHh3oLlWSaCCFiThVIA"
from database import db

from keep_alive import keep_alive
#from ioe_crawler import get_new_notifications, run_spider
#import commands

from discord.ext import tasks
from cogs.reddit import unleash_reddit
from cogs.news import send_news
#import ffmpeg

#from discord import FFmpegPCMAudio
from dotenv import load_dotenv
from telegram_bot.bot import start_bot
from viber_bot.bot import start_bot as start_viber_bot

load_dotenv()

intents = config.intents
client = discord.Client(intents=intents)

"""  
Setup bot intents (events restrictions)
For more information about intents, please go to the following websites:
https://discordpy.readthedocs.io/en/latest/intents.html
https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents
"""


# intents.guild_typing = False
# intents.typing = False
# intents.dm_messages = False
# intents.dm_reactions = False
# intents.dm_typing = False
# intents.guild_messages = True
# intents.guild_reactions = True
# intents.integrations = True
# intents.invites = True
# intents.voice_states = False
# intents.webhooks = False

bot = Bot(command_prefix=config.BOT_PREFIX, help_command=None, intents=intents)

# Removes the default help command of discord.py to be able to create our custom help command.
#bot.remove_command("help")
                    

@tasks.loop(hours=6)
async def unleashing():
    # ---------------------------
        # unleash subreddit
    # ---------------------------
    print('\n main.unleshing: start Unleashing Reddit')
    intents = discord.Intents.default()
    #discord.Intents.members = True
    intents.members = True
    intents.all()

    
    reddit_db = db('subreddit')
    subreddits = reddit_db.get_all()
    
    for channel_id in subreddits:
        # subreddits[str(channel_id)] = {jokes:10, memes:11}
        len_subs = len(subreddits[str(channel_id)])
        channel = bot.get_channel(id=int(channel_id))
        for progress, each_sub in enumerate(subreddits[str(channel_id)]):
          last_sub = True if (progress == len_subs-1) else False
          await unleash_reddit(channel = channel, subreddit = each_sub, no_of_posts = int(subreddits[channel_id][each_sub]), author=False, last_sub=last_sub)

          # print('Unleashed')
    
    # ---------------------------
        # unleash news
    # ---------------------------
    # @tasks.loop(hours=6)
    # async def unlease_news():
    print("\n unleashing news")
    # for channel_id in db['subscription']):
    news_db = db('news').get_all()
    # subscription_db = json.loads(db['subscription'].replace("'", "\""))
    for channel_id in news_db:
      print(f'\n\n unleash_subscriptions: channel_id:{channel_id} {type(channel_id)} \n\n')
      channel = bot.get_channel(id=int(channel_id))
      # db['subscription'][str(channel_id)]['countries']
      
      # countries = subscription_db[str(channel_id)]['countries']
      countries = news_db[str(channel_id)]
      # if 'news' in subscription_db[str(channel_id)]['what']:
      len_countries = len(countries)
      # progress -> count no. of countrie's sent
      for progress, country in enumerate(countries):
        how_many = int(countries[country])

        #true for last country in countries
        last_country = (len_countries-1)==progress
          
        await send_news(channel, country, how_many, last_country=last_country)
    # await unleash_ioe_notifications.start()

@tasks.loop(hours=3)
async def unleash_ioe_notifications():
  # sending ioe_notifications to subscribed channels perodically: '3 hours'
  #n=json.load(open('ioe_notices.json','r'))
  #notifications = {'topics': [n['topics'][0]], 'urls':[n['urls'][0]]}
  
  notices = requests.get('http://ioee.herokuapp.com/api/')
  notices = notices.json()['notices']
  print('Got Notifications:  {}'.format(notices))
  notices.reverse()
  
  #nathan_server = bot.get_channel(id=904750102126657616)
  #zaroom = bot.get_channel(id=934322824540209202)
  #veg = bot.get_channel(id=871256858587979816)


  for notice in notices:
    #topic.reverse()
    #url.reverse()
    #print("notice: ".format(notice))

    # Space in url causing err: In embed.url: Not a well formed URL
    # %20 is for space
    url = str(notice['url']).replace(' ','%20')
    
    embed = discord.Embed(
      title=notice['title'],
      description = "Date: {}".format(notice['date']),
      url = url,
      color=0x00FF00
    )
    #embed.set_image(url="")
    #embed.set_footer(text=f"Help requested by: {ctx.message.author} !",#icon_url=ctx.author.avatar_url)
    
    embed.add_field(
      name="link",
      value="{}".format(url),
      inline=False
    )
    embed.add_field(
      name="Source:",
      value='https://exam.ioe.edu.np/',
      inline=False
      #f"Usage: {config.BOT_PREFIX}avatar",
    )

    # await nathan_server.send(embed=embed)
    # await zaroom.send(embed=embed)
    for channel_id in db('ioe_notifications').get_all():
      try:
        channel = await bot.fetch_channel(int(channel_id))
        print("channel_id : {}, channel: {}, notification: {}".format(channel_id, channel, notice['title']))
        
        # AttributeError: 'NoneType' object has no attribute 'send'
        await channel.send(embed=embed)
      
      except Exception as ex:
        # can't send ioe_notification
        error = "can't send ioe_notification: " + str(ex)
        # db['errors'].append(error)
        #await channel.send(error)
        print(error)
    #await veg.send(embed=embed)
    #print('got_notifications {}'.format(notices))
  
  print('\n Done unleashing ioe_notices\n')
  try:
      await unleashing.start()
      print('\n\nunleash ioe continue\n\n')
  except:
    pass
  return(1)

@tasks.loop(seconds=3)
async def print_hi():
  print('\n\n _________-hi================== \n\n')
@tasks.loop(seconds=3)
async def print_hi2():
  print('\n\n _________-hi2================== \n\n')


unleashing.start()
unleash_ioe_notifications.start()
# The code in this event is executed when the bot is ready
@bot.event
async def on_ready():
  bot.loop.create_task(status_task())
  # await bot.loop.create_task(unleashing_tasks())
  

  print(f"Logged in as {bot.user.name}")
  print(f"Discord.py API version: {discord.__version__}")
  print(f"Python version: {platform.python_version()}")
  print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
  print("-------------------")

# Setup the game status task of the bot
async def status_task():
  while True:
    await bot.change_presence(activity=discord.Game("Prefix : $"))
    await asyncio.sleep(60)
    await bot.change_presence(activity=discord.Game("Coded by 🥀 Me !"))
    #await bot.change_presence(activity=discord.Game("Coded by 🥀 Persian#5273 !"))
    await asyncio.sleep(60)
    await bot.change_presence(activity=discord.Game(f"{config.BOT_PREFIX}help"))
    await asyncio.sleep(60)
    await bot.change_presence(activity=discord.Game("🌖⃤. SΞΛTTŁΞ .🌖⃤"))
    await asyncio.sleep(60)


async def process_message(message):
    # we do not want the bot to reply to itself or other bots
    if message.author == bot.user:
        return
    
    if message.content.startswith('.guess'):
        await message.channel.send('Guess a number between 1 to 10')
        
        def guess_check(m):
            return m.content.isdigit()
            
        guess = await bot.wait_for('message', timeout=5.0, check=guess_check)
        answer = random.randint(1, 10)
        if guess is None:
            fmt = 'Sorry, you took too long. It was {}.'
            await message.channel.send(fmt.format(answer))
            return
        if int(guess.content) == answer:
            await message.channel.send('You are right!')
        else:
            await message.channel.send(
                'Sorry. It is actually {}.'.format(answer))
    else:

        if message.guild is None and message.author != bot.user:
            #await channel.send(str(message.author) + str(message.content))
        
            embed = discord.Embed(title=message.author,
                                  description=message.content)
            channel = bot.get_channel(id=873477235477184522)
            await channel.send(embed=embed)
            
        print(str(message.content))
        if any(word in str(message) for word in config.sad_words):
            options = config.starter_encouragements
            #if "encouragements" in db.keys():
            try:
                encouragements = "encouragements"
                #print(list(db["encouragements"]))
                options = options  #+ list(db["encouragements"])
                await message.channel.send(random.choice(options))
            except:
                sqlite_dict['encouragements']=[]
def is_int(word):
    try:
        int_word = int(word)
        return True
    except:
        return False

def is_word(string):
    # checks server_channel in chain games db, starting letter and end letter matches, and message contain single word.
    if str(string)[0] == str(string)[-1] and str(string)[1:-1].strip() == str(string)[1:-1].strip().replace(' ', ''):
        return True
    else:
        return False
    
async def process_games(message):
    if str(message.channel.id) in config.count_ids and is_int(message.content):
              print('\nproceed count\n')
              await proceed_count(message, int(message.content))
    elif str(message.channel.id) in config.chain_ids and is_word(message.content):
              print('\nproceed_chain\n')
              await proceed_chain(message)
    else:
        return False


# The code in this event is executed every time someone sends a message, with or without the prefix
@bot.event
async def on_message(message):
    # Ignores if a command is being executed by a bot or by the bot itself
    if message.author == bot.user or message.author.bot:
        # ignoring messages by bots
        return
    elif message.author.id not in config.BLACKLIST:
        # Process the command if the user is not blacklisted
        
        # checking and implementing vent_channel
        vent_db = db('vent')
        vent_channels = vent_db.get_all()
        print('\n\n author not black_listed \n\n')
        if int(message.channel.id) in vent_channels and message.clean_content != '.vent':
          print(f'\n\n channel{message.channel.id} in \'vent\' table:{vent_channels} clean_content:{message.clean_content}\n\n')
          message_text = message.content
          message_channel = message.channel
          
          await message.delete()  # deleting message
          await message_channel.send(message_text)  # sending message
          return

        processing_games = await process_games(message);
        if not processing_games:
            print(f"\n{message.author}: {message.content}\n")
            await bot.process_commands(message)
    else:
      # Send a message to let the user know he's blacklisted
      context = await bot.get_context(message)
      embed = discord.Embed(
        title="You're blacklisted!",
        description="Ask the owner to remove you from the list if you think it's not normal.",
        color=0x00FF00
      )
      await context.send(embed=embed)

global player
@bot.event
async def on_reaction_add(reaction, user,a=''):
    #embed = reaction.embeds[0]
    #emoji = reaction.emoji
    #print('hii')
    #await reaction.message.add_reaction('♥️')
    if not user.bot:
        
        #global player
        #player = ctx.bot.get_cog('Music')
        #player = author.voice.channel
        # stop emoji
        if str(reaction.emoji) == "⏹️":
            config.player.stop()
        
        # pause emoji
        elif str(reaction.emoji) == "⏸️":
            if config.player.is_playing():
                config.player.pause()
                print('paused')
            else:
                config.player.resume()
                print('resume')
        
        # next emoji
        elif str(reaction.emoji) == "⏭️":
            if config.playing=='fm':
              
              print('Playing next, current:{}'.format(config.stream))
              config.stream = get_stream('next',config.stream)
              config.player.stop()
              config.player.play(FFmpegPCMAudio(config.stream['url']))
              
              embed=get_embed(reaction, user, config.stream)
              await config.currently_playing_message.edit(embed=embed)
              
            #message.send('Hello World')
            #play_next()
        
        # previous emoji
        elif str(reaction.emoji) == "⏮️":
            if config.playing=='fm':
              
              print('Playing next, current:{}'.format(config.stream))
              config.stream = get_stream('prev', config.stream)
              config.player.stop()
              config.player.play(FFmpegPCMAudio(config.stream['url']))
              
              embed=get_embed(reaction, user, config.stream)
              await config.currently_playing_message.edit(embed=embed)
            
            print('Playing next')

        # download emoji
        elif str(reaction.emoji) == "⬇️":
          if config.playing!='fm':  
            if not 'downloads' in os.listdir():
                os.mkdir('downloads')
            print('Try download')
    
            async with reaction.message.channel.typing():
                
                URL, thumbnails, title, vid_url = await YTDLSource.from_url(config.playing, loop=bot.loop, download=True)
                
                full_downloaded_file_name = title + '.mp3'
                
                await reaction.message.channel.send(file=discord.File(full_downloaded_file_name))
                os.remove(full_downloaded_file_name)
                print(' downloaded!!! ')
        else:
          await reaction.message.add_reaction(reaction)
    #print('hii')
    #print(reaction)
    #print(reaction.message)
    #print(user)

    #if user.bot:
    #    return
    #else:
    #  previous_messages = await channel.history(limit=1).flatten()
    #  prev_message.add_reaction('♥️')
    '''if emoji == "emoji 1":
        fixed_channel = bot.get_channel(channel_id)
        await fixed_channel.send(embed=embed)
    elif emoji == "emoji 2":
        #do stuff
    elif emoji == "emoji 3":
        #do stuff
    else:
        return'''



@bot.event
async def on_reaction_remove(reaction, user):
    print('\nremoved reaction\n')
    if not user.bot:
        
        
        # stop emoji
        if str(reaction.emoji) == "⏹️":
            config.player.stop()
        
        # pause emoji
        elif str(reaction.emoji) == "⏸️":
            if config.player.is_playing():
                config.player.pause()
                print('paused')
            else:
                config.player.resume()
                print('resume')
        
        # next emoji
        elif str(reaction.emoji) == "⏭️":
            if config.playing=='fm':
              
              print('Playing next, current:{}'.format(config.stream))
              config.stream = get_stream('next',config.stream)
              config.player.stop()
              config.player.play(FFmpegPCMAudio(config.stream['url']))
              
              embed=get_embed(reaction, user, config.stream)
              await config.currently_playing_message.edit(embed=embed)
              
            #message.send('Hello World')
            #play_next()
        
        # previous emoji
        elif str(reaction.emoji) == "⏮️":
            if config.playing=='fm':
              
              print('Playing next, current:{}'.format(config.stream))
              
              config.stream = get_stream('prev', config.stream)
              config.player.stop()
              config.player.play(FFmpegPCMAudio(config.stream['url']))
              
              embed=get_embed(reaction, user, config.stream)
              await config.currently_playing_message.edit(embed=embed)
            
            print('Playing next')

        # download emoji
        elif str(reaction.emoji) == "⬇️":
          if config.playing=='fm':  
            if not 'downloads' in os.listdir():
                os.mkdir('downloads')
            print('Try download')
    
            async with reaction.message.channel.typing():
                full_downloaded_file_name = await download_from_youtube(config.playing)
                await reaction.message.channel.send(file=discord.File(full_downloaded_file_name))
                os.remove(full_downloaded_file_name)
                print(' downloaded!!! ')
        else:
          await reaction.message.add_reaction(reaction)

#To make leave voice channel if bot is alone in voice channel
@bot.event
async def on_voice_state_update(member, before, after):
    print('\n\n Fired on_voice_state_update function \n\n')
    voice_state = member.guild.voice_client
    if voice_state is None:
        # Exiting if the bot it's not connected to a voice channel
        return 

    if len(voice_state.channel.members) == 1:
        await voice_state.disconnect()




# The code in this event is executed every time a command has been *successfully* executed
@bot.event
async def on_command_completion(ctx):
  fullCommandName = ctx.command.qualified_name
  split = fullCommandName.split(" ")
  executedCommand = str(split[0])
  #print(f"Executed {executedCommand} command in {ctx.guild.name} by {ctx.message.author} (ID: {ctx.message.author.id})")
  
  # Storing command history/logs
  with open('logs.json','r') as file:
      command_logs = json.load(file)
  #command_logs={}
  #print('command_logs',command_logs)
  try:
    command_logs[executedCommand]
  except:
    command_logs[executedCommand]=[]
  
  try:
    print('Try')
    command_logs[executedCommand][0][str(ctx.message.author.id)]["times_excuted"] += 1
  except Exception as Ex:
    print(f'Except: {Ex}')
    command_logs[executedCommand].append({ctx.message.author.id : {"uesrname":str(ctx.message.author.name)+str(ctx.message.author.discriminator), "times_excuted":1}})
    
  #print(command_logs)
  with open('logs.json','w') as file:
        json.dump(command_logs, file, indent = 4)
  

# The code in this event is executed every time a valid commands catches an error
@bot.event
async def on_command_error(context, error):
  if isinstance(error, commands.CommandOnCooldown):
    embed = discord.Embed(
      title="Error!",
      description="This command is on a %.2fs cooldown" % error.retry_after,
      color=0x00FF00
    )
    await context.send(embed=embed)
    raise error



if __name__ == "__main__":
  for extension in config.STARTUP_COGS:
    try:
      bot.load_extension(extension)
      extension = extension.replace("cogs.", "")
      print(f"Loaded extension '{extension}'")
    except Exception as e:
      exception = f"{type(e).__name__}: {e}"
      extension = extension.replace("cogs.", "")
      print(f"Failed to load extension {extension}\n{exception}")
  
  telegram_thread = threading.Thread(target = start_bot, args=(config.TELEGRAM_TOKEN,))
  telegram_thread.setDaemon(True) #runs without blocking the main program from exiting
  telegram_thread.start()    # starts telegram thread

  viber_thread =threading.Thread(target = start_viber_bot, args=(config.VIBER_AUTH_TOKEN, config.TMDB_API_KEY))
  viber_thread.setDaemon(True)
  viber_thread.start()    # starts twitter thread
  
  # twitter_thread=threading.Thread(target = start_twitter_bot, args=(config.,))
  bot.run(config.DISCORD_TOKEN)     # run discord bot

  


# keep_alive()
# Run the bot with the token
# bot.run(os.environ['TOKEN'])



#client.loop.create_task(my_background_task())




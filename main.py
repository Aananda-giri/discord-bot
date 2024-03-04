# from discord.ext import commands
# from discord import Member
# from discord.ext.commands import has_permissions, MissingPermissions
# from prawcore import NotFound
# from discord import FFmpegPCMAudio
#from cogs.music import get_stream, 
# from cogs.functions import YTDLSource, download_from_youtube, 
from cogs.functions import get_embed, proceed_count, RandomEmoji, get_anonymous_message
import json, random, discord, asyncio, os, platform, sys, requests, json, threading
from discord.ext import commands
from discord.ext.commands import Bot
from urllib.parse import unquote, quote

if not os.path.isfile("config.py"):
  sys.exit("'config.py' not found! Please add it and try again.")
else:
  import config
  config.init()

# replit db import method
# from os import environ
# environ["REPLIT_DB_URL"] = "https://kv.replit.com/v0/eyJhbGciOiJIUzUxMiIsImlzcyI6ImNvbm1hbiIsImtpZCI6InByb2Q6MSIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjb25tYW4iLCJleHAiOjE2NTExNDExMDAsImlhdCI6MTY1MTAyOTUwMCwiZGF0YWJhc2VfaWQiOiIwZDNkZTY3My04ZjM3LTQ4ZjktOGFmNS00OWU2MWUyNTMzMGYifQ.CpVO558CCW0s7b9C3rH6m77hW_ybOqHzVJVFwhf8fcv0sebcg5D26CiAilVybi5pfYVUHh3oLlWSaCCFiThVIA"
from database import db
from database import SocialDb

# from keep_alive import keep_alive
from cogs.ioe_crawler import get_new_notifications
#import commands

from discord.ext import tasks
from cogs.reddit_cog import unleash_reddit
from cogs.news_cog import send_news
#import ffmpeg

from datetime import datetime, timedelta
import pytz
from cogs.stats_cog import count_messages
from cogs.quiz_functions import create_stylish_leaderboard_embed
from cogs.functions import get_embeded_message
from cogs.social_media_cog import SocialMedia

#from discord import FFmpegPCMAudio
from dotenv import load_dotenv


import time




load_dotenv()

bot = Bot(command_prefix=config.BOT_PREFIX, help_command=None, intents=config.intents)
client = discord.Client(intents=config.intents)

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
    print('\n\nsubreddits: ', subreddits)
    for channel_id in subreddits:
        # subreddits[str(channel_id)] = {jokes:10, memes:11}
        len_subs = len(subreddits[str(channel_id)])
        try:
          print('\n\n channel_id1: \'{}\'\n\n'.format(channel_id))
          channel = bot.get_channel(int(channel_id))
        except Exception as ex:
          print(f"channel id:{channel_id} \nerror:\n {ex} ")
        for progress, each_sub in enumerate(subreddits[str(channel_id)]):
          last_sub = True if (progress == len_subs-1) else False
          await unleash_reddit(channel = channel, subreddit = each_sub, no_of_posts = int(subreddits[channel_id][each_sub]), author=False, last_sub=last_sub)

          # print('Unleashed')


@tasks.loop(hours=16)
async def unleash_news():
    # ---------------------------
        # unleash news
    # ---------------------------
    # @tasks.floop(hours=6)
    # async def unlease_news():
    print("\n unleashing news")
    # for channel_id in db['subscription']):
    news_db = db('news').get_all()
    # subscription_db = json.loads(db['subscription'].replace("'", "\""))
    for channel_id in news_db:
      try:
        print(f'\n\n unleash_subscriptions: channel_id:{channel_id} {type(channel_id)} \n\n')
        channel = bot.get_channel(id=int(channel_id))
      except Exception as ex:
          print(f"channel id:{channel_id} \nerror:\n {ex} ")
          continue
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
async def unleash_subscription():
  print('unleash subs.')
  db = SocialDb(table_name='instagram')
  subscription_data = db.get_all()
  for sub in subscription_data:
    print(sub)
    if sub['platform'] == 'instagram':
      print('get_new')
      new_posts = SocialMedia.get_new_posts(sub['social_username'],
                                            sub['channel_id'], sub['posts'],
                                            db)
      sub_channel = bot.get_channel(int(sub['channel_id']))
      if new_posts:
        posts.extend(new_posts)
        db.add(sub['channel_id'], sub['social_username'], sub['social_url'],
               sub['platform'], posts)
        for post in new_posts:
          await sub_channel.send(
              embed=get_embeded_message(sub_channel,
                                        'new-post',
                                        'Everyone, there is new post from:' +
                                        str(sub['social_username']) + ' in ' +
                                        str(sub['platform']) +
                                        '\n\n Checkout on Page :  ' +
                                        str(post),
                                        author=False))
      else:
        print(f"no new post on {sub['social_username']}")
        # await sub_channel.send('hi!')

@tasks.loop(hours=4)
async def unleash_ioe_notifications():
  # sending ioe_notifications to subscribed channels perodically: '3 hours'
  #n=json.load(open('ioe_notices.json','r'))
  #notifications = {'topics': [n['topics'][0]], 'urls':[n['urls'][0]]}
  
  # notices = requests.get('http://ioee.herokuapp.com/api/')
  # notices = notices.json()['notices']
  notices = get_new_notifications()
  print('Got Notifications:  {}'.format(notices))
  # notices.reverse()
  
  #nathan_server = bot.get_channel(id=904750102126657616)
  #zaroom = bot.get_channel(id=934322824540209202)
  #veg = bot.get_channel(id=871256858587979816)


  for notice in reversed(notices):
    #topic.reverse()
    #url.reverse()
    #print("notice: ".format(notice))

    # Space in url causing err: In embed.url: Not a well formed URL
    # %20 is for space
    # url = quote(notice['url'])
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
  return(1)

from cogs.rest_of_world_functions import get_articles


async def unleash_rest_of_World():
  # channel_id = 1098474629766578280  # veg
  # channel_id = 1132858904582311946  # ai4growth moderator_only
  # channel_id = 1154660261106552832  # ai4growth test_channel
  # channel_id = 1160197406848192613  # ai4growth leaderboard channel
  channel_id = 1132855697332256849  # ai4growth news channel
  channel = bot.get_channel(channel_id)
  articles = get_articles()
  print(f'\n\n new articles from rest of world: {list(articles)} \n\n')
  for article in articles:
    await channel.send(article['link'])
    await asyncio.sleep(1)

async def send_most_active():
  print('getting most active members...')
  # channel_id = 1098474629766578280  # veg to_read
  # channel_id = 1132858904582311946  # ai4growth moderator_only
  # channel_id = 1154660261106552832  # ai4growth test_channel
  channel_id = 1160197406848192613  # ai4growth leaderboard
  channel = bot.get_channel(channel_id)
  # await channel.send('.')

  print(f'guild: {dir(channel)} guild:{channel.guild}'
        )  #  {channel.guild}') # {channel.message.guild}')
  # await ctx.send('wait.')
  # Get the start of the current day
  channels_to_exclude = [
      1132857202911215759, 1132858472212467712, 1132858133413371915,
      1132858904582311946, 1154660261106552832
  ]
  today = datetime.now()
  # start_of_day = datetime(today.year, today.month, today.day)
  start_of_week = today - timedelta(days=today.weekday() + 1)  # start_of_week

  message_dict = {}
  # Iterate over all text channels in the server
  for msg_channel in channel.guild.text_channels:
    # for channel in ctx.guild.get_all_channels():
    if int(msg_channel.id) in channels_to_exclude:
      continue
      await asyncio.sleep(.2)
    try:
      # List all the messages sent in the channel today
      messages = msg_channel.history(after=start_of_week)
      async for message in messages:
        await asyncio.sleep(.2)

        def to_ignore(message_author_roles):
          roles_to_ignore = [
              'admin', 'admins', 'moderator', 'moderators', 'bots'
          ]
          for role in message_author_roles:
            if role.name.lower() in roles_to_ignore:
              return True
          return False

        if not message.author.bot and not to_ignore(message.author.roles):
          # Dont display messages by bot
          if message.channel.name not in message_dict:
            message_dict[message.channel.name] = []
          message_dict[message.channel.name].append(
              {
                  'author': message.author.name,
                  'content': message.content
              }
          )  # 'created_at': message.created_at, 'channel_id': message.channel.id})
          print(
              f'{message.author.name} : {message.content} : {message.created_at}'
          )
        else:
          print(f'skip_message: {message.author.name} : {message.content}')
    except Exception as e:
      print(f"Couldn't fetch history from {channel.name}, {e}")
  print(f'\n\n wait.2 \n\n')
  # await channel.send('wait.')
  message_count = count_messages(messages=message_dict, how_many=15)
  # message_count = [('anon.sepian', 42)]
  # await channel.send('wait.2')
  print(f'message_count: {message_count}')
  msg_embed = create_stylish_leaderboard_embed(message_count,
                                               question_expired=False,
                                               is_most_active_leaderboard=True)
  await channel.send(embed=msg_embed)
1
@bot.event
async def on_ready():
  # await unleash_rest_of_World()
  # await send_most_active()
  # Run tasks concurrently using asyncio.gather
  # await most_active_task()
  print("ready!")
  # await asyncio.gather(
  #     quiz_loop_task(),
  #     unleash_subscription_task(),
  #     # most_active_task(),  # merged quiz_loop and most_active task for now.
  # )

  # bot.loop.create_task(status_task())

  # await bot.tree.sync(
  # )  # sync CommandTree in order for slash commands to appear : https://discordpy.readthedocs.io/en/v2.2.2/ext/commands/commands.html#hybrid-commands

  # print("Change bot profile pic")
  # pfp_path = "ai4growthorg_logo.jpeg"
  # fp = open(pfp_path, 'rb')
  # pfp = fp.read()
  # await bot.user.edit(avatar=pfp)
  # fp.close()

  print(f"Logged in as {bot.user.name}")
  print(f"Discord.py API version: {discord.__version__}")
  print(f"Python version: {platform.python_version()}")
  print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
  print("-------------------")
  # unleashing.start() # reddit posts
  # unleash_ioe_notifications.start()
  # unleash_news.start()  # news

def get_one_quiz_question(questions_file='questions.json'):
  # Read questions
  with open(questions_file, 'r') as file:
    questions = json.load(file)['questions']
  # questions

  # print(len(quqestions))
  # pop first question
  question = questions.pop(0)
  # print(len(questions))

  # Save remaining questions
  with open(questions_file, 'w') as file:
    json.dump({'questions': questions}, file, indent=4)

  question_args = question
  question_command = '.quiz \"' + '\", \"'.join(question_args) + '\"'

  return question_args, question_command

@tasks.loop(hours=24)
async def quiz_loop():
  # channel_id = 1098474629766578280  # veg
  # channel_id = 1132858904582311946  # ai4growth moderator_only
  # channel_id = 1154660261106552832  # ai4growth test_channel
  channel_id = 1160197406848192613  # ai4growth leaderboard channel
  channel = bot.get_channel(channel_id)
  print(f'channel: {channel}')
  # Get the command object
  command = bot.get_command('quiz')

  # quiz_args = ["Which of the following best defines Artificial Intelligence (AI)?", "The ability of a machine to mimic human intelligence", "The study of algorithms and statistical models that enable computers to perform tasks without explicit instructions", "A branch of computer science that focuses on creating intelligent machines capable of performing tasks that typically require human intelligence", "All of the above", "4"]
  # quiz_command = '.quiz "Which of the following best defines Artificial Intelligence (AI)?" "The ability of a machine to mimic human intelligence" "The study of algorithms and statistical models that enable computers to perform tasks without explicit instructions" "A branch of computer science that focuses on creating intelligent machines capable of performing tasks that typically require human intelligence", "All of the above" "4"'
  quiz_args, quiz_command = get_one_quiz_question()
  # Get the rest of the arguments
  command_args = quiz_args

  # Get the command object from the bot
  # command = bot.get_command(command_name)
  # msg = await channel.send('hi..')
  allowed_mentions = discord.AllowedMentions(everyone=True)
  msg = await channel.send(content=".", allowed_mentions=allowed_mentions)
  ctx = await bot.get_context(msg)
  print(f"ctx: {ctx} msg:{msg}")
  # ctx = await bot.get_context(channel.message)
  ctx.message.content = quiz_command  # Set the content to the full command string
  ctx.command = 'quiz'
  ctx.args = command_args
  print("invoking")
  # await bot.invoke(ctx, ["hello there", "how are you", "what is your name","what is your age"])
  await command(ctx, *command_args)

  # send new articles from rest of world
  await unleash_rest_of_World()

  now = datetime.now()
  if now.weekday() == 6:  # 6 is Sunday.
    print(f'\n\n sending most active leaderboard.')
    await send_most_active()


@quiz_loop.before_loop
async def before():
  hour = 20  # 7 PM

  # minute = 20
  # now = datetime.now()
  def get_kathmandu_datetime():
    utc_dt = pytz.utc.localize(datetime.utcnow())
    target_tz = pytz.timezone('Asia/Kathmandu')
    return utc_dt.astimezone(target_tz)

  now = get_kathmandu_datetime()
  # if now.minute >=minute:
  #     # If it's already past 9 PM, start the task at 9 PM tomorrow
  #     tomorrow = datetime.now() + timedelta(days=1)
  #     next_start_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day, hour, minute)
  # else:
  #     next_start_time = datetime(now.year, now.month, now.day, now.hour, minute)
  if now.hour > hour:
    # If it's already past 9 PM, start the task at 9 PM tomorrow
    tomorrow = now + timedelta(days=1)
    next_start_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day,
                               hour)
  elif now.hour == hour: # or now.hour == hour + 1:
    pass
  else:
    # If it's before 9 PM, start the task at 9 PM today
    next_start_time = datetime(now.year, now.month, now.day, hour)

    sleep_seconds = (
        next_start_time -
        datetime(now.year, now.month, now.day, now.hour)).total_seconds()
    print(
        f'next_quiz_start_time: {next_start_time}, sleep:{sleep_seconds} sec.')
    await asyncio.sleep(sleep_seconds)

async def quiz_loop_task():
  await quiz_loop.start()


async def unleash_subscription_task():
  await unleash_subscription.start()

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



# -----------------------------------
# Gemini Response
# -----------------------------------
import google.generativeai as genai
import dotenv
import os
dotenv.load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]
history = [
            {
                "role": "user",
                "parts": ["imagine you are an AI researcher at NAAMII Institute. NAAMII stands for NepAl Applied Mathematics and Informatics Institute. it is an institute in nepal. you are researching on implementing AGI. your name is \"Genna GenAi\". you are answering queries of users in a discord channel called \"AI4GROWTH\". AI4GROWTH is the result of partnership of \"NAAMII\" and \"Kings college\". AI4GROWTH offers AI courses. .please answer questions i will ask subsequently. Also please do not introduce yourself unless someone explicitly asks you to do so."]
            }
            ,
            {
                "role": "model",
                "parts": ["ok."]
            }
        ]
model = genai.GenerativeModel(model_name="gemini-1.0-pro-001",      # "gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)
def get_gemini_response(query):
    convo = model.start_chat(history=history)
    convo.send_message(query)
    history.extend([
      {"role": "user", "parts": [query]},
      {"role": "model", "parts": [convo.last.text]}
      ])
    last_text = convo.last.text
    return last_text, history
# -----------------------------------
# ///////Gemini Response//////////////
# -----------------------------------


random_emo = RandomEmoji()    
async def process_vent_and_games(message):
    # checking and implementing vent_channel
    vent_db = db('vent')
    # vent_channels = vent_db.get_all()
    
    count_db = db('count')
    vent_db = db('vent')
    vent_channels = vent_db.get_all()
    gemini_chat_db = db('gemini_chat')
    gemini_chat_channels = gemini_chat_db.get_all()
    if int(message.channel.id) in vent_channels and message.clean_content != '.vent':
      # if vent_db.exists(message.channel.id) and message.clean_content != '.vent':
      print(f'\n\n proceed vent channel:{message.channel.id} in \'vent\' exists_in_vent_db:{True} clean_content:{message.clean_content}\n\n')
      
      message_channel = message.channel
      print(f'content_types:{[a.content_type for a in message.attachments]}')
      
      # Check if the message has an image attachment
      if len(message.attachments) == 0:
        # await ctx.send("This message doesn't contain an image attachment.")
        message_text = message.content
        await message.delete()  # deleting message
        
        embed = get_anonymous_message(message_text, message.author.id, random_emo)  # sending message
        await message.channel.send(embed=embed)
        # print(f'\n\n response time: {time.time() - start_time} \n\n ')
      
      else:
          # Create a list of file objects from the attachments
          files = [await attachment.to_file() for attachment in message.attachments]

          await message.delete()  # deleting message

          # Send the files along with the message text
          await message_channel.send(message.content, files=files)
      return True
    
    elif int(message.channel.id) in gemini_chat_channels and message.clean_content != '.chat':
        # with bot.typing(message.channel):
        gemini_response, _ = get_gemini_response(str(message.clean_content))
        await message.reply(gemini_response)
    elif count_db.exists(message.channel.id) and message.clean_content != '.count':
       print('\nproceed count\n')
       await proceed_count(message, count_db)

    else:
      print(f"\n{message.author}: {message.content}\n")
      await bot.process_commands(message)
# The code in this event is executed every time someone sends a message, with or without the prefix
@bot.event
async def on_message(message):
    # start_time = time.time()
    # Ignores if a command is being executed by a bot or by the bot itself
    if message.author == bot.user or message.author.bot:
        # ignoring messages by bots
        return
    elif message.author.id not in config.BLACKLIST:
        # Process the command if the user is not blacklisted
        print('\n\n author not black_listed \n\n')
        await process_vent_and_games(message)

        # await process_message(message)
    else:
      # Send a message to let the user know he's blacklisted
      context = await bot.get_context(message)
      embed = discord.Embed(
        title="You're blacklisted!",
        description="Ask the owner to remove you from the list if you think it's not normal.",
        color=0x00FF00
      )
      await context.send(embed=embed)

from quiz_db.quiz_questions import QuizQuestions
from quiz_db.quiz_scores import QuizScores
from cogs.quiz_functions import update_scores, create_stylish_leaderboard_embed, get_question_embed

global player

@bot.event
async def on_reaction_add(reaction, user, a=''):
  #embed = reaction.embeds[0]
  #emoji = reaction.emoji
  #print('hii')
  #await reaction.message.add_reaction('♥️')
  if not user.bot:
    await reaction.message.add_reaction(reaction)
    return
    # check quiz question
    quiz_question = QuizQuestions.get_question(reaction.message.id)
    if quiz_question and quiz_question['active']:
      print('quiz_question')
      response = await update_scores(quiz_question, reaction, user)
      leaderboard_data = response['leaderboard_data']
      if response['question_expired']:
        print('question expired')
        # edit question and tick the correct answer
        question_message = await reaction.message.channel.fetch_message(
            quiz_question['question_id'])
        # await question_message.edit(embed=get_question_embed('context', question_text=quiz_question['question'], options=list(quiz_question['options']), question_expired=True, answer_index=int(quiz_question['answer_index'])), silent=False)
        question_message = await question_message.edit(
            embed=get_question_embed('dummey_context',
                                     question_text=quiz_question['question'],
                                     options=list(quiz_question['options']),
                                     question_expired=True,
                                     answer_index=int(
                                         quiz_question['answer_index'])), )

        await question_message.add_reaction("1️⃣")
        await question_message.add_reaction('2️⃣')
        await question_message.add_reaction('3️⃣')
        await question_message.add_reaction('4️⃣')

      # update leaderboard message
      leaderboard_message = await reaction.message.channel.fetch_message(
          quiz_question['leaderboard_message_id'])

      await leaderboard_message.edit(
          embed=create_stylish_leaderboard_embed(leaderboard_data))

      print(f'removing user reaction: {user}')
      await reaction.remove(user)
    else:
      # reaction by bot
      return
      #  pass
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
      if config.playing == 'fm':

        print('Playing next, current:{}'.format(config.stream))
        config.stream = get_stream('next', config.stream)
        config.player.stop()
        config.player.play(FFmpegPCMAudio(config.stream['url']))

        embed = get_embed(reaction, user, config.stream)
        await config.currently_playing_message.edit(embed=embed)

      #message.send('Hello World')
      #play_next()

    # previous emoji
    elif str(reaction.emoji) == "⏮️":
      if config.playing == 'fm':

        print('Playing next, current:{}'.format(config.stream))
        config.stream = get_stream('prev', config.stream)
        config.player.stop()
        config.player.play(FFmpegPCMAudio(config.stream['url']))

        embed = get_embed(reaction, user, config.stream)
        await config.currently_playing_message.edit(embed=embed)

      print('Playing next')

    # download emoji
    elif str(reaction.emoji) == "⬇️":
      if config.playing != 'fm':
        if not 'downloads' in os.listdir():
          os.mkdir('downloads')
        print('Try download')

        async with reaction.message.channel.typing():

          URL, thumbnails, title, vid_url = await YTDLSource.from_url(
              config.playing, loop=bot.loop, download=True)

          full_downloaded_file_name = title + '.mp3'

          await reaction.message.channel.send(
              file=discord.File(full_downloaded_file_name))
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
async def on_raw_reaction_add(payload):
  '''
  <RawReactionActionEvent message_id=1171890158287732777 user_id=861131196779331624 channel_id=1160197406848192613 guild_id=1132851455028637706 emoji=<PartialEmoji animated=False name='4️⃣' id=None> event_type='REACTION_ADD' member=<Member id=861131196779331624 name='anon.sepian' global_name='anon' bot=False nick=None guild=<Guild id=1132851455028637706 name='AI4GROWTH' shard_id=0 chunked=True member_count=663>>>
  '''
  # return
  print("raw reaction")
  if not payload.member.bot:
    print('not bot')
    channel = bot.get_channel(payload.channel_id)
    print(f'channel:{channel}')
    message = await channel.fetch_message(payload.message_id)
    print(f'message:{message}')
    # Mirror Reaction
    await message.add_reaction(payload.emoji)
    # check quiz question
    quiz_question = QuizQuestions.get_question(payload.message_id)
    print('got question')
    print(f'quiz_question:{quiz_question} {payload.message_id}')
    if quiz_question:
      leaderboard_data = await update_scores(question=quiz_question,
                                             raw_reaction=True,
                                             message=message,
                                             payload=payload)
      print(
          f'\n\n---------------------- \n got leaderboard data:{leaderboard_data} \n\n'
      )
      leaderboard_message = await channel.fetch_message(
          quiz_question['leaderboard_message_id'])

      await leaderboard_message.edit(embed=create_stylish_leaderboard_embed(
          leaderboard_data['leaderboard_data']))
      # remove reaction
      for reaction in message.reactions:
        print(f'+reaction:{reaction}')
        # if not reaction.me:
        try:
          await reaction.remove(bot.get_user(payload.user_id))
          print(
              f'-reaction:{reaction} \n{payload.member} \n{bot.get_user(payload.user_id)}'
          )
        except Exception as Ex:
          print(Ex)

    else:
      return
  # print(payload)
  print(payload.emoji)



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
  print(error)
  if isinstance(error, commands.CommandOnCooldown):
    embed = discord.Embed(
      title="Error!",
      description="This command is on a %.2fs cooldown" % error.retry_after,
      color=0x00FF00
    )
    await context.send(embed=embed)
    raise error


# await only inside async function
async def load_extensions():
  for filename in os.listdir("./cogs"):
        if filename.endswith("cog.py"):
            try:
                # cut off the .py from the file name
                extension_name = f"cogs.{filename[:-3]}"
                await bot.load_extension(extension_name)
    
                print(f"Loaded extension '{extension_name}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension_name}\n{exception}")
            # extension = extension.replace("cogs.", "")
            # await bot.load_extension(extension)


if __name__ == "__main__":
  asyncio.run(load_extensions())
  bot.run(config.DISCORD_TOKEN)     # run discord bot


# --------------------
# Running in Replit
# --------------------
# async def change_logo():
#   # create logs.json for storing commands logs
#   if not os.path.exists('logs.json'):
#     with open('logs.json', 'w') as file:
#       file.write('{}')

# if __name__ == "__main__":
#   asyncio.run(load_extensions())
#   asyncio.run(change_logo()) # change the logo
# from keep_alive import keep_alive
#   keep_alive()
#   bot.run(config.DISCORD_TOKEN)  # run discord bot



#client.loop.create_task(my_background_task())




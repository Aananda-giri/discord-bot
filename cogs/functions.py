""""
Copyright © Krypton 2020 - https://github.com/kkrypt0nn
Description:
This is a template to create your own discord bot in python.

Version: 2.0
"""

import discord, os, config
# from discord.ext.commands import Bot
# from discord.ext import commands


import string, random
# import os, discord, asyncio, os, platform, sys, asyncprawcore
import requests
import json
# import math, random
from database import db
import asyncpraw
#import commands

import time, datetime
# from discord.ext import tasks
# from discord import Member
# from discord.ext.commands import has_permissions, MissingPermissions
# from prawcore import NotFound
#import ffmpeg

reddit = asyncpraw.Reddit(
    client_id= config.RD_CLIENT_ID,# os.environ['RD_CLIENT_ID'],
    client_secret= config.RD_CLIENT_SECRET, # os.environ['rd_client_secret'],
    password= config.RD_PASS,    # os.environ['rd_pass'],
    user_agent="praw_test",
    username="Alternative-Ad-8849",
)

#from discord import FFmpegPCMAudio
from dotenv import load_dotenv

load_dotenv()

async def proceed_count(message, count_db):
        print("\n Try processing count \n")
        
        if not message.content.isdigit():
            return

        channel_id = str(message.channel.id)
        new_count = int(message.content)
        count_data = count_db.get_one(channel_id)   # dict of data

        previous_counter = count_data['current_author']
        previous_count = int(count_data['current_count'])
        new_counter = str(message.author)
        # current_score = previous_count
        highest_score = int(count_data['highest_score'])
        
        if new_count == (previous_count + 1):
            if not new_counter == previous_counter:
                # new_count = previous_count + 1 and new_counter != previous_counter
                new_highest_score = new_count if (new_count > highest_score) else highest_score
                count_db.add_one_chain_word(channel_id, current_word = new_count, current_author = new_counter, current_score = new_count, highest_score = new_highest_score)
                
                await message.add_reaction('✅')
            else:
                # new_count = previous_count + 1 and new_counter = previous_counter
                
                count_db.add_one_chain_word(channel_id, current_word = 0, current_author = '', current_score = 0, highest_score = highest_score)
                
                await message.add_reaction('❌')

                title = "**!!Same person can't count two numbers in a row.**"
                description = f"**{message.author.mention} RESTARTING COUNT** \n highest_score: **{highest_score}** \n !! Next number is: **1**"
                embed = discord.Embed(title=title, description=description, color=0x9b59b6)

                await message.channel.send(embed=embed)
                # embed.description = "Vote [here](https://top.gg/bot/862191340355715093/vote) to earn saves so you can continue counting next time. See .help games"
        elif type(new_count)==int:    
            # new_count != previous_count + 1 and it is integer
            count_db.add_one_chain_word(channel_id, current_word = 0, current_author = '', current_score = 0, highest_score = highest_score)
            
            await message.add_reaction('❌')

            # await message.channel.send("{} RUINED IT AT **{}**!! Next number is: **1 Wrong number**.".format(message.author.mention, current_count))
            await message.channel.send(f"**!!Wrong Number** \n {message.author.mention} RESTARTING COUNT \n highest_score: **{highest_score}** \n !! Next number is: **1** \n")
            embed = discord.Embed(color=0x9b59b6)
            # embed.description = "Vote [here](https://top.gg/bot/862191340355715093/vote) to earn saves so you can continue counting next time. See .help games"
            await message.channel.send(embed=embed)

async def proceed_chain(message):
        # updating word chain data
        print("\n Try updating word chain \n")
        
        chain_word_db = db('chain_word')
        channel_id = str(context.channel.id)
        
        # dictionary of data
        chain_word_data = chain_word_db.get_one(channel_id)

        previous_author = chain_word_data['last_counter']
        previous_word = chain_word_data['current_word']
        current_score = chain_word_data['current_score']
        highest_score = int(chain_word_data['highest_score'])
        
        new_author = str(message.author)
        new_word = str(message.content)[1:-1].strip()
        
        search_response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{new_word}/').json()
        
        
        try:
            # try searching error message
            
            if previous_word =='' or new_word==None:
                # word exists raise exception and proceed
                raise ValueError("Last word empty! please proceed")
            if str(last_word)[-1] != new_word[0]:
                # raise ValueError("Word doesn't start with previous word's last letter")
                response = "Starting letter didn\'t match with previous word's last letter"
            elif previous_author == new_author:
                response = "You can't enter two words in a row."
            else:
                title = search_response['title']
                if title == 'No Definitions Found':
                    response = "Word doesn\'t exist"
                    # word doesn't exists
                else:
                    # word exists raise exception and proceed
                    raise ValueError("word exists! please proceed...")
            
            # updating values in database
            count_db.add_one_chain_word(channel_id, current_word = '', current_author = '', current_score = 0, highest_score = highest_score)

            await message.add_reaction('❌')
            await message.channel.send("{} RUINED IT AT ** {} {}**!! **Next word starts with:\"{}\", **.".format(message.author.mention, chain_length, response, 'anything you want'))
            
            embed = discord.Embed(color=0x9b59b6)
            embed.description = "Vote [here](https://top.gg/bot/862191340355715093/vote) to earn saves so you can continue next time. See .help games"
            await message.channel.send(embed=embed)
        except:
            # word exists and starts with ending of previous word
            meaning = search_response[0]['meanings'][0]['definitions'][0]['definition']
            print("meaning: {} ".format(meaning))

            # updating values in database
            current_score += 1
            new_highest_score = current_score if current_score > highest_score else highest_score
            count_db.add_one_chain_word(channel_id, current_word = new_word, current_author = new_author, current_score = current_score, highest_score = new_highest_score)

            await message.add_reaction('✅')
            await message.channel.send('**{}** : {}'.format(new_word, meaning.split('.')[0]))   #get first sentence of meaning


def get_embeded_message(context, title, description='', author=True):
    print(f'\n embed_title: {title} avatar:{context.author.avatar}\n')
    embed = discord.Embed(
            title=title,
            description=description,
            color=0x00FF00
        )
    
    #embed.set_author(name=context.message.author)
    #embed.set_thumbnail(url=context.author.avatar_url)
    
    embed.add_field(
            name="Over!",
            #value=":ping_pong:",
            value=":pizza:",
            inline=True
        )
    if author: #author=False for perodic unleash/subscription
      embed.set_footer(text=f'{context.author}',icon_url=context.author.avatar)
    return(embed)

def get_question_embed(context, question, options):
    # print(type(options))
    embed = discord.Embed(
        title=f"{question}",
        color=discord.Color.green()
    )
    numbers = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', ':keycap_ten:']
    
    for index, option in enumerate(list(options)):
        embed.add_field(
            name=f"{numbers[index]} {option}",
            value=f"",
            inline=False
        )
    return embed


def create_stylish_leaderboard_embed(leaderboard_data):
    # Create a new Discord embed
    embed = discord.Embed(
        title="Top 10 Leaderboard",
        color=discord.Color.green()
    )

    # Create the leaderboard text
    leaderboard_text = ""
    for rank, data in enumerate(leaderboard_data):
        username = data[0]
        score = data[1]['score']
        leaderboard_text += f"`{str(rank+1).rjust(4)}`      `{username.center(10)}`      `{str(score).center(5)}`\n\n"

        # print(leaderboard_text)
    # Add a field to the embed with the leaderboard text
    embed.add_field(
        name='Rank          User            Score',
        value=leaderboard_text,
        inline=True
    )
    return embed


# Good subreddit unleashing
async def get_meme(ctx, how_many, breaks = False):
  subreddit = 'memes'
  submissions = await reddit.subreddit(subreddit)
  #subreddit = await reddit.subreddit('memes')
  print('How many: ',how_many)
  
  selected_randoms = random.sample(range(1, 500), how_many)
  print(selected_randoms)
  randoms_count = 0
  send_count = 0
  loop_count = 0
  for i in range(how_many):
        #async for submission in submissions.hot(limit=30):
        submission = random.choice([meme async for meme in submissions.hot(limit=50)])

        #loop_count += 1
        #print('Loop: ',selected_randoms[randoms_count])
        #if selected_randoms[randoms_count] == loop_count:
        randoms_count += 1
        send_count += 1
        print('Unleash for loop:{}'.format(0))
        title = submission.title
        body = submission.selftext
        embed = discord.Embed(title=title,
                              url=submission.url,
                              description=body,
                              colour=discord.Color.red())
        embed.set_image(url=submission.url)
        #To set subreddit name in footer
        embed.set_footer(text="subreddit: \"r/{}\"".format(subreddit))
        print('Submission_url: ', submission.url)
        try:
            #To filter lenthy messages > 2500 letters
            if len(str(body)) < 2500:
                image_formats = ['jpg', 'jpeg', 'png']

                #checks if image_format in submission.url
                if sum([(i in str(submission.url)) for i in image_formats]):
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(submission.url)
        except:
            pass
'''elif loop_count == selected_randoms[-1]:
        if send_count != 0 or breaks==True:
          print('\nBreaking\n')
          break
          # breaks the loop the end of sending 'how_many' memes
        else:
          # try send two memes if didnot send any memes
          await get_meme(ctx, 2, breaks = True)'''



def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


def get_joke():
    response = requests.get("https://imao.herokuapp.com/api/jokes/random/")
    json_data = response.json()
    joke = str(json_data['title']) + ' : ' + str(
        json_data['body']) + ' - ' + str(json_data['author'])
    return (joke)


def get_jokes(no_of_jokes):
    response = requests.get("https://imao.herokuapp.com/api/jokes/{}/".format(
        int(no_of_jokes)))
    jokes = []
    for joke in response.json()['jokes']:
        jokes.append(
            str(joke['title']) + ' : ' + str(joke['body']) + ' - ' +
            str(joke['author']))
    return (jokes)


def get_puns():
    return ('Puns are comming very very soon!')


def get_riddles():
    return ('Riddles are comming very very soon!')


def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragment(index):
    encouragements = list(db["encouragements"])
    #if len(encouragements) > index:
    if index in encouragements:
        #del encouragements[index]
        encouragements.remove(index)
        db["encouragements"] = encouragements


def sanitize_db():

    users = list(set(list(db["users"])))
    users_sanitized = []
    for user in users:
        users_sanitized.append(
            user.replace('\'', '').replace('\"', '').strip())
    db["users"] = users_sanitized
    print('Users sanitized. \n Users:')
    print(list(db["users"]))


def get_embed(reaction, user, stream):
  embed=discord.Embed(title=stream['name'],
    #description=stream['longDesc'],
    color=0x00FFFF,
    url=stream['url'])
  embed.set_author(
        name=user,
        )
        #icon_url=ctx.message.author.avatar_url)
  embed.set_thumbnail(url=stream['image'])
    
  #embed.pfp = author.avatar_url
  embed.timestamp = datetime.datetime.utcnow()
  embed.set_footer(text=f'Added by {user}', icon_url= user.avatar_url)
  return embed


class MySchedule:
    async def schedule_message(sth,context, 
                               author='anonymous',
                               message='please provide a message',
                               id=863298114949218324,
                               seconds=0):
        print('received:')
        print(author, message, id, seconds)
        #await ctx.message.delete()
        if author == 'anonymous':
            #author = 'anonymous'
            description = 'command: .anon your_message'
        else:
            author = author + '  <scheduled_message>'
            description = "command: .schedule time_in_seconds your_message"
            time.sleep(seconds)
            print('sleep 10 seconds')
        print('author : ', author)
        #channel = bot.get_channel(id=ctx.channel.id)
        #print('sending {}'.format(message))

        #retStr = str("""```css\nThis is some colored Text```""")
        #embed = discord.Embed(title="Random test")
        #embed.add_field(name="Name field can't be colored as it seems",value=retStr)
        #await ctx.send(embed=embed)

        #message = str(ctx.message.author).split('#')[0] + ' : ' + message
        embed = discord.Embed(title=author, colour=discord.Color.blue())
        embed.add_field(
            name=message,
            value=description,
        )
        await context.send(embed=embed)
        #channel = ctx.bot.get_channel(id=id)
        #await channel.send(embed=embed)


def get_anonymous_message(message, author_id, random_emo):
  # print(f'emoji_assigned:{random_emo.get_emoji(author_id)}')
  random_emoji, random_username = random_emo.get_emoji(author_id)
  embed = discord.Embed(
      title=f" {random_emoji} {random_username}",
      description=message,
      color=0x00ff00
  )
  # embed.set_author(name="title", icon_url=author_avatar_url)
  # embed.set_author(name="😄  title")
  # embed.set_thumbnail(url=author_avatar_url)
  # embed.set_footer(text=f'🗿',icon_url=author_avatar_url)
  # embed.set_footer(text=f'\'anon\'',icon_url='\U0001F578')
  return embed

class RandomEmoji:
    def __init__(self):
        self.emoji_dict = {}
        # Create a dictionary to store emoji assignments
        self.emojis_as_avatar = ['📓', ':merman:', ':ninja:', ':scales:', '🎚', ':desert:', ':clapper:', ':fist:', '⚕️', '🧠', '🗨️', '🖨', ':man_detective:', ':scroll:', '📚', ':bar_chart:', ':flag_au:', '🗃', '🧮', '📟', ':dragon:', ':diving_mask:', ':crystal_ball:', '🧲', ':alien:', ':rocket:', '📈', ':alembic:', ':smiling_imp:', '🖲', '⚖', '📖', '🔬', '🧪', '🗂', ':construction_site:', ':brain:', ':lizard:', ':man_artist:', '📔', ':sleeping:', ':man_mage:', ':tools:', ':pirate_flag:', '�', '🖋', ':spider_web:', ':speaking_head:', ':handshake:', '💡', '🕹', ':man_judge:', ':detective:', '📝', ':eye:', '📗', ':robot:', ':man_technologist:', ':baby:', '📕', '📋', '🤖', ':art:', '📏', '📙', '🧫', '💻', ':exploding_head:', ':computer:', '⌨', '📘', ':compass:', '📜', ':man_walking:', '📁', ':chess_pawn:', '🖥', ':dash:', '🗜', '🧑', '💾', ':musical_keyboard:', '📠', '📡', '🕰', ':woman_detective:', '🧬', '🌐', '🔍', '⚙', '🔎', '📂', '📊', '📒', ':dancer:', ':bulb:', '🖱', ':map:', '��']
        self.user_names = ['BinaryBaronet', 'LogicLynx', 'NeuralNetNinja', 'RoboticsRenegade', 'BitBaroness', 'ArtificialIntelligenceAstrologer', 'ReinforcementLearningRaider', 'NaturalLanguageProcessingNomadic', 'LearningLion', 'NaturalLanguageProcessingNinja', 'ArtificialIntelligenceAmbassador', 'DigitalDame', 'QuantumQuirk', 'ComputerVisionConnoisseur', 'NaturalLanguageProcessingNomad', 'TechTactician', 'CyberCerebrum', 'ReinforcementLearningRookie', 'DataScienceDiplomat', 'DeepLearningDisciple', 'CodeCraftsman', 'ProgramProdigy', 'AlgorithmAlchemist', 'DataDoyen', 'QuantumQuester', 'QuantumQueen', 'AI_Adventurer', 'RoboticsRevolutionist', 'CyberChampion', 'QuantumQuestioner', 'LogicLord', 'ArtificialIntelligenceAficionado', 'AlgorithmAdept', 'ComputeCatalyst', 'DigitalDeity', 'LearningLegend', 'TechTitan', 'AlgorithmArtisan', 'CyberSavant', 'ModelMaven', 'RoboticsRobotics', 'TechTinker', 'QuantumKing', 'InsightInnovator', 'DataScienceScholar', 'RoboticsRebel', 'ModelMonarch', 'BinaryBelle', 'DeepLearningDeveloper', 'ReinforcementLearningRevolutionist', 'BinaryBrain', 'CodeConnoisseur', 'TechTemplar', 'MachineLearningMythbuster', 'TechTycoon', 'DeepLearningDynamo', 'ModelMatriarch', 'AlgorithmArtist', 'CodeCount', 'ReinforcementLearningRenegade', 'AI_Artisan', 'LogicLady', 'NeuralNetworkNetworker', 'NaturalLanguageProcessingProdigy', 'DataDrivenDev', 'DataDuchess', 'MachineLearningMythologist', 'DataDiva', 'ArtificialIntelligenceArchivist', 'MachineLearningMagician', 'CyberCognoscenti', 'ModelMaestro', 'ByteBoss', 'ComputerVisionCryptozoologist', 'NeuralNetworkNomad', 'DeepLearningDragon', 'NaturalLanguageProcessingNewbie', 'ReinforcementLearningRoadrunner', 'AnalysisArtisan', 'DeepLearningDiver', 'NeuralNetworkNerd', 'AlgorithmAristocrat', 'NeuralNetworkNegotiator', 'CyberCount', 'MachineLearningMastermind', 'AI_Alchemist', 'ReinforcementLearningStrategist', 'ComputerVisionCartographer', 'ArtificialIntelligenceAdventurer', 'SystemStrategist', 'CodeCzar', 'TechTrailblazer', 'CodeCountess', 'DataScienceDetective', 'NeuralNetworkNinja', 'RoboticsReformer', 'MachineMindset', 'DataDuke', 'BinaryBaron', 'DigitalDuke', 'AlgorithmArchitect', 'MachineLearningMaestro', 'BitBard', 'DeepLearningDreamer', 'DigitalDreamer', 'NeuralNavigator', 'ArtificialIntelligenceAnalyst', 'NeuralNetworkNavigator', 'ReinforceRanger', 'MachineMaestro', 'AlgorithmAnimator', 'MachineMind', 'ComputerVisionCryptid', 'InformationIlluminator', 'DataDynamo', 'SyntaxSorcerer', 'CircuitSage', 'DeepLearningDancer', 'NetworkNavigator', 'PatternProphet', 'DataScienceSherlock', 'BitBaron', 'CodeConductor', 'ComputerVisionChameleon', 'LearningLuminary', 'BotBrainiac', 'DigitalDruid', 'AlgorithmAce']


    def get_emoji(self,user_id):
        # Check if the user already has an emoji
        if user_id in self.emoji_dict:
            return self.emoji_dict[user_id]

        # If the user does not already have an emoji, assign one to them
        else:
            emoji, user_name = self.get_random_emoji()
            self.emoji_dict[user_id] = [emoji, user_name]
            return [emoji, user_name]

    # Get a random emoji
    def get_random_emoji(self):
        return [random.choice(self.emojis_as_avatar), random.choice(self.user_names)]

def get_embeded_message(context, title, description='', author=True):
  print(f'\n embed_title: {title} avatar:{context.author.avatar}\n')
  embed = discord.Embed(title=title, description=description, color=0x00FF00)

  #embed.set_author(name=context.message.author)
  #embed.set_thumbnail(url=context.author.avatar_url)

  embed.add_field(
      name="Over!",
      #value=":ping_pong:",
      value=":pizza:",
      inline=True)
  if author:  #author=False for perodic unleash/subscription
    embed.set_footer(text=f'{context.author}', icon_url=context.author.avatar)
  return (embed)

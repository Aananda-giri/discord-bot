import discord
from discord.ext import commands
import os
import time, asyncio
from dotenv import load_dotenv
load_dotenv()
import datetime


intents = discord.Intents().all()
intents.messages = True
intents.reactions = True
intents.presences = True
intents.members = True  # To cache the every user For on_remove_reaction to be usable
intents.guilds = True
intents.emojis = True
intents.bans = True

#- ------------------------
#- ------------------------
# questions have: {Channel_id: [{message_id, question, options, answer, leaderboard_message_id, created_datetime, expire_date_time, reacted_users, correctly_answered_users}]}
global questions
questions = {}

# Scores have: {server_id: {[user_id, score, server_id]}}
global scores
scores = {}



def get_embeded_message(context, title, description='', author=True):
    # print(f'\n embed_title: {title} avatar:{context.author.avatar}\n')
    embed = discord.Embed(
            title=title,
            description=description,
            color=0x00FF00
        )
    embed.add_field(
            name="Over!",
            value=":pizza:",
            inline=True
        )
    if author: #author=False for perodic unleash/subscription
      embed.set_footer(text=f'{context.author}',icon_url=context.author.avatar)
    return(embed)

import discord

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


bot = commands.Bot(command_prefix="!", description="The description", intents=intents)

@bot.event
async def  on_ready():
    print("Ready !")

def update_scores(emoji, reaction_time, username, server_id, message):
    '''
    - check:
        - has not already reacted
        - reacted within the time limit
        - reacted to the correct answer
        
        
    - update scores
    - sort scores on server = server[server_id] by scores
    - return top 10
    '''
    question = questions[message.id]
    if username not in question['reacted_users']:
        print('username not in reacted_users')
        if reaction_time < question['expire_date_time']:
            print('\n\nvalid reaction time')
            print(question['answer'])
            if emoji == question['answer']:
                print('\n\ncorrect answer')    
                # add user to reacted users
                question['reacted_users'].append(username)
                
                # add user to scores if not already there
                if username not in scores[server_id]:
                    scores[server_id][username] = {'score':0}
                
                # update score of user
                scores[server_id][username]['score'] += 1
                
                # update correctly_answered_users
                question['correctly_answered_users'].append(username)

                # sorted scores
                print(scores)
                print(server_id)
                sorted_scores = sorted(scores[server_id].items(), key=lambda x: x[1]['score'], reverse=True)

                print(f'\n\n sorted_scores: {sorted_scores} \n\n')
    return sorted_scores[:10]   # top 10

@bot.event
async def on_reaction_add(reaction, user):
    if not user.bot:
        
        # Get the message that the user reacted to
        message = reaction.message

        # Get the username of the user who reacted
        username = user.display_name

        # Get the time that the user reacted
        reaction_time = reaction.message.created_at

        # Get the emoji that the user reacted with
        emoji = reaction.emoji

        # Display the username, time, and emoji in the channel
        # await message.channel.send(f"{username} reacted with {emoji} at {reaction_time}.")

        print(f'content:{reaction.emoji} \n\
               time:{reaction.message.created_at} type:{type(reaction.message.created_at)}\n \
               name:{reaction.message.author.name}\
              ')

        server_id = reaction.message.guild.id
        channel = reaction.message.channel
        
        leaderboard_data = update_scores(emoji = emoji, reaction_time=reaction_time, username=username, server_id=server_id, message=message)

        leaderboard_embed = create_stylish_leaderboard_embed(leaderboard_data)
        leaderboard_message_id = questions[message.id]['leaderboard_message_id']
        leaderboard_message = await channel.fetch_message(leaderboard_message_id)
        await leaderboard_message.edit(embed=leaderboard_embed)

@bot.command()
async def ping(ctx):
    await ctx.send(embed= get_embeded_message(ctx, 'ping-pong', 'this is body', author=False), silent=True)

@bot.command()
async def quiz(ctx, question, *options):
    print(f'\n ctx:{ctx}\n question: {question} options:{options}\n')
    question_message = await ctx.send(embed= get_question_embed(ctx, question, options), silent=True)
    
    await question_message.add_reaction("1️⃣")
    await question_message.add_reaction('2️⃣')
    await question_message.add_reaction('3️⃣')
    await question_message.add_reaction('4️⃣')
    
    # Create a list of user data (rank, username, score)
    leaderboard_data = [('cnon', {'score': 6}), ('bnon', {'score': 3}), ('enon', {'score': 3}), ('dnon', {'score': 2}), ('fnon', {'score': 2}), ('anon', {'score': 6})]
    leaderboard_message = await ctx.send(embed= create_stylish_leaderboard_embed(leaderboard_data), silent=False)
    server_id = ctx.guild.id
    global questions
    questions[server_id] = {
            'message_id':question_message.id,
            'channle_id':ctx.channel.id,
            'question':question,
            'options':options,
            'answer':'1️⃣',
            'leaderboard_message_id':leaderboard_message.id,
            'created_datetime':question_message.created_at,
            'expire_date_time':question_message.created_at + datetime.timedelta(minutes=60),    # Expires after 60 minutes
            'reacted_users':[],
            'correctly_answered_users':[]
    }

    global scores
    if server_id not in scores:
        scores[ctx.guild.id] = {
            'anon': {'score':6},
            'bnon': {'score':3},
            'cnon': {'score':6},
            'dnon': {'score':2},
            'enon': {'score':3},
            'fnon': {'score':2},

            }
    return
    

    

bot.run(os.environ.get('TEST_BOT_TOKEN'))

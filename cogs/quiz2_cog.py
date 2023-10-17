import os, sys, discord, platform, random, aiohttp, json, datetime, requests
from discord.ext import commands
from multiprocessing import context
from .quiz_functions import get_question_embed, create_stylish_leaderboard_embed

from quiz_db.quiz_scores import QuizScores
from quiz_db.quiz_questions import QuizQuestions
import datetime

class Quiz(commands.Cog, name="quiz"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="quiz", brief=" short_help: to test if bot responding  ",
             help='quiz: e.g. .ping', aliases=[], ephermal=True, hidden=True, usage='.quiz')
    async def quiz(self, context, question: str, option1: str, option2: str, option3: str, option4: str, answer_index: str):
        
        print(f"question: \"{question}\" options: {option1, option2, option3, option4} answer_index: {answer_index}")
        options = [option1, option2, option3, option4]
        # number_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
        # answer = number_emojis[int(answer_index)-1]
        
        question_message = await context.send(embed = get_question_embed(context, question, options), silent=True)
    
        await question_message.add_reaction("1️⃣")
        await question_message.add_reaction('2️⃣')
        await question_message.add_reaction('3️⃣')
        await question_message.add_reaction('4️⃣')
        server_id = context.guild.id

        # Create a list of user data (rank, username, score)
        leaderboard_data = QuizScores.get_top_ten(server_id)
        # leaderboard_data = [('cnon', {'score': 6}), ('bnon', {'score': 3}), ('enon', {'score': 3}), ('dnon', {'score': 2}), ('fnon', {'score': 2}), ('anon', {'score': 6})]
        # leaderboard_data = 
        leaderboard_message = await context.send(embed= create_stylish_leaderboard_embed(leaderboard_data), silent=False)
        
        
        # save question
        expire_datetime = question_message.created_at + datetime.timedelta(hours=3)     # Expires after 3 hours minutes
        # print(server_id, question_message.id, question, options, int(answer_index), leaderboard_message.id, question_message.created_at, expire_datetime, [], [], True)
        QuizQuestions.add_question(server_id, channel_id=context.channel.id, question_id=question_message.id, question=question, options=options, answer_index=int(answer_index), leaderboard_message_id=leaderboard_message.id, created_datetime=question_message.created_at, expire_date_time=expire_datetime, users_reacted=[], correctly_answered_users=[], active=True)
        # QuizScores.add_score(user_name=1, server_id=863298114491514891, score=10)
        return
    
    @commands.command(name='quiz', aliases=[], brief='quiz questions', help='vent_channels make every message anonymous by deleting and re-posting user\'s messages \n e.g. `.quiz complete question option1 option2 option3 option4 answer_index` ')
    async def quiz(self, context, question, *options):
        # await context.send(response_message)
        await context.message.delete()
        print(f'\n ctx:{context}\n question: {question} options:{options}\n')
        answer_index = list(options).pop()
        options = list(options)[:-1]
        print(f"question: \"{question}\" options: {options} answer_index: {answer_index}")
        # options = [option1, option2, option3, option4]
        # number_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
        # answer = number_emojis[int(answer_index)-1]
        
        question_message = await context.send(embed = get_question_embed(context, question, options), silent=True)
    
        await question_message.add_reaction("1️⃣")
        await question_message.add_reaction('2️⃣')
        await question_message.add_reaction('3️⃣')
        await question_message.add_reaction('4️⃣')
        server_id = context.guild.id

        # Create a list of user data (rank, username, score)
        leaderboard_data = QuizScores.get_top_ten(server_id)
        # leaderboard_data = [('cnon', {'score': 6}), ('bnon', {'score': 3}), ('enon', {'score': 3}), ('dnon', {'score': 2}), ('fnon', {'score': 2}), ('anon', {'score': 6})]
        # leaderboard_data = 
        leaderboard_message = await context.send(embed= create_stylish_leaderboard_embed(leaderboard_data), silent=False)
        
        
        # save question
        expire_datetime = question_message.created_at + datetime.timedelta(hours=3)     # Expires after 3 hours minutes
        # print(server_id, question_message.id, question, options, int(answer_index), leaderboard_message.id, question_message.created_at, expire_datetime, [], [], True)
        print(f'\ncreaeted_At: {question_message.created_at} {type(question_message.created_at)}')
        QuizQuestions.add_question(server_id, channel_id=context.channel.id, question_id=question_message.id, question=question, options=options, answer_index=int(answer_index)-1, leaderboard_message_id=leaderboard_message.id, created_datetime=question_message.created_at, expire_date_time=expire_datetime, users_reacted=[], correctly_answered_users=[], active=True)
        # QuizScores.add_score(user_name=1, server_id=863298114491514891, score=10)
        return
    
async def setup(bot):
    await bot.add_cog(Quiz(bot))






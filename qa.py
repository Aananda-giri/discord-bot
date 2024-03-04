"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""
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










import interactions
import discord
from discord.ext import commands
import config, asyncio
from cogs.functions import get_embeded_message
config.init()
from database import db

bot = commands.Bot(command_prefix="!", description="The description", intents=config.intents)
# bot = discord.Client()

@bot.event
async def  on_ready():
    print("Ready !")
    # await bot.interactions.sync_all_commands()
    await bot.tree.sync() # sync CommandTree in order for slash commands to appear : https://discordpy.readthedocs.io/en/v2.2.2/ext/commands/commands.html#hybrid-commands

import math, asyncpraw, asyncprawcore


@bot.hybrid_command(name='ping', description='test')
async def ping(ctx, what='pong'):
    await ctx.send(embed= get_embeded_message(ctx, 'ping-pong', f'this is body, what:{what}', author=False))
    # await ctx.send('**pong**: The silent reply',  silent=True)

@bot.event
async def on_message(message):
    print(f'messaged: {message.clean_content}')
    gemini_chat_db = db('gemini_chat')
    gemini_chat_channels = gemini_chat_db.get_all()
    if message.author.bot:
      return
    if int(message.channel.id) in gemini_chat_channels and message.clean_content != '.chat':
        # with bot.typing(message.channel):
        gemini_response, _ = get_gemini_response(str(message.clean_content))
        await message.reply(gemini_response)
        


bot.run(config.DISCORD_TEST_BOT_TOKEN)




# if __name__=="__main__":
#     last_text, history = get_gemini_response("I need help.")
#     print(last_text)
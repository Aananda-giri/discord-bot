import datetime
from discord.ext import commands
from .quiz_functions import get_question_embed, create_stylish_leaderboard_embed


from datetime import datetime
import time
def count_messages(messages, how_many=None):
    print('counting messages')
    message_count = {}
    for channel in messages:
        for message in messages[channel]:
            if message['author'] in message_count:
                message_count[message['author']] += 1
            else:
                message_count[message['author']] = 1

    message_count = sorted(message_count.items(), key=lambda x: x[1], reverse=True)
    return message_count[:how_many]


class Stats(commands.Cog, name="stats"):

  def __init__(self, bot):
    self.bot = bot

  @commands.hybrid_command(name="pinge",
                           brief=" short_help: to test if bot responding  ",
                           help='pinge: e.g. .pinge',
                           aliases=[],
                           ephermal=True,
                           hidden=True,
                           usage='.pinge')
  async def pinge(self, context):

    await context.send('hie')
  
  @commands.hybrid_command(name="most_active",
                           brief=" short_help: to test if bot responding  ",
                           help='pinge: e.g. .pinge',
                           aliases=[],
                           ephermal=True,
                           hidden=True,
                           usage='.most_active')
  async def most_active(self, ctx):
      # @commands.command(name='most_active', aliases=[])
      # async def most_active(self, ctx):
      print(f'guild: {dir(ctx)} {ctx.guild} {ctx.message.guild}')
      await ctx.send('hie')
      # Get the start of the current day
      channels_to_exclude = [
          1132857202911215759, 1132858472212467712, 1132858133413371915,
          1132858904582311946, 1154660261106552832
      ]
      today = datetime.now()
      # start_of_day = datetime(today.year, today.month, today.day)
      start_of_week = today - timedelta(days=today.weekday()+1)

      message_dict = {}
      # Iterate over all text channels in the server
      for channel in ctx.guild.text_channels:
      # for channel in ctx.guild.get_all_channels():
        if int(channel.id) in channels_to_exclude:
          continue
        time.sleep(.2)
        try:
          # List all the messages sent in the channel today
          messages = channel.history(after=start_of_day)
          async for message in messages:
            time.sleep(.2)
            if not message.author.bot:
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
        except Exception as e:
          print(f"Couldn't fetch history from {channel.name}, {e}")

      message_count = count_messages(messages = message_dict, how_many = 15)
      await ctx.author.send(
          f'## Here is lis of messages today to the server:{ctx.guild.name}`\n {str(message_dict)[:1900]}`',
          silent=True)
      print(message_count)
      msg_embed = create_stylish_leaderboard_embed(message_count, question_expired=False, is_most_active_leaderboard=True)

      await ctx.send(embed=msg_embed, silent=True)
    
async def setup(bot):
  await bot.add_cog(Stats(bot))
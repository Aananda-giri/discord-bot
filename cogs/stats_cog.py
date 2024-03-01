import datetime
from discord.ext import commands
from .quiz_functions import get_question_embed, create_stylish_leaderboard_embed


from datetime import datetime, timedelta
import time, json
import discord


def count_percentage(message_count):
    '''
    Returns the percentage of messages by each user in a list.
    '''
    total_messages = sum(count for username, count in message_count)
    percentage_list = [(username, (count / total_messages) * 100) for username, count in message_count]
    return percentage_list

# Example Usage
# message_count = [('anon3', 3), ('anon2', 2), ('anon', 1)]
# result = count_percentage(message_count)
# print(result)


# # Example Usage
# message_count = [('anon3', 3), ('anon2', 2), ('anon', 1)]
# result = count_percentage(message_count)
# print(result)

def count_messages(messages, how_many=None):
    print('counting messages')
    message_count = {}
    reaction_count = {}
    for channel in messages:
        for message in messages[channel]:
            # Count Message
            if message['author'] in message_count:
                message_count[message['author']] += 1
            else:
                message_count[message['author']] = 1
            # try:
              # # Count Reaction
              # print(f'reactions:{reactions}')
              # for reaction in message['reactions']:
              #     print(f'reaction:{reaction}')
              #     print(f'user:{reaction["user"]} {type(reaction["user"])}')
              #     if reaction['user'] in reaction_count:
              #         reaction_count[reaction['user']] += 1
              #     else:
              #         reaction_count[reaction['user']] = 1
            # except Exception as Ex:
            #   print(f'error: {Ex}')

    message_count = sorted(message_count.items(), key=lambda x: x[1], reverse=True)
    return message_count[:how_many], count_percentage(message_count[:how_many])


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
      start_of_day = datetime(today.year, today.month, today.day)
      start_of_week = today - timedelta(days=today.weekday()+1)

      message_dict = {}
      reaction_dict = {}
      # Iterate over all text channels in the server
      print(f'ctx.guild')
      for channel in ctx.guild.text_channels:
      # for channel in ctx.guild.get_all_channels():
        if int(channel.id) in channels_to_exclude:
          continue
        time.sleep(.2)
        try:
          # List all the messages sent in the channel today
          messages = channel.history(after=start_of_day)
          print(f'messages:{messages}')
          async for message in messages:
            time.sleep(.2)
            if not message.author.bot:
              print(f'channel:{channel.name} \n\n message:{message}\n\nfucking reactions: {message.reactions}')
            #   print(f'author:{message.reactions[0].author} \n\n ')
              for reaction in  message.reactions:
                async for user in reaction.users():
                    if str(user) not in reaction_dict:
                        reaction_dict[str(user)] = 1
                    else:
                        reaction_dict[str(user)] += 1

              # Dont display messages by bot
              if message.channel.name not in message_dict:
                message_dict[message.channel.name] = []
              # Append reactions to reaction_dict
              
              message_dict[message.channel.name].append(
                  {
                      'author': str(message.author.name),
                      'content': str(message.content)
                  }
              )  # 'created_at': message.created_at, 'channel_id': message.channel.id})
              print(
                  f'{message.author.name} : {message.content} : {message.created_at}'
              )
        except Exception as e:
          print(f"Couldn't fetch history from {channel.name}, {e}")

      message_count, message_percentage  = count_messages(messages = message_dict, how_many = -1)
      reactions_count = sorted(reaction_dict.items(), key=lambda x: x[1], reverse=True)
      # Save as json file
      
      with open("messsage_reaction_count.json",'w') as f:
        json.dump({"message_count": message_count, 'reactions_count':reactions_count},f)
      # Send the file to user
      await ctx.author.send(file=discord.File("messsage_reaction_count.json"))
      #   await ctx.author.send(
      #       f'## Here is lis of messages today to the server:{ctx.guild.name}`\n {str(message_dict)[:1900]}`',
      #       silent=True)
      # print(message_count)
      msg_embed = create_stylish_leaderboard_embed(message_percentage, question_expired=False, is_most_active_leaderboard=True)

      await ctx.send(embed=msg_embed, silent=True)

    
async def setup(bot):
  await bot.add_cog(Stats(bot))

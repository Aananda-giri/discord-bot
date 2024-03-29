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

from .quiz_functions import create_stylish_leaderboard_embed
from discord.ext import commands
from datetime import datetime
import time


class ListMessages(commands.Cog, name="list_messages"):

  def __init__(self, bot):
    self.bot = bot

  @commands.hybrid_command(name="list",
                           brief="list all messages sent today in channel",
                           help='list: e.g. .l or .list',
                           aliases=[],
                           ephermal=True,
                           hidden=True,
                           usage='.l')
  async def l(self, ctx):

    # list all the messages sent in the channel today
    today = datetime.now()
    start_of_day = datetime(today.year, today.month, today.day)

    # List all the messages sent in the channel today
    messages = ctx.channel.history(after=start_of_day)

    # messages = ctx.channel.history(limit=100)#.flatten()
    print(messages)
    message_dict = {}
    async for message in messages:
      if message.channel.name not in message_dict:
        message_dict[message.channel.name] = []
      message_dict[message.channel.name].append(
          {
              'author': message.author.name,
              'content': message.content
          }
      )  # 'created_at': message.created_at, 'channel_id': message.channel.id})
      print(
          f'{message.author.name} : {message.content} : {message.created_at}')

    await ctx.author.send(
        f'## Here is lis of messages today to the channel:{ctx.channel.name}\n`{str(message_dict)[:1900]}`',
        silent=True)
    await ctx.message.delete()  # delete original message
    # await ctx.channel.send(f'`{str(message_dict)[:1900]}`', silent=True)

  @commands.command(
      name='list_all',
      aliases=[],
      brief='list all messages sent in a server today',
      help=
      'list all messages sent in a server today. \n e.g. `.la or .list_all :  sends list of messages to private message` '
  )
  async def la(self, ctx):
    # Get the start of the current day
    channels_to_exclude = [
        1132857202911215759, 1132858472212467712, 1132858133413371915,
        1132858904582311946, 1154660261106552832
    ]
    today = datetime.now()
    start_of_day = datetime(today.year, today.month, today.day)

    message_dict = {}
    # Iterate over all text channels in the server
    for channel in ctx.guild.text_channels:
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

    await ctx.author.send(
        f'## Here is lis of messages today to the server:{ctx.guild.name}`\n {str(message_dict)[:1900]}`',
        silent=True)
    await ctx.message.delete()  # delete original message
    # await ctx.channel.send(f'`{str(message_dict)[:1900]}`', silent=True)
  

  @commands.command(
      name='dataset',
      aliases=[],
      brief='get dataset of all messages sent in servers to train bot to predict reaction to messages',
      help=
      'list all messages sent in a server today. \n e.g. `.la or .list_all :  sends list of messages to private message` '
  )
  async def dataset(self, ctx):
    for guild in bot.guilds:
        
        print(f'server: {guild.id}')
        
        if saved_already(guild.id):
            print(f'data already saved for server: {guild.id}')
            continue
        # Get the start of the current day
        channels_to_exclude = []
        count = 0
        # today = datetime.now()
        # start_of_day = datetime(today.year, today.month, today.day)
        message_dict = {}
        # Iterate over all text channels in the server
        # for channel in ctx.guild.text_channels:
        for channel in guild.text_channels:
          # if int(channel.id) in channels_to_exclude:
          #   continue
          await asyncio.sleep(.5)
          try:
                # List all the messages sent in the channel today
                messages = channel.history(after=None)
                async for message in messages:
                  await asyncio.sleep(.2)
                  if not message.author.bot:
                        if message.reactions:
                            data = {
                                            'server_id': guild.id,
                                            'server_name': guild.name,
                                            "channel_id": message.channel.id,
                                            'author': message.author.name,
                                            'content': message.content,
                                            "reactions": [str(reaction.emoji) for reaction in message.reactions],
                                            # "created_at": message.created_at
                                    }
                            if message.channel.name not in message_dict:
                                message_dict[message.channel.name] = []
                            message_dict[message.channel.name].append(data)  # 'created_at': message.created_at, 'channel_id': message.channel.id})
                        # if message.reactions:
                        #         print(data)
                        
                        if count  < 20:
                            if message.reactions:
                                print(data)
                                count += 1
                        #   break
                        # print(
                        #         f'{message.author.name} : {message.content} : {message.reactions}, {channel.name}'
                        # )
          except Exception as e:
                print(f"Couldn't fetch history from {channel.name}, {e}")
        # save data in json file
        import json
        with open('data_'+ str(guild.id) + '.json', 'w') as outfile:
                json.dump(message_dict, outfile)
        try:
            await ctx.author.send('saved dataset to json files starting with `data_`')
        except:
            pass
        # await ctx.author.send(
        #         f'## Here is lis of messages today to the server:{ctx.guild.name}`\n {str(message_dict)[:1900]}`',
        #         silent=True)
        # await ctx.message.delete()  # delete original message
        # await ctx.channel.send(f'`{str(message_dict)[:1900]}`', silent=True)
    await ctx.author.send('done saving all data')


  @commands.command(name='channels', aliases=[])
  async def channels(self, ctx):
    # get name and id if all channels in a server

    channels_data = []
    for channel in ctx.guild.channels:
      # await ctx.send(f'Channel Name: {channel.name}, Channel ID: {channel.id}')
      print(f'Channel Name: {channel.name}, Channel ID: {channel.id}')
      channels_data.append({'channel_name':channel.name, 'channel_id': channel.id})
    await ctx.author.send(channels_data)

    await ctx.channel.send(msg_embed, silent=True)
async def setup(bot):
  await bot.add_cog(ListMessages(bot))

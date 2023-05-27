import os, sys, discord, platform, random, aiohttp, json, datetime, requests
from discord.ext import commands
from multiprocessing import context

if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config

async def hybrid(ctx):
        await ctx.send("This is a hybrid command!")

class general(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info", aliases=["botinfo"])
    async def info(self, context):
        embed = discord.Embed(
            #description="Created by Persian | EsfahanArmy",
            description="Created by Saneora | Nathan",
            color=0xFF3371
        )
        embed.set_author(
            name="Bot Information"
        )
        embed.add_field(
            name="Owner:",
            #value="Persian#5273",
            value="Nathan.#9449",
            inline=True
        )
        embed.add_field(
            name="Python Version:",
            value=f"{platform.python_version()}",
            inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"{config.BOT_PREFIX}",
            inline=False
        )
        embed.set_footer(
            text=f"Requested by {context.message.author}"
        )
        await context.send(embed=embed)

    @commands.command(name="serverinfo")
    async def serverinfo(self, context):
        server = context.message.guild
        roles = [x.name for x in server.roles]
        role_length = len(roles)
        if role_length > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)
        channels = len(server.channels)
        time = str(server.created_at)
        time = time.split(" ")
        time = time[0]

        embed = discord.Embed(
            title="**Server Name:**",
            description=f"{server}",
            color=0x33C4FF
        )
        embed.set_thumbnail(
            url=server.icon_url
        )
        embed.add_field(
            name="Owner",
            value=f"{server.owner}\n{server.owner.id}"
        )
        embed.add_field(
            name="Server ID",
            value=server.id
        )
        embed.add_field(
            name="Member Count",
            value=server.member_count
        )
        embed.add_field(
            name="Text/Voice Channels",
            value=f"{channels}"
        )
        embed.add_field(
            name=f"Roles ({role_length})",
            value=roles
        )
        embed.set_footer(
            text=f"Created at: {time}"
        )
        await context.send(embed=embed)


    @commands.command(name="ping", brief=" short_help: to test if bot responding  ",
             help='long_help: e.g. .ping', aliases=[])
    async def ping(self, context):
        print('\n Invoked ping \n')
        embed = discord.Embed(
            color=0x00FF00
        )
        embed.add_field(
            name="Pong!",
            value=":ping_pong:",
            inline=True
        )
        embed.set_footer(
            text=f"Pong request by {context.message.author}"
        )
        await context.send(embed=embed)

    @commands.command(name='invite',aliases=['share'], brief='`.invite` to get bot invite link',
             help='Plesae enter `.invite` or `.share` to invite me in another servers')
    async def invite(self, ctx, args=None):
        #await ctx.send("! I gave you a PM, go and see !")
        # To send invite link to author
        await ctx.author.send(f"Click on the link to add me to the server: https://discord.com/oauth2/authorize?client_id={config.APPLICATION_ID}&permissions=2148002880&scope=bot")
    
        embed=discord.Embed(title='Invitation link',
            #description=stream['longDesc'],
            color=0x00FFFF,
            url='https://discord.com/api/oauth2/authorize?client_id=862191340355715093&permissions=2148002880&scope=bot')
    
        embed.set_author(name=ctx.message.author)
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        embed.add_field(name="`Please vote for me`",
                        value="\thttps://top.gg/bot/862191340355715093/vote",
                        inline=False,
                        #url='https://top.gg/bot/862191340355715093/vote'
                        )
        embed.set_footer(text=f'{ctx.author} Please vote for me:https://top.gg/bot/862191340355715093/vote')
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
        
    
    
    @commands.command(name="server")
    async def server(self, context):
        await context.send("! I gave you a PM, go and see !")
        await context.author.send("Join our server: https://discord.gg/n4YPW6jeS7")
        #await context.send("! بهت یک پی ام دادم برو ببین !")
        #await context.author.send("به سرور ما بپیوندید: https://discord.gg/n4YPW6jeS7")

    @commands.command(name="poll")
    async def poll(self, context, *args):
        poll_title = " ".join(args)
        embed = discord.Embed(
            title = "A new poll has been created!",
            #title="!یک نظر سنجی جدید ایجاد شد!",
            description=f"{poll_title}",
            color=0x00FF00
        )
        embed.set_footer(
            text=f"Poll created by: {context.message.author} • React to vote!"
        )
        embed_message = await context.send(embed=embed)
        await embed_message.add_reaction("👍")
        await embed_message.add_reaction("👎")
        await embed_message.add_reaction("🤷")

    @commands.command(name="8ball")
    async def eight_ball(self, context, *args):
        answers = ['It is certain.', 'It is decidedly so.', 'You may rely on it.', 'Without a doubt.',
                   'Yes - definitely.', 'As I see, yes.', 'Most likely.', 'Outlook good.', 'Yes.',
                   'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.',
                   'Cannot predict now.', 'Concentrate and ask again later.', 'Don\'t count on it.', 'My reply is no.',
                   'My sources say no.', 'Outlook not so good.', 'Very doubtful.']
        embed = discord.Embed(
            title="**My Answer:**",
            description=f"{answers[random.randint(0, len(answers))]}",
            color=0x00FF00
        )
        embed.set_footer(
            text=f"Question asked by: {context.message.author}"
        )
        await context.send(embed=embed)

    @commands.command(name="bitcoin")
    async def bitcoin(self, context):
        url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
        # Async HTTP request
        async with aiohttp.ClientSession() as session:
            raw_response = await session.get(url)
            response = await raw_response.text()
            response = json.loads(response)
            embed = discord.Embed(
                title=":information_source: Info",
                description=f"Bitcoin price is: ${response['bpi']['USD']['rate']}",
                color=0x00FF00
            )
            await context.send(embed=embed)


    @commands.command(name="notifi")
    async def notifi(self, context, *args):
        notifi_title = " ".join(args)
        embed = discord.Embed(
            title="New announcement was made, please send it if confirmed!",
            #title="!اطلاعیه جدید ایجاد شد در صورت تایید ارسال فرمایید!",
            description=f"{notifi_title}",
            color=0x00FF00
        )
        embed.set_footer(
            text=f"Notification created by: {context.message.author} • vote to send!"
        )
        embed_message = await context.send(embed=embed)
        await embed_message.add_reaction("✔")
        await embed_message.add_reaction("❌")


        embed.add_field(
            name="Pong!",
            value=":ping_pong:",
            inline=True
        )
    
    
    
    
    @commands.command(name='movie',
             brief='To get movie url. e.g .movie harry potter',
             help='e.g .movie harry potter')
    async def movie(self, context, *args):
          movie_name = " ".join(args)
          print("movie: \"{}\"".format(movie_name))
          if movie_name == '':
            await context.send('please include the movie name like:  .movie harry potter')
          else:
            await context.send('movie_url: ')
            #search_term = message.split(' ',1)[1:]
            tmdb_url = 'https://api.themoviedb.org/3/search/movie?api_key={}&language=en-US&page=1&include_adult=true&query={}'.format(os.environ['TMDB_API_KEY'] ,movie_name)

            result = requests.get(tmdb_url).json()

            movie_url = "https://www.2embed.ru/embed/tmdb/movie?id={}".format(result['results'][0]['id'])
            await context.send(movie_url)
    

    @commands.HybridCommand(name="hybrid", func="hybrid")
    async def hybrid(ctx):
        await ctx.send("This is a hybrid command!")

    # @commands.hybrid_command(name="hybrid2")
    # async def hybrid(ctx):
    #     await ctx.send("This is a hybrid command!")

async def setup(bot):
    await bot.add_cog(general(bot))
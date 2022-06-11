import os, sys, discord
from discord.ext import commands
if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config

class Help(commands.Cog, name="help"):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name='help',
                 brief='`.help` for help',
                 help='Plesae enter `.help` for help', aliases=['h'])
    async def help(self, context, *args):
        args = ' '.join(args).strip()
        print('help invoked: ',args)
        if args=='':
           args=None
        command_names_list = [x.name for x in self.bot.commands]
        # Note that commands made only for the owner of the bot are not listed here.
        embed = discord.Embed(
            title="Encouragement Bot Help!",
            #Type `.help <command name>` for more details about each command. e.g. `.help joke`",
            description=
            "These are the commands you can use\nFor more detailed command explanations, \nType `.help <command_name>` e.g. `.help unleash`",
            
            
            
            #description="لیست دستورات بات :",
            color=0x00FF00
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/807598108812247090/809910607209824256/Save-Help-Me-Sticker-downsized.gif")
        #embed.set_footer(text=f"{context.message.author}, For more detailed command explanations type .help <command_name> !",icon_url=context.author.avatar_url)
        embed.set_author(
            name=context.message.author,
            #url="https://twitter.com/RealDrewData",
            icon_url=
            context.author.avatar_url
        )
        
        embed.add_field(
                name="List of supported commands:",
                value='value',
                #value="\n".join([str(i+1)+". "+x.name for i,x in enumerate(bot.commands)]),
                inline=False,
                #colour=discord.Color.blue()
            )
        
        if not args:
            print('\n argss is none')
            
            embed.add_field(
                name="Invite",
                value=f"Usage: {config.BOT_PREFIX[0]}invite",
                inline=False
            )
            
            embed.add_field(
                name="Server",
                value=f"Usage: {config.BOT_PREFIX[0]}server",
                inline=False
            )
            embed.add_field(
                name="Poll",
                value=f"Usage: {config.BOT_PREFIX[0]}poll <Idea>",
                inline=False
            )
            embed.add_field(
                name="Bitcoin",
                value=f"Usage: {config.BOT_PREFIX[0]}bitcoin",
                inline=False
            )
            embed.add_field(
                name="Info",
                value=f"Usage: {config.BOT_PREFIX[0]}info",
                inline=False
            )
            embed.add_field(
                name="avatar",
                value=f"Usage: {config.BOT_PREFIX[0]}avatar",
                inline=False
            )

            embed.add_field(
                name="Help",
                value=f"Usage: {config.BOT_PREFIX}help",
                inline=False
            )
            print('hill')
            # print('brief',list(context.bot.commands)[0].name, list(context.bot.commands)[0].brief, list(context.bot.commands)[0].help)
            
            for command in list(context.bot.commands):
                print(command.name)
                embed.add_field(
                    name='***{}***'.format(command.name),
                    value=f'\t *usage:* {str(command.help)} \n {str(command.brief)} \n\t ',
                    #value = f'*usage:* {str(context.bot.get_command(args).usage} \n\t {str(context.bot.get_command(args).brief}',
                    #value= '\t Usage: {}\n\t {}'.format(str(context.bot.get_command(args).help), str(context.bot.get_command(args).brief)),
                    inline=False,
                    #colour=discord.Color.blue()
                )
                continue
                #print(i.name)
                #print(i)
                #print(bot.get_command(i.name).help)
                '''for i,command in enumerate(bot.commands):
                
                help_embed.add_field(
                    name = command,
                    value = bot.get_command(command),
                    inline=True
                )'''
            embed.add_field(
                name="Details",
                value= '\t' +  "Type `.help <command name>` for more details about each command.",
                inline=False)
            
        # If the argument is a command, get the help text from that command:
        elif args in command_names_list:
            print('\n args in commands')
            
            embed.add_field(name=args,
                            value='\t *usage*: `{}` \n\t - {} \n\t - {})'.format(str(context.bot.get_command(args).usage), str(context.bot.get_command(args).brief), str(context.bot.get_command(args).help)),
                            inline=False)
    
        # If someone is just trolling:
        else:
            print('\n args not in commands')
            embed.add_field(name="Nope.",
                                 value="Don't think I got that command, boss!", inline=False)
        await context.channel.send(embed=embed)

class AnimeHelp(commands.Cog, name="anime_help"):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name='anime_help',
                 brief='`.help` for help',
                 help='Plesae enter `.help` for help', aliases=[])
    async def help(self, context, *args):
        args = ' '.join(args).strip()
        print('help invoked: ',args)
        if args=='':
           args=None
        command_names_list = [x.name for x in self.bot.commands]
        # Note that commands made only for the owner of the bot are not listed here.
        embed = discord.Embed(
            title="Anime Help!",
            #Type `.help <command name>` for more details about each command. e.g. `.help joke`",
            #description=
            #"These are the commands you can use\nFor more detailed command explanations, \nType `.help <command_name>` e.g. `.help unleash`",
            
            
            
            #description="لیست دستورات بات :",
            color=0x00FF00
        )
        #embed.set_image(url="https://cdn.discordapp.com/attachments/807598108812247090/809910607209824256/Save-Help-Me-Sticker-downsized.gif")
        #embed.set_footer(text=f"{context.message.author}, For more detailed command explanations type .help <command_name> !",icon_url=context.author.avatar_url)
        embed.set_author(
            name=context.message.author,
            #url="https://twitter.com/RealDrewData",
            icon_url=
            context.author.avatar_url
        )
        
        '''embed.add_field(
                name="Anime commands:",
                #value='value',
                #value="\n".join([str(i+1)+". "+x.name for i,x in enumerate(bot.commands)]),
                inline=False,
                #colour=discord.Color.blue()
            )'''
        
        if not args:
            print('\n args2 is none')
            embed.add_field(
                name="hello",
                value=f"Usage: `{config.BOT_PREFIX[1]}hello` \n\t e.g: `.hello`",
                inline=False
            )
            
            embed.add_field(
                name="ratewaifu",
                value=f"Usage: `{config.BOT_PREFIX[1]}ratewaifu <iifu_character>` \n\t e.g: `.ratewaifu nepgear`",
                inline=False
            )
            embed.add_field(
                name="https://i.imgur.com/nmnVtgs.jpg",
                value=f"Usage: `{config.BOT_PREFIX[1]}sauce <wifu_character_url>` \n\t e.g: .sauce https://i.imgur.com/nmnVtgs.jpg`",
                inline=False
            )
            embed.add_field(
                name="anime",
                value=f"Usage: `{config.BOT_PREFIX[1]}anime <anime_character>`\n\t e.g: `.anime kuro`",
                inline=False
            )
            embed.add_field(
                name="image",
                value=f"Usage: `{config.BOT_PREFIX[1]}image <anime_character>` \n\t e.g: `.image naruto`",
                inline=False
            )
            embed.add_field(
                name="aninews",
                value=f"Usage: `{config.BOT_PREFIX[1]}aninews <no_of_news_articles>` \n\t e.g: `.aninews 3`",
                inline=False
            )
        if args==None or args.lower()=='anime':
          await context.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
    bot.add_cog(AnimeHelp(bot))

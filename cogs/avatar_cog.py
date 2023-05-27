import discord
from discord.ext import commands

class avatar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.hybrid_command(name='avatar',
                 brief='To see avatar of specific member in the group',
                 help='e.g. `.avatar @Encouragement Bot`')
    #async def avatar(self, context, *, member: discord.Member = None):
    async def avatar(self, context, member : discord.Member = None):

        if member is None:
            #embed = discord.Embed(title="از این دستور اینطور استفاده کن: ```+avatar [member]```", colour=0xff0000, timestamp=context.message.created_at)
            embed = discord.Embed(title="Use this command like this: ```+avatar [member]```", colour=0xff0000, timestamp=context.message.created_at)
            
            await context.send(embed=embed)
            return

        else:
            embed2 = discord.Embed(title=f"Avatar {member} !", colour=0x0000ff)
            embed2.add_field(name="Animated avatar?", value=member.avatar.is_animated())
            #embed2 = discord.Embed(title=f"آواتار {member} !", colour=0x0000ff)
            #embed2.add_field(name="آواتار متحرک ؟", value=member.is_avatar_animated())
            embed2.set_image(url=member.avatar)
            embed2.set_footer(text=f"Avatar requested by: {context.message.author} !")
            await context.send(embed=embed2)

    


async def setup(bot):
    await bot.add_cog(avatar(bot))

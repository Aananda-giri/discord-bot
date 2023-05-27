import discord
from discord.ext import commands

class moderation(commands.Cog, name="moderation"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='kick', pass_context=True)
    async def kick(self, context, member: discord.Member, *args):
        if context.message.author.guild_permissions.kick_members:
            if member.guild_permissions.administrator:
                embed = discord.Embed(
                    title="Error!",
                    description="User has Admin permissions.",
                    color=0x00FF00
                )
                await context.send(embed=embed)
            else:
                try:
                    reason = " ".join(args)
                    embed = discord.Embed(
                        title="User Kicked!",
                        description=f"**{member}** was kicked by **{context.message.author}**!",
                        color=0x00FF00
                    )
                    embed.add_field(
                        name="Reason:",
                        value=reason
                    )
                    await context.send(embed=embed)
                    try:
                        await member.send(
                            f"You were kicked by **{context.message.author}**!\nReason: {reason}"
                        )
                    except:
                        pass
                except:
                    embed = discord.Embed(
                        title="Error!",
                        description="An error occurred while trying to kick the user.",
                        color=0x00FF00
                    )
                    await context.message.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0x00FF00
            )
            await context.send(embed=embed)

    @commands.hybrid_command(name="nick")
    async def nick(self, context, member: discord.Member, *, name: str):
        if context.message.author.guild_permissions.administrator:
            try:
                if name.lower() == "!reset":
                    name = None
                embed = discord.Embed(
                    title="Changed Nickname!",
                    description=f"**{member}'s** new nickname is **{name}**!",
                    color=0x00FF00
                )
                await context.send(embed=embed)
                await member.edit(nick=name)
            except Exception as err:
                print(err)
                error_message = str(err).split(':')[-1]
                embed = discord.Embed(
                    title="Error!",
                    description= "An error occurred : {}".format(error_message),
                    color=0x00FF00
                )
                await context.message.channel.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0x00FF00
            )
            await context.send(embed=embed)

    @commands.hybrid_command(name="ban")
    async def ban(self, context, member: discord.Member, *args):
        if context.message.author.guild_permissions.administrator:
            try:
                if member.guild_permissions.administrator:
                    embed = discord.Embed(
                        title="Error!",
                        description="User has Admin permissions.",
                        color=0x00FF00
                    )
                    await context.send(embed=embed)
                else:
                    reason = " ".join(args)
                    embed = discord.Embed(
                        title="User Banned!",
                        description=f"**{member}** was banned by **{context.message.author}**!",
                        color=0x00FF00
                    )
                    embed.add_field(
                        name="Reason:",
                        value=reason
                    )
                    await context.send(embed=embed)
                    await member.send(f"You were banned by **{context.message.author}**!\nReason: {reason}")
                    await member.ban(reason=reason)
            except Exception as err:
                print(err)
                error_message = str(err).split(':')[-1]
                embed = discord.Embed(
                    title="Error!",
                    description="An error occurred : {}".format(error_message),
                    color=0x00FF00
                )
                await context.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0x00FF00
            )
            await context.send(embed=embed)

    @commands.hybrid_command(name="warn")
    async def warn(self, context, member: discord.Member, *args):
        if context.message.author.guild_permissions.administrator:
            reason = " ".join(args)
            embed = discord.Embed(
                title="User Warned!",
                description=f"**{member}** was warned by **{context.message.author}**!",
                color=0x00FF00
            )
            embed.add_field(
                name="Reason:",
                value=reason
            )
            await context.send(embed=embed)
            try:
                await member.send(f"You were warned by **{context.message.author}**!\nReason: {reason}")
            except:
                pass
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0x00FF00
            )
            await context.send(embed=embed)

    @commands.hybrid_command(name="purge")
    async def purge(self, context, number):
        if context.message.author.guild_permissions.administrator:
            purged_messages = await context.message.channel.purge(limit=number)
            embed = discord.Embed(
                title="Chat Cleared!",
                description=f"**{context.message.author}** cleared **{len(purged_messages)}** messages!",
                color=0x00FF00
            )
            await context.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0x00FF00
            )
            await context.send(embed=embed)

def setup(bot):
    bot.add_cog(moderation(bot))
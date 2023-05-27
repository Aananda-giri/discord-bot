# discord.py hybrid commands
import interactions
import config
bot = interactions.Client(token=config.DISCORD_TEST_BOT_TOKEN, application_id=config.DISCORD_TEST_BOT_ID)

@bot.command(
# @interactions.slash_command(  # v5
    name="my_first_command",
    description="This is the first command I made!",
)
# async def my_first_command(ctx: interactions.SlashContext):   # v5
async def my_first_command(ctx: interactions.CommandContext):
    await ctx.send("Hi there!")

bot.start()
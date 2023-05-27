# discord.py hybrid commands
import interactions
import config
bot = interactions.Client(token=config.TEST_BOT_TOKEN, application_id=config.TEST_BOT_ID)

# @bot.command(
@interactions.slash_command(
    name="my_first_command",
    description="This is the first command I made!",
)
async def my_first_command(ctx: interactions.SlashContext):
    await ctx.send("Hi there!")

bot.start()
# bot.run("ODY0NDA2NTQ3MTA2MjM0Mzc4.GuvmJe.RHrGHqEuGrAVeR1Ub7kdnYXiFiHoKflNxCQYsg")
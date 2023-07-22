import os
import discord
import tafe_timetable
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


def on_start():
    TOKEN = '[YOUR TOKEN HERE]'
    #TEST_TOKEN = '[my other test bot]'

    @bot.event
    async def on_ready():
        await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="!timetable"))
        print(f'{bot.user} is now running!')


    @bot.command()
    async def timetable(ctx): # Change to 'timetable' when on main build. # tt is for testing purposes.
        try:
            message = await ctx.send("Fetching timetable...")
            tafe_timetable.timetable_lookup()

            file = discord.File("timetable.png", filename="timetable.png")
            await ctx.send(file=file)

            png = "timetable.png"
            os.remove(png)

            await message.edit(content="Most recent timetable:")
        except Exception as e:
            print(e)
            await ctx.send(">>> **Error fetching timetable.**\nWebsite is down or overloaded.\nPlease try again later!\nIf this issue persists, please contact the developer")
            await message.delete()
    bot.run(TOKEN)

if __name__ == '__main__':
    on_start()
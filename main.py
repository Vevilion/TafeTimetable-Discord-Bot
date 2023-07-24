import os
import discord
import asyncio
import tafe_timetable
from datetime import date, datetime, timedelta
from image_recognition import compare_images
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
loop = False
def on_start():
    TOKEN = '[YOUR TOKEN HERE]'
    #TEST_TOKEN = '[my other test bot]'

    @bot.event
    async def on_ready():
        await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="!timetable"))
        print(f'{bot.user} is now running!')


    @bot.command()
    async def timetable(ctx): # Change to 'timetable' when on main build. # 'tt' is for testing purposes.
        try:
            message = await ctx.send("Fetching timetable...")
            tafe_timetable.timetable_lookup()

            file = discord.File("new_timetable.png", filename="new_timetable.png")
            await ctx.send(file=file)

            try:
                os.remove('manual_timetable.png')
            except Exception as e:
                print(e)
            os.rename('new_timetable.png', 'manual_timetable.png')
            # This will fail if update function runs at the same time when timetable is deleted.

            await message.edit(content="Most recent timetable:")
        except Exception as e:
            print(e)
            await ctx.send(">>> **Error fetching timetable.**\nWebsite is down or overloaded.\nPlease try again later!\nIf this issue persists, please contact the developer")
            await message.delete()
    
    
    async def update_timetable(ctx):
        now = date.today()
        try:
            tafe_timetable.timetable_lookup()
            os.rename('new_timetable.png', 'compare_timetable.png')
            if compare_images() == 'None':
                msg = await ctx.send(f">>> Timetable has not been updated on **{now.strftime('%d/%m/%Y')}** at **{datetime.now().strftime('%H:%M:%S')}**")
                os.remove('compare_timetable.png')
                #await msg.delete(delay=10)
            else:   
                await ctx.send(f">>> @everyone Latest timetable update: **{now.strftime('%d/%m/%Y')}** at **{datetime.now().strftime('%H:%M:%S')}**")
                file = discord.File("compare_timetable.png", filename="compare_timetable.png")
                await ctx.send(file=file)

                os.remove('timetable.png')
                os.rename('compare_timetable.png', 'timetable.png')
        except Exception as e:
            print(e)
            await ctx.send("Error")     


    async def daily_update(ctx):
            try: 
                await update_timetable(ctx)
                now = datetime.now()
                next_update = now.replace(hour=1, minute=22, second=0, microsecond=0)
                if now > next_update:
                    next_update += timedelta(minutes=1)
                delta = next_update - now
                if delta.total_seconds() < 0:
                    delta = abs(delta)
                msg = await ctx.send(f">>> Will try again on: **{next_update.strftime('%d/%m/%Y')}** at **{next_update.strftime('%H:%M:%S')}**")
                #print(int(delta.total_seconds()))
                await asyncio.sleep(delta.total_seconds())
                #await msg.delete(delay=10)  
            except Exception as e:
                print(e)
                await ctx.send(">>> **Something went wrong, please restart the command.**")
            pass
    
    async def start_loop(ctx):
        global loop
    
        if loop:
            await ctx.send(">>> **Auto update is already on.**")
            pass
        else:
            loop = True
            await ctx.send(">>> **Auto update turned on.**")
            while loop:
                await daily_update(ctx)
    
    async def stop_loop(ctx):
        global loop
    
        if not loop:
            await ctx.send(">>> **Auto update is already off.**")
        else:
            loop = False
            await ctx.send(">>> **Auto update turned off.**")

    @bot.command()
    async def auto_update(ctx, arg=None):
        print(arg)
        if arg == 'on':
            await start_loop(ctx)
        elif arg == 'off':
            await stop_loop(ctx)
        else:
            await ctx.send(">>> **Invalid argument.**\nPlease use: `!auto_update on/off`")

    @bot.command()
    async def commands(ctx):
        await ctx.send(">>> **Commands:**\n`!timetable` - Fetches the latest timetable\n`!auto_update on/off` - Turns on/off auto daily timetable updates. Default set to 7am\n`!commands` - Displays this message")

    bot.run(TOKEN)

if __name__ == '__main__':
    on_start()
import discord
from discord.ext import commands, tasks
import aiohttp
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=";!", intents=intents)

# You can costumize your prefix by changing the ";!" to any prefix you want

TOKEN = 'token in here'
checking_task = None
running = False

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

async def check_usernames(ctx):
    global running
    async with aiohttp.ClientSession() as session:
        while running:
            username = generate_username()
            async with session.get(f'https://discord.com/api/v9/users/{username}') as resp:
                if resp.status == 404:
                    await ctx.send(f'The username `{username}` is available!')
            await asyncio.sleep(1)

def generate_username():
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

@bot.command()
async def usernames(ctx):
    global checking_task, running
    if checking_task is None or checking_task.done():
        running = True
        checking_task = bot.loop.create_task(check_usernames(ctx))
        await ctx.send("Started checking usernames.")

@bot.command()
async def stop(ctx):
    global checking_task, running
    if checking_task and not checking_task.done():
        running = False
        checking_task.cancel()
        await ctx.send("Stopped checking usernames.")

bot.run(TOKEN)

from discord.ext import commands
import discord
import os

intents=discord.Intents.all()

client = commands.Bot(command_prefix="!",intents=intents)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run("ODYyMTE0MDUyODc5ODEwNjIy.YOToRw.wa5wwKsbNdMdGKNc_5YhVu3Mmtc")
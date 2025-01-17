import discord
from discord.ext import commands
import os
import requests
from .keyHole import GUILD_ID
from .intents import intent, botstuff

# Set up bot with command prefix and intents (using discord.Bot)
intents = intent
intents.messages = True

# Initialize the bot using discord.Bot (for slash commands)
bot = botstuff

guild_id = GUILD_ID
async def on_Ready():
    try:
        print(f'Logged in as {bot.user}')  
        
        # Iterate through all guilds the bot is connected to
        for guild in bot.guilds:
            print(f'{bot.user} is connected to {guild.name} (ID: {guild.id})')
    except Exception as e:
        print(f'unable to log {bot.user} into {guild.name}')
    try:
        await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f'Logged in as {bot.user}')
        print(f'registered commands: {bot.tree.command} to {guild.name}')
    except Exception as e:
        print(f'unable to register {bot.tree.command} commands to {guild.name}')

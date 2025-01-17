import discord
from discord import app_commands
from discord.ext import commands
import requests
import logging
from events import (
    checkEnvVar, 
    DISCORD_BOT_TOKEN,
    GUILD_ID,
    R6API, 
    botstuff,
    intent,
    on_Ready
)

# Confirm .env variables are correct and loading properly
checkEnvVar()

# Init bot intents
intents = intent
intents.message_content = True
bot = botstuff


# Bot event for on_ready
@bot.event
async def on_ready():
    await on_Ready()

# Slash command definition
@bot.tree.command(guild=discord.Object(id=GUILD_ID), name="r6stats", description="Fetch Rainbow Six Siege stats for a player")
@app_commands.describe(username="Enter the player's name", platform="Enter the platform a platform")
async def r6stats(interaction: discord.Interaction, username: str, platform: str):

    await interaction.response.defer()


    
    if platform == 'PC' or 'pc': #platform.lower():
        platform = 'ubi'
    elif platform == 'Xbox' or 'xbox': #platform.lower():
        platform = 'xbl'
    elif platform == 'PlayStation' or 'playstation': #platform.lower():
        platform = 'psn'
    else:
        await interaction.followup.send("Failed to find platform. Please try again later.")


   
            

    # Constructing the API URL
    api_url = f"https://r6.tracker.network/r6siege/profile/{platform}/{username}/overview"
    
    try:
        # Check if the URL is reachable by sending a simple request (no need to parse JSON if we just want the link)
        response = requests.get(api_url, timeout=15)
        response.raise_for_status()

        if response.status_code == 200:
            # Send the link to the player's stats directly in the message
            await interaction.followup.send(f"Here are the stats for {username} on {platform.capitalize()}: {api_url}")
        else:
            await interaction.followup.send("Failed to fetch stats. Please try again later.")
    
    except requests.exceptions.Timeout:
        await interaction.followup.send("The request timed out. Please try again later.")
    except requests.exceptions.HTTPError as e:
        await interaction.followup.send(f"HTTP error occurred: {str(e)}. Please try again later.")
    except requests.exceptions.RequestException as e:
        await interaction.followup.send(f"An error occurred: {str(e)}. Please try again later.")

# Run the bot

bot.run(DISCORD_BOT_TOKEN)

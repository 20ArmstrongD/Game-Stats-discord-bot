import discord
from discord import app_commands
import requests
import logging
from events import (
    checkEnvVar, 
    DISCORD_BOT_TOKEN,
    GUILD_ID,
    botstuff,
    intent,
    on_Ready,
    get_playerdata
)
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Confirm .env variables are correct and loading properly
checkEnvVar()

# Init bot intents
intents = intent
intents.message_content = True

bot = botstuff

# Define bot_run flag
bot_run = False

# Bot event for on_ready
@bot.event
async def on_ready():
    await on_Ready()

# Slash command definition
@bot.tree.command(guild=discord.Object(id=GUILD_ID), name="r6stats", description="Fetch Rainbow Six Siege stats for a player")
@app_commands.describe(username="Enter the player's name", platform="Enter the platform (PC, Xbox, PlayStation)", option="Url included ('yes', 'no') for just the link type 'link'")
async def r6stats(interaction: discord.Interaction, username: str, platform: str, option: str):

    global bot_run  # Access the bot_run flag
    user = interaction.user
    channel_location = interaction.channel
    await interaction.response.defer()
    start_time = time.time()

    try:
        platform = platform.lower()
        option = option.lower()
        
        if platform == 'pc':
            logging.info(f"{platform} element found")
            platform = 'ubi'
        elif platform == 'xbox':
            logging.info(f"{platform} element found")
            platform = 'xbl'
        elif platform == 'playstation':
            logging.info(f"{platform} element found")
            platform = 'psn'
        else:
            logging.error(f"Failed to find {platform} platform")
            await interaction.followup.send("Failed to find platform. Please try again later.")
            return  # Exit early if the platform is invalid
   
    except Exception as e:
        logging.error(f'Failed to convert to {platform}')
   
    # Constructing the API URL
    api_url = f'https://r6.tracker.network/r6siege/profile/{platform}/{username}/overview'
    
    try:
        # Check if the URL is reachable by sending a simple request (no need to parse JSON if we just want the link)
        response = requests.get(api_url, timeout=20)
        response.raise_for_status()

        if response.status_code == 200 and not bot_run:
            logging.info(f"Accepted, Proceeding with {user.display_name}'s request ")

            # Ensure get_playerdata runs only once
            # kd, level, playtime, rank, ranked_kd = get_playerdata(api_url)
            # bot_run = True  # Set the flag to True to prevent re-running the function

            # Send the link to the player's stats directly in the message
            if option == 'no':
                kd, level, playtime, rank, ranked_kd = get_playerdata(api_url)
                bot_run = True  # Set the flag to True to prevent re-running the function
                logging.info(f"Scrapping complete, replying to {user.display_name} in {channel_location} channel.")
                response_message = (
                    f"Here are the stats for {username} on {platform.capitalize()}:\n"
                    f" * Level: {level}\n"
                    f" * All playlist KD Ratio: {kd}\n"
                    f" * Total Play Time: {playtime}\n"
                    f" * Current Rank: {rank}\n"
                    f" * Ranked KD Ratio: {ranked_kd}")
                logging.info(f"Sending this message to {user} in {channel_location} channel: \n{response_message}")
                await interaction.followup.send(response_message)
                end_time = time.time()
                time_duration = end_time - start_time
                logging.info(f"time to completion: {time_duration:.2f} seconds on request")
                
            elif option == 'yes':
                kd, level, playtime, rank, ranked_kd = get_playerdata(api_url)
                bot_run = True  # Set the flag to True to prevent re-running the function
                logging.info(f"Scrapping complete, replying to {user.display_name} in {channel_location} channel.")
                response_message = (
                    f"Stats for {username} on {platform.capitalize()}:\n" 
                    f"Obtained from: {api_url}\n"
                    f"These stats were pulled:\n"
                    f" * Level: {level}\n"
                    f" * All playlist KD Ratio: {kd}\n"
                    f" * Total Play Time: {playtime}\n"
                    f" * Current Rank: {rank}\n"
                    f" * Ranked KD Ratio: {ranked_kd}")
                logging.info(f"Sending this message to {user} in {channel_location} channel: \n{response_message}")
                await interaction.followup.send(response_message)
                end_time = time.time()
                time_duration = end_time - start_time
                logging.info(f"time to completion: {time_duration:.2f} seconds on request")
            
            elif option == "link":
                bot_run = False
                logging.info(f"Link generated, replying to {user.display_name} in {channel_location} channel.")
                response_message = (f"Here is the link for {username}: {api_url}")
                logging.info(f"Sending this message to {user} in {channel_location} channel: \n{response_message}")
                await interaction.followup.send(response_message)
                end_time = time.time()
                time_duration = end_time - start_time
                logging.info(f"time to completion: {time_duration:.2f} seconds on request")
                
            else:
                await interaction.followup.send("Failed to fetch stats. Please try again later.")
                end_time = time.time()
                time_duration = end_time - start_time
                logging.info(f"time to failure: {time_duration:.2f} seconds on request")
        else:
            await interaction.followup.send("Failed to complete request")
            end_time = time.time()
            time_duration = end_time - start_time
            logging.info(f"time to failure: {time_duration:.2f} seconds on request")
        
    except requests.exceptions.Timeout:
        await interaction.followup.send("The request timed out. Please try again later.")
        end_time = time.time()
        time_duration = end_time - start_time
        logging.info(f"time to completion: {time_duration:.2f} seconds")
    except requests.exceptions.HTTPError as e:
        await interaction.followup.send(f"HTTP error occurred: {str(e)}. Please try again later.")
        end_time = time.time()
        time_duration = end_time - start_time
        logging.info(f"time to completion: {time_duration:.2f} seconds")
    except requests.exceptions.RequestException as e:
        await interaction.followup.send(f"An error occurred: {str(e)}. Please try again later.")
        end_time = time.time()
        time_duration = end_time - start_time
        logging.info(f"time to completion: {time_duration:.2f} seconds")

# Run the bot
bot.run(DISCORD_BOT_TOKEN)

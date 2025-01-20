import discord
from discord import app_commands
import aiohttp  
import logging
import time
import asyncio
from events import (
    checkEnvVar, 
    DISCORD_BOT_TOKEN,
    GUILD_ID,
    botstuff,
    intent,
    on_Ready,
    get_playerdata
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
@app_commands.describe(username="Enter the player's name", platform="Enter the platform (PC, Xbox, PlayStation)", link_option="For just the link type 'yes'")
async def r6stats(interaction: discord.Interaction, username: str, platform: str, link_option: str = None):

    user = interaction.user
    channel_location = interaction.channel
    await interaction.response.defer()
    start_time = time.time()

    try:
        platform = platform.lower()
        link_option = link_option.lower() if link_option else None
        
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

    api_url = f'https://r6.tracker.network/r6siege/profile/{platform}/{username}/overview'
    
    try:
        # Use aiohttp to make the request asynchronously
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, timeout=20) as response:
                if response.status == 200:
                    if link_option is None:

                        kd, level, playtime, rank, ranked_kd, ranked_img,= get_playerdata(api_url)
                        logging.info(f"Scraping complete, replying to {user.display_name} in {channel_location} channel.")
                        
                        # Create embed message for 'no' link option
                        embed = discord.Embed(title=f"Stats for {username} on {platform.capitalize()}\n", color=discord.Color.yellow())
                        embed.add_field(name="**Overall Stats**", value=f" * Level: {level}\n * All playlist KD Ratio: {kd}\n * Total Play Time: {playtime}", inline=False)
                        embed.add_field(name="**Ranked Stats**", value=f" * Current Rank: {rank}\n * Ranked KD: {ranked_kd}", inline=False)
                        embed.set_thumbnail(url=ranked_img)  
            
                        # Send embed message for 'yno' link option
                        logging.info(f"Sending this message to {user} in {channel_location} channel: \n{embed}")
                        await interaction.followup.send(embed=embed)

                        end_time = time.time()
                        time_duration = end_time - start_time
                        logging.info(f"time to completion: {time_duration:.2f} seconds on request")

                    
                    elif link_option is not None:
                        # api_url = f'https://r6.tracker.network/r6siege/profile/{platform}/{username}/overview'
                        logging.info(f"Link generated, replying to {user.display_name} in {channel_location} channel.")
                        
                        # Create embed message for 'Just link' option
                        embed = discord.Embed(title=f"Stats for {username} on {platform.capitalize()}\n", color=discord.Color.yellow())
                        embed.add_field(name=f"Can be found on this link:", value=f"{api_url}")

                        # Send embed message for'Just link' option
                        logging.info(f"Sending this message to {user} in {channel_location} channel: \n{embed}")
                        await interaction.followup.send(embed=embed)

                        end_time = time.time()
                        time_duration = end_time - start_time
                        logging.info(f"time to completion: {time_duration:.2f} seconds on request")

                    else:
                        await interaction.followup.send("Failed to fetch stats. Please try again later.")
                        end_time = time.time()
                        time_duration = end_time - start_time
                        logging.info(f"time to failure: {time_duration:.2f} seconds on request")

                else:
                    await interaction.followup.send("Failed to complete request.")
                    end_time = time.time()
                    time_duration = end_time - start_time
                    logging.info(f"time to failure: {time_duration:.2f} seconds on request")
        
    except asyncio.TimeoutError:
        await interaction.followup.send("The request timed out. Please try again later.")
        end_time = time.time()
        time_duration = end_time - start_time
        logging.info(f"time to failure: {time_duration:.2f} seconds on request")
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {str(e)}. Please try again later.")
        end_time = time.time()
        time_duration = end_time - start_time
        logging.info(f"time to failure: {time_duration:.2f} seconds on request")

# Run the bot
bot.run(DISCORD_BOT_TOKEN)

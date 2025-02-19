import discord
from discord import app_commands
import logging
import inspect
from events import (
    checkEnvVar, 
    DISCORD_BOT_TOKEN,
    GUILD_ID,
    botstuff,
    intent,
    on_Ready,
    get_r6siege_player_data,
    generate_link, 
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%I:%M:%S %p'  # 12-hour clock with AM/PM
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


# Dictionary to store usernames per game
usernames = {
    f"fortnite": ["Budg3taryChunk5"],
    f"siege": ["BigMcD0n"]
}

# Function to provide dynamic username suggestions
async def username_autocomplete(interaction: discord.Interaction, current: str):
    """Dynamically provides username suggestions based on input."""
    game_value = getattr(interaction.namespace, 'game', None)


    """Check if game value is none"""
    if game_value:
        """create list of choice objects based on the usernames and the game tied to that value"""
        choices = [
            app_commands.Choice(name=name, value=name) 
            for name in usernames.get(game_value, []) if current.lower() in name.lower()
        ]
        return choices # matching choice list
    return [] # return empty list if game value is not provided

# Slash command definition
@bot.tree.command(guild=discord.Object(id=GUILD_ID), name="game_stats", description="Fetch game stats for a player")
@app_commands.describe(username="Enter the player's name", game="Choose a game", platform="Enter the platform (PC, Xbox, PlayStation)")
@app_commands.choices(game=[
    app_commands.Choice(name="Fortnite", value="fortnite"),
    app_commands.Choice(name="Rainbow Six Siege", value="siege"),
])
@app_commands.autocomplete(username=username_autocomplete)
async def pull_stats(interaction: discord.Interaction, game: app_commands.Choice[str], username: str, platform: str = None):

    if not interaction.response.is_done():
        await interaction.response.defer()

    game = game.value.lower()

    # Add username to the list if not present
    if username not in usernames.get(game, []):
        usernames.setdefault(game, []).append(username)
        logging.info(f"New username '{username}' added to {game} list.")
    else:
        logging.info(f"{username} found in {game} list")

    if platform:
        platform = platform.lower()
        platform_map = {
            "pc": "ubi", 
            "xbox": "xbl", 
            "playstation": "psn"
            }
        
        platform = platform_map.get(platform, None)

        if not platform:
            logging.error(f"Invalid platform: {platform}")
            await interaction.followup.send("Failed to find platform. Please try again later.")
            return

    # Mapping of game scrapers
    game_scrapers = {
        "siege": {"func": get_r6siege_player_data, "requires_platform": True},
        "fortnite": {"func": generate_link, "requires_platform": False}
    }

    if game not in game_scrapers:
        await interaction.followup.send(f"{game} not supported. Please pick from these options:")
        return

    scraper_func = game_scrapers[game]["func"]
    requires_platform = game_scrapers[game]["requires_platform"]

    if requires_platform and not platform:
        await interaction.followup.send(f"{game.capitalize()} requires a platform (PC, Xbox, PlayStation).")
        return

    num_args = len(inspect.signature(scraper_func).parameters)

    if num_args == 2:
        logging.info(f"Fetching {game} stats for {username} on {platform}...")
        kd, level, playtime, rank, ranked_kd, user_profile_img, rank_img = await get_r6siege_player_data(username, platform)

        # Ensure values are not None
        kd = kd or "N/A"
        level = level or "N/A"
        playtime = playtime or "N/A"
        rank = rank or "N/A"
        ranked_kd = ranked_kd or "N/A"
        user_profile_img = user_profile_img or "N/A"
        rank_img = rank_img or "N/A"

        logging.info(f"Stats retrieved. Sending response to {interaction.user} in {interaction.channel}...")
        embed = discord.Embed(title=f"Stats for {username} on {game.capitalize()}", color=discord.Color.yellow())
        embed.add_field(name="**Overall Stats**", value=f" * Level: {level}\n * KD Ratio: {kd}\n * Play Time: {playtime}", inline=False)
        embed.add_field(name="**Ranked Stats**", value=f" * Rank: {rank}\n * Ranked KD: {ranked_kd}", inline=False)
        embed.set_thumbnail(url=user_profile_img)
        embed.set_image(url=rank_img)
        await interaction.followup.send(embed=embed)

    elif num_args == 1:
        url = await generate_link(username)

        if not url:
            await interaction.followup.send("Failed to generate the link.")
            return
        else:
            logging.info(f"Link generated")
            logging.info(f"Replying to {interaction.user} in {interaction.channel}")

        embed = discord.Embed(title=f"Fortnite Stats for {username}", color=discord.Color.purple())
        embed.add_field(name="Link", value=f"{url}", inline=False)
        await interaction.followup.send(embed=embed)

    else:
        await interaction.followup.send(f"Could not fetch stats for {username} in {game.capitalize()}.")
        

# Run the bot
bot.run(DISCORD_BOT_TOKEN)

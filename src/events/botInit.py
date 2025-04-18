import discord
from discord.ext import commands
import os
import requests
import json
from .intents import intent, botstuff

# Set up bot with command prefix and intents (using discord.Bot)
intents = intent
intents.messages = True
intents.guilds = True

# Initialize the bot using discord.Bot (for slash commands)
bot = botstuff

GUILD_LOG_PATH = "/home/DiscordPi/code/discord_bots/r6-discord-bot/src/Json/guilds.json"

@bot.event
async def on_guild_join(guild):
    print(f"🔔 on_guild_join triggered for: {guild.name} ({guild.id})")

    # Ensure file exists and is valid
    if not os.path.exists(GUILD_LOG_PATH) or os.path.getsize(GUILD_LOG_PATH) == 0:
        with open(GUILD_LOG_PATH, "w") as f:
            json.dump({"servers": []}, f)

    # Load existing data
    with open(GUILD_LOG_PATH, "r") as f:
        data = json.load(f)

    # Append new guild info if not already tracked
    if not any(str(g["id"]) == str(guild.id) for g in data["servers"]):
        data["servers"].append({
            "id": str(guild.id),
            "name": guild.name
        })

        with open(GUILD_LOG_PATH, "w") as f:
            json.dump(data, f, indent=4)

    print(f"✅ Joined new server: {guild.name} ({guild.id})")

@bot.event
async def on_Ready():
    try:
        print(f'✅ Logged in as {bot.user}')  
        
        for guild in bot.guilds:
            print(f'Connected to: {guild.name} (ID: {guild.id})')
    except Exception as e:
            print(f'❌ Failed to list connected guilds: {e}')

        # --- Ensure all current guilds are tracked in the JSON file ---
    try:
        # If file doesn't exist or is empty/corrupt, initialize it
        if not os.path.exists(GUILD_LOG_PATH) or os.path.getsize(GUILD_LOG_PATH) == 0:
            with open(GUILD_LOG_PATH, "w") as f:
                json.dump({"servers": []}, f)

        with open(GUILD_LOG_PATH, "r+") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"servers": []}

            existing_ids = {s["id"] for s in data["servers"]}
            updated = False

            for guild in bot.guilds:
                if str(guild.id) not in existing_ids:
                    data["servers"].append({
                        "id": str(guild.id),
                        "name": guild.name
                    })
                    updated = True
                    print(f"📌 Added missing server from startup: {guild.name} ({guild.id})")

            if updated:
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
    except Exception as e:
            print(f"❌ Failed to sync guilds.json with current guilds: {e}")

        # --- Sync slash commands ---
    try:
        synced_commands = await bot.tree.sync()
        command_names = [cmd.name for cmd in synced_commands]

        if len(command_names) <= 1:
            print(f"✅ Synced command: {', '.join(command_names)}")
        else:
            print(f"✅ Synced commands: {', '.join(command_names)}")
    except Exception as e:
            print(f"❌ Failed to sync commands: {e}")
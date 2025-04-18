#!/bin/bash
source /home/DiscordPi/code/discord_bots/r6-discord-bot/pivenv/bin/activate
echo "Starting script with xvfb-run..."
xvfb-run -a python /home/DiscordPi/code/discord_bots/r6-discord-bot/src/main.py
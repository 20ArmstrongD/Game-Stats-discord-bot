import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
R6API = os.getenv('R6_API_KEY')
GUILD_ID = os.getenv('GUILD_ID')


# print(DISCORD_BOT_TOKEN, R6API, GUILD_ID)
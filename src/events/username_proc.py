import json

file_path = "/home/DiscordPi/code/discord_bots/r6-discord-bot/src/Json/usernames.json"

def load_usernames():
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return{}

def save_usernames(usernames):
    with open(file_path, "w") as file:
        json.dump(usernames, file, indent=4)
        
        
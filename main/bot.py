import discord
intents = discord.Intents.all()
from discord.ext import commands
import json


TOKEN = open("token.txt", "r").readline()

client = commands.Bot(
    command_prefix = '!',
    intents = intents)

def ext_modules():
    with open('data/ext_modules.json') as f:
        modules = json.load(f)
        return modules



@client.event
async def on_ready():
    loaded_modules = []
    not_loaded_modules = []
    print(f"logged in as {client.user.name}")
    print("\n--------\nLoading modules")
    modules = ext_modules()
    for i in modules:
        try:
            client.load_extension('modules.'+i)
            loaded_modules.append(i)
        except Exception as error:
            print(f"Could not load module {i}")
            print(f"{i}{error}")
            not_loaded_modules.append(i)
    

    



client.run(TOKEN)
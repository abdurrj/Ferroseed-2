import discord
intents = discord.Intents.all()
from discord.ext import commands
import json

def get_prefix(client, message):
    with open(prefix_path, 'r', encoding='utf-8') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

def ext_modules_open():
    with open('main/data/ext_modules.json') as f:
        modules = json.load(f)
        return modules
def ext_modules_write(data):
    with open('main/data/ext_modules.json') as f:
        json.dump(data, f)

TOKEN = open("main/token.txt", "r").readline()
prefix_path = 'main/data/prefixes.json'
client = commands.Bot(
    command_prefix = (get_prefix),
    intents = intents)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        await client.process_commands(message)

@client.event
async def on_ready():
    loaded_modules = []
    not_loaded_modules = []
    print(f"logged in as {client.user.name}")
    print("\n--------\nLoading modules")
    modules = ext_modules_open()
    for i in modules:
        try:
            client.load_extension('modules.'+i)
            loaded_modules.append(i)
        except Exception as error:
            print(f"Could not load module {i}")
            print(f"{i} {error}")
            not_loaded_modules.append(i)
    
    print("Loaded modules: "+ ', '.join(i for i in loaded_modules))
    print("Modules not loaded: "+ ', '.join(i for i in not_loaded_modules))

@client.command()
@commands.is_owner()
async def extension(ctx, task:str=None, module:str=None):
    modules = ext_modules_open()
    if task == "names":
        print(', '.join(i for i in modules))
    elif task == "add":
        modules.append(module)
        ext_modules_write(modules)
    elif task == "remove":
        modules.pop(module)


    modules.append(module)



client.run(TOKEN)
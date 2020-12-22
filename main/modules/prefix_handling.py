from discord.ext import commands
from discord.ext.commands import Cog
import json

prefix_path = 'main/data/prefixes.json'
standard_prefix = "fb!"

def json_open(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data

def json_write(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


class prefix_handling(commands.Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener("on_message")
    async def reset_prefix(self, message):
        if message.author == self.client.user:
            return
        if message.guild == None:
            await message.author.send("Hi, I do not have any commands for use in DM")
            return

        if message.author.guild_permissions.administrator == True and message.content == "fb!reset":
            data = json_open(prefix_path)
            data[str(message.guild.id)] = standard_prefix
            json_write(prefix_path, data)
            await message.channel.send("Prefix has been reset to fb!. To change it, use fb!change_prefix")
        
    @Cog.listener("on_guild_join")
    async def new_guild_prefix(self, guild):
        data = json_open(prefix_path)
        data[str(guild.id)] = standard_prefix
        json_write(prefix_path, data)

    @Cog.listener("on_guild_remove")
    async def remove_guild_prefix(self, guild):
        data = json_open(prefix_path)
        data.pop(str(guild.id))
        json_write(prefix_path, data)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def change_prefix(self, ctx, prefix:str=standard_prefix):
        data = json_open(prefix_path)
        data[str(ctx.guild.id)] = prefix
        json_write(prefix_path, data)
        await ctx.send(f"Prefix changed to {prefix}")

def setup(client):
    client.add_cog(prefix_handling(client))
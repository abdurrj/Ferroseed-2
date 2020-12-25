from discord.ext import commands
from discord.ext.commands import Cog
import json, discord

settings = 'main/data/settings.json'
standard_prefix = "fb!"

def json_open(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data

def json_write(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


class server_settings(commands.Cog):
    def __init__(self, client):
        self.client = client

    #### Prefix settings
    @Cog.listener("on_message")
    async def reset_prefix(self, message):
        """Reset the server prefix, will work no matter what prefix is set"""
        if message.author == self.client.user:
            return
        if message.guild == None:
            await message.author.send("Hi, I do not have any commands for use in DM")
            return

        if message.author.guild_permissions.administrator == True and message.content == "fb!reset":
            data = json_open(settings)
            guild_dict = data[str(message.guild.id)]
            guild_dict["prefix"] = standard_prefix
            data[str(message.guild.id)] = guild_dict
            json_write(settings, data)
            await message.channel.send("Prefix has been reset to fb!. To change it, use fb!change_prefix")
        
    @Cog.listener("on_guild_join")
    async def new_guild_prefix(self, guild):
        """Create guild_dict when bot joins new server"""
        data = json_open(settings)
        data[str(guild.id)] = {
            "prefix":standard_prefix,
            "welcome_channel":None
        }
        json_write(settings, data)

    @Cog.listener("on_guild_remove")
    async def remove_guild_prefix(self, guild):
        """Remove guild_dict when bot leaves a server"""
        data = json_open(settings)
        data.pop(str(guild.id))
        json_write(settings, data)
    
    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def change_prefix(self, ctx, prefix:str=standard_prefix):
        """Customize prefix for the server"""
        data = json_open(settings)
        guild_dict = data[str(ctx.guild.id)]
        guild_dict["prefix"] = prefix
        data[str(ctx.guild.id)] = guild_dict
        json_write(settings, data)
        await ctx.send(f"Prefix changed to {prefix}")


    #### Member Welcome
    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def set_welcome(self, ctx, channel:discord.TextChannel):
        """Set welcome channel for the server"""
        data = json_open(settings)
        guild_dict = data[str(ctx.guild.id)]
        guild_dict["welcome_channel"] = str(channel.id)
        data[str(ctx.guild.id)] = guild_dict
        json_write(settings, data)
        await ctx.send(f"Welcome channel set to {channel}")

    @Cog.listener("on_member_join")
    async def member_welcome(self, member):
        """If welcome channel is set, welcome message will be sent there"""
        data = json_open(settings)
        guild_dict = data[str(member.guild.id)]
        if guild_dict["welcome_channel"]:
            welcome_channel = member.guild.get_channel(int(guild_dict["welcome_channel"]))
            embed = discord.Embed(colour=0x62eb96)
            embed.add_field(name='Someone new joined the server!', value=f"Please say welcome to {member.mention}")
            await welcome_channel.send(embed=embed)



def setup(client):
    client.add_cog(server_settings(client))
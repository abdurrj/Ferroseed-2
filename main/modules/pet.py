import discord, json
from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands.cooldowns import BucketType
from .server_settings import json_open, json_write

pet_count_path = 'main/data/pet_count.json'
settings = 'main/data/settings.json'


class pet(commands.Cog):
    def __init__(self, client):
        self.client = client


    @Cog.listener("on_guild_join")
    async def guild_add(self, guild):
        data = json_open(pet_count_path)
        data[str(guild.id)] = {
            "Total pet":0,
            "Total hurt":0,
            "Members":{}
        }
        json_write(pet_count_path, data)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def pet_random(self, ctx):
        embed = discord.Embed()
        embed.add_field(name="Would you like to always allow pets?", value="React with ✅ to always allow\nReact with ❌ to set to random")
        message = await ctx.send(embed=embed)

        emoji_list = ['✅','❌']
        data = json_open(settings)
        guild_settings = data[str(ctx.guild.id)]
        for i in emoji_list:
            await message.add_reaction(i)

        def checker(reaction, user):
            return user == ctx.author and str(reaction.emoji) in emoji_list

        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=15, check=checker)

                if str(reaction.emoji) == "✅":
                    guild_settings["pet_stat"] = "always"
                    await ctx.send("Pet settings changed to always allow pets")
                elif str(reaction.emoji) == "❌":
                    guild_settings["pet_stat"] = "random"
                    await ctx.send("Pet settings changed to randomize pets")

                data[str(ctx.guild.id)] = guild_settings
                json_write(settings, data)
                    
            except:
                await message.clear_reactions()
                await message.edit(content="You did not react in time, settings not changed")

    @commands.command()
    @commands.cooldown(1, 5, type=BucketType.user)
    



    
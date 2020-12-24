import discord, json, asyncio
import numpy as np
from discord.ext import commands
from discord.ext.commands import Cog, CommandOnCooldown
from discord.ext.commands.cooldowns import BucketType


pet_count_path = 'main/data/pet_count.json'
settings = 'main/data/settings.json'

def json_open(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data

def json_write(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

class petting(commands.Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener("on_guild_join")
    async def guild_add(self, guild):
        data = json_open(pet_count_path)
        data[str(guild.id)] = {
            "pet_stat":"random",
            "chance":0.8,
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
        data = json_open(pet_count_path)
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
                json_write(pet_count_path, data)
                await message.delete()
                    
            except asyncio.TimeoutError:
                break

    @commands.command(description="You can try petting Ferroseed, though Iron Barbs might kick in and hurt you")
    @commands.cooldown(1, 5, type=BucketType.user)
    async def pet(self, ctx):
        data = json_open(pet_count_path)
        guild_dict = data[str(ctx.guild.id)]
        random = guild_dict["pet_stat"]
        Member_dict = guild_dict["Members"]
        if str(ctx.author.id) in Member_dict.keys():
            member = Member_dict[str(ctx.author.id)]
        else:
            Member_dict[str(ctx.author.id)] = {"pet":0, "hurt":0}
            member = Member_dict[str(ctx.author.id)]
        
        if random == "random":
            choices = ['pet', 'no pet']
            pet_chance = float(guild_dict["chance"])
            hurt_chance = float(1 - pet_chance)
            selection = np.random.choice(choices, 1, p=[pet_chance, hurt_chance])
        elif random == "always":
            selection = 'pet'

        if selection[0] == 'pet':
            total_pet = guild_dict["Total pet"]
            total_pet += 1
            guild_dict["Total pet"] = total_pet
            pet_count = member["pet"]
            pet_count += 1
            member["pet"] = pet_count
            embed = discord.Embed(
            colour = discord.Colour.green())
            embed.add_field(name='Ferroseed anticipated this', value=f"{ctx.author.mention} pet Ferroseed! <:ferroHappy:734285644817367050> \n"
                                                                        "\nYou have pet me **"+str(pet_count)+"x** times!")

        elif selection[0] == 'no pet':
            total_hurt = guild_dict["Total hurt"]
            total_hurt += 1
            guild_dict["Total hurt"] = total_hurt
            pet_hurt = member["hurt"]
            pet_hurt += 1
            member["hurt"] = pet_hurt
            embed = discord.Embed(
            colour = discord.Colour.red())
            embed.set_author(name='Ouch!')
            embed.add_field(name='*Sorry!*', value=f"{ctx.author.mention} got hurt by Iron Barbs <:ferroSad:735707312420945940>\n"
                                                    "\nI've hurt you a total of **"+ str(pet_hurt) +"x** times.")

        Member_dict[str(ctx.author.id)] = member
        guild_dict["Members"] = Member_dict
        data[str(ctx.guild.id)] = guild_dict
        json_write(pet_count_path, data)
        await ctx.send(embed=embed)

    @pet.error
    async def pet_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            time = str(int(error.retry_after))
            await ctx.send(f"You can't pet me this often, you need to wait {time}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def pet_chance(self, ctx, value:float=0.75):
        """Change % chance of petting/getting hurt"""
        data = json_open(pet_count_path)
        guild_dict = data[str(ctx.guild.id)]
        if value>=1 or value<0:
            await ctx.send("Enter a value between 0 and 1")
        else:
            guild_dict["chance"] = value
            data[str(ctx.guild.id)] = guild_dict
            json_write(pet_count_path, data)
            value = value*100
            value = int(value)
            await ctx.send(f"Ferroseed has now **{value}%** chance of getting pet")


    @commands.command()
    async def pets_total(self, ctx):
        """Show server total pet and hurt count"""
        data = json_open(pet_count_path)
        guild_dict = data[str(ctx.guild.id)]
        petcount = str(guild_dict["Total pet"])
        hurtcount = str(guild_dict["Total hurt"])
        await ctx.send("I've been pet **"+petcount+"x** times and I've hurt all of you **"+hurtcount+"x** times")

    @commands.command()
    async def pets(self, ctx):
        """Show personal pet and hurt count"""
        data = json_open(pet_count_path)
        guild_dict = data[str(ctx.guild.id)]
        Member_dict = guild_dict["Members"]
        if str(ctx.author.id) in Member_dict.keys():
            user_dict = Member_dict[str(ctx.author.id)]
            pet = str(user_dict["pet"])
            hurt = str(user_dict["hurt"])
            allowed_mentions = discord.AllowedMentions(users=False)
            await ctx.send(f"{ctx.author.mention}! you have pet me **{pet}x** times, and have been hurt **{hurt}x** times.", allowed_mentions=allowed_mentions)


def setup(client):
    client.add_cog(petting(client))  
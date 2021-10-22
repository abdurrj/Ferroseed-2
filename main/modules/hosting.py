from discord.ext import commands
from discord.ext.commands import Cog
from discord.utils import get
import discord

class Hosting(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def host(self, ctx, *, chaname):
        chnid = 739139612005630014
        if ctx.message.channel.id == chnid:
            a = str(chaname)
            b = str.replace(a, " ", "-")
            raid_category = self.client.get_channel(739139545202950161)
            print(raid_category)
            await ctx.guild.create_text_channel(str(b), category=raid_category)
        else:
            return



    # To end channels created in the category "A raid category", but also not allowing to close
    # the channel "A raid category", which is the only channel .host command works
    @commands.command()
    async def end(self, ctx):
        a = ctx.message.channel.id
        b = ctx.message.channel.category_id
        raidcat = 739139545202950161
        '''
        Channels and ID's
        #a-current-den-list = 735961355747590215
        #a-den-promo-pic-channel = 735170480545333308
        #a-raid-category = 739139612005630014
        '''
        raidchan = [739139612005630014, 735170480545333308, 735961355747590215]
        channeltest = all(channel != a for channel in raidchan)
        # To prevent deleting channels outside "A RAID CATEGORY"
        if raidcat == b: # Checks if the command is used inside "A RAID CATEGORY"
            if channeltest == True: # Prevents the command from working in the channel "a-raid-category"
                await ctx.message.channel.delete()
            else:
                await ctx.send("Not this channel, it's important! <a:RBops2:718139698912034937>")
        else:
            await ctx.send("Not this channel, it's important! <a:RBops2:718139698912034937>")

    @Cog.listener("on_raw_reaction_add")
    async def create_voice_channel(self, payload):
        guild = self.client.get_guild(payload.guild_id)
        message_id = payload.message_id
        if message_id == 770315723464638484:
            voice_category = self.client.get_channel(739139545202950161)
            channel_list = guild.channels
            channel_name_list = []
            for i in range(0, len(channel_list)):
                channel_name = channel_list[i].name
                channel_name_list.append(channel_name)
            if payload.emoji.name == '🟥':
                channel_name = "a-red-voice-channel"
                if channel_name in channel_name_list:
                    print("Channel already created")
                else:
                    await guild.create_voice_channel(channel_name, category=voice_category)
            elif payload.emoji.name == '🟩':
                channel_name = "a-green-voice-channel"
                if channel_name in channel_name_list:
                    print("Channel already created")
                else:
                    await guild.create_voice_channel(channel_name, category=voice_category)
            elif payload.emoji.name == '🟦':
                channel_name = "a-blue-voice-channel"
                if channel_name in channel_name_list:
                    print("Channel already created")
                else:
                    await guild.create_voice_channel(channel_name, category=voice_category)

    @Cog.listener("on_raw_reaction_remove")
    async def remove_voice_channel(self, payload):
        guild = self.client.get_guild(payload.guild_id)
        message_id = payload.message_id
        if message_id == 770315723464638484:
            if payload.emoji.name == '🟥':
                channel_name = "a-red-voice-channel"
                channel = discord.utils.get(guild.voice_channels, name=channel_name)
                await channel.delete()
            elif payload.emoji.name == '🟩':
                channel_name = "a-green-voice-channel"
                channel = discord.utils.get(guild.voice_channels, name=channel_name)
                await channel.delete()
            elif payload.emoji.name == '🟦':
                channel_name = "a-blue-voice-channel"
                channel = discord.utils.get(guild.voice_channels, name=channel_name)
                await channel.delete()



"""
    @commands.command()
    async def ctchan(self, ctx, *,channelName): # User must specify channel name when calling command
        await ctx.send("Name of category:")

        # A check to make sure that the the bot waits for a message by the user who called the command
        # This check is called on in wait_for
        def check(m):
            return m.author == ctx.author
        
        # Using .content.upper() since all category names are in upper case
        categoryName = await self.client.wait_for('message', check=check, timeout=15)

        # Looking for a CategoryChannel, using discord.utils.find, with lambda expression to match name
        categoryChannel = discord.utils.get(ctx.guild.categories, name=categoryName.content.upper())

        # If it found a category
        if categoryChannel:
            # Create the channel with desired name, in the category it found
            await ctx.guild.create_text_channel(channelName, category=categoryChannel)
            return
        # Didn't find a category? Tell the user it didn't find one, don't create a channel
        await ctx.send(f"Couldn't find a category by the name __**{categoryName}**__. Aborting")
"""

def setup(client):
    client.add_cog(Hosting(client))

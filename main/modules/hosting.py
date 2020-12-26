from discord.ext import commands

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





def setup(client):
    client.add_cog(Hosting(client))

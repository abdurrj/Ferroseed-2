import discord
from discord.ext import commands
from discord.ext.commands import BadArgument, Cog
from io import BytesIO
import random, emoji, re, sys
import numpy as np

class functions(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clearup(self, ctx, amount:int=0):
        await ctx.message.delete()
        await ctx.message.channel.purge(limit=amount)


    @commands.command()
    async def flip(self, ctx):
        options = ['Heads','Tails','Side']
        selection = np.random.choice(options,1,p=[0.49, 0.49, 0.02])
        await ctx.send(selection[0]) 


    @commands.command()
    async def poll(self, ctx, *, a:str):
        id = ctx.message.author.id
        emoji_init_string = str(emoji.emoji_lis(a))
        disc_emoji_sep = re.findall(r"':([^:']*):'", emoji.demojize(emoji_init_string))
        disc_emoji_string = emoji.emojize(str([''.join(':' + demoji + ':') 
                                        for demoji in disc_emoji_sep]))
        disc_emoji = re.findall(r"'([^']*)'", disc_emoji_string)
        custom_emojis = re.findall(r'<([^>]*)>', a)
        cemojilist = [''.join('<' + cemoji + '>') for cemoji in custom_emojis]
        all_emojis = disc_emoji + cemojilist
        poll = await ctx.send("**Poll from** <@" + str(id) + ">**!!**\n"
                            ""+ a)
        for i in all_emojis:
            try:
                await poll.add_reaction(i)
            except:
                print("Emoji " + i + " not found")


    @commands.command()
    async def spoiler(self, ctx, *, text:str=""):
        poster = ctx.message.author.id
        files = []
        for file in ctx.message.attachments:
            fp = BytesIO()
            await file.save(fp)
            files.append(discord.File(fp, filename=file.filename, spoiler=True))
        await ctx.message.delete()
        await ctx.send("Sent by <@"+str(poster)+">\n"+str(text), files=files)


    @commands.command()
    async def teams(self, ctx):
        guild = ctx.message.guild
        team1 = guild.get_role(746168865737932831)
        team1_name = team1.name
        team1_members = [member.id for member in team1.members]
        team1_size = str(len(team1_members))
        if team1_size == "0":
            team1_members_at = "None"
        else:
            team1_members_at = (''.join('<@' + str(team1_id) + '> \n' for team1_id in team1_members))

        team2 = guild.get_role(746169087347916851)
        team2_name = team2.name
        team2_members = [member.id for member in team2.members]
        team2_size = str(len(team2_members))
        if team2_size == "0":
            team2_members_at = "None"
        else:
            team2_members_at = (''.join('<@' + str(team2_id) + '> \n' for team2_id in team2_members))
        
        embed = discord.Embed(title="Territory war!", description="Team standings in territory war.", colour=0xFF0000)
        embed.add_field(name=team1_name + " (Members: " + team1_size + ")", value=team1_members_at, inline=True)
        embed.add_field(name=team2_name + " (Members: " + team2_size + ")", value=team2_members_at, inline=True)
        await ctx.send(embed=embed)


    @commands.command()
    async def gibroll(self, ctx, wnr_amount:int=1):
        guild = ctx.message.guild
        raffle_channel = discord.Guild.get_channel(guild, channel_id=766277566934810634)
        command_user = ctx.message.author
        message = await  raffle_channel.history().find(lambda m: m.author.id == command_user.id)
        keyword = 'raffle time!'

        if keyword in message.content.lower():
            if int(wnr_amount) < 1:
                await ctx.send("why would you do that :(")
            else:
                await command_user.send("Thank you for being so awesome!")
                for reaction in message.reactions:
                    seed = random.randrange(sys.maxsize)
                    random.Random(seed)
                    user_list = [user async for user in reaction.users()]
                    print(user_list)
                    participants = int(len(user_list))
                    if int(wnr_amount) > int(participants):
                        winner = random.sample(user_list, k=int(participants))
                        winner_names = ', '.join([winner.name for winner in winner])
                        winner_id = ', '.join([''.join('<@' + str(winner.id) + '>') for winner in winner])
                    else:
                        winner = random.sample(user_list, k=int(wnr_amount))
                        winner_names = ', '.join([winner.name for winner in winner])
                        winner_id = ', '.join([''.join('<@' + str(winner.id) + '>') for winner in winner])
                    await command_user.send("\n"+str(participants) + " participants for the emoji: "+ str(reaction) + "\nWinner name(s):\n"
                                + str(winner_names)+"\nWinner ID:\n```"+str(winner_id) + "```")
                    
        else:
            await ctx.send("Sorry, I can't find your message in <#766277566934810634>. Does it have the keyword: " + keyword + ""
                    "\nI can only see your last message, you can edit the message to add the keyword though!")
    

    @gibroll.error
    async def gibroll_error(self, ctx, error):
        if isinstance(error, BadArgument):
            await ctx.send("Something went wrong, please check your input, and make sure it's a number")


    @commands.command()
    async def dice(self, ctx, *,initial_input:str=""):
        listed_input = initial_input.split(" ")
        sides = 6 ; amount = 1
        for i in listed_input:
            if i.endswith("s"):
                sides = int(i.split("s")[0])
            
            if i.endswith("a"):
                amount = int(i.split("a")[0])
        
        if sides>60 or sides<1 or amount<1 or amount>10:
            await ctx.send("Maximum allowed dice is 10, maximum allowed sides on each die is 60. Numbers must be positive")
            return

        dice_throws = [] ; i = 0
        while i<amount:
            i+=1
            throw = random.sample(range(1, (sides+1)),1)
            dice_throws.append(throw)
            seed = random.randrange(sys.maxsize)
            random.Random(seed)
        dice_throws.sort()
        result = [str(i) for i in dice_throws]
        text = ", ".join(result)
        await ctx.send("**Result**\n" + f"{text}")

    # Remove this if it has no more use
    @commands.command()
    async def oldroll(self, ctx, wnr_amount, msg_id):
        command_user = ctx.message.author
        print(command_user)
        guild = ctx.message.guild
        channel_id = 766277566934810634
        channel = discord.Guild.get_channel(guild, channel_id=channel_id)
        print(channel)
        message_id = msg_id
        message = await  channel.fetch_message(message_id)
        if wnr_amount.isnumeric():
            if int(wnr_amount) < 1:
                await ctx.send("why would you do that :(")
            else:
                await command_user.send("Thank you for being so awesome!")
                for reaction in message.reactions:
                    seed = random.randrange(sys.maxsize)
                    random.Random(seed)
                    user_list = [user async for user in reaction.users()]
                    participants = int(len(user_list))
                    if int(wnr_amount) > int(participants):
                        winner = random.sample(user_list, k=int(participants))
                        winner_names = ', '.join([winner.name for winner in winner])
                        winner_id = ', '.join([''.join('<@' + str(winner.id) + '>') for winner in winner])
                    else:
                        winner = random.sample(user_list, k=int(wnr_amount))
                        winner_names = ', '.join([winner.name for winner in winner])
                        winner_id = ', '.join([''.join('<@' + str(winner.id) + '>') for winner in winner])
                    await command_user.send("\n"+str(participants) + " participants for the emoji: "+ str(reaction) + "\nWinner name(s):\n"
                                + str(winner_names)+"\nWinner ID:\n```"+str(winner_id) + "```")
        else:
            await ctx.send("What, you want **" + wnr_amount + "** winner(s)? Maybe try a (positive) number?")
        await message.unpin()


    @Cog.listener("on_raw_reaction_add")
    async def reaction_pinning_add(self, payload):
        if payload.emoji.name == "📌":
            pin_channel = self.client.get_channel(payload.channel_id)
            pin_msg = payload.message_id
            pin_msg = await pin_channel.fetch_message(payload.message_id)
            # pin_msg_user = [pin_msg.author.id]
            # pin_reactor = discord.utils.find(lambda m : m.id == payload.user_id, pin_guild.members)
            # pin_reactor_id = int(pin_reactor.id)
            # valid_users = pin_msg_user + admin_users_id
            # valid_users_test = all(user != pin_reactor_id for user in valid_users)
            # if valid_users_test == False:
            await pin_msg.pin()
    
    
    @Cog.listener("on_raw_reaction_remove")
    async def reaction_pinning_remove(self, payload):
        if payload.emoji.name == "📌": 
            pin_channel = self.client.get_channel(payload.channel_id)
            pin_msg = payload.message_id
            pin_msg = await pin_channel.fetch_message(payload.message_id)
            # pin_msg_user = [pin_msg.author.id]
            # pin_reactor = discord.utils.find(lambda m : m.id == payload.user_id, pin_guild.members)
            # pin_reactor_id = int(pin_reactor.id)
            # valid_users = pin_msg_user + admin_users_id
            # valid_users_test = all(user != pin_reactor_id for user in valid_users)
            # if valid_users_test == False: # use this if you want only message author and admins to be able to unpin
            await pin_msg.unpin()



def setup(client):
    client.add_cog(functions(client))
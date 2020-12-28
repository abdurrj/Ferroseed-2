import discord
from discord.ext import commands
from discord.ext.commands import Cog
from datetime import datetime
from .server_settings import json_open, json_write
import pytz
import random

class fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Naught, for when you don't catch the pokemon
    @commands.command(pass_context=True, name = 'naught', aliases=['not'])
    async def naught(self, ctx):
        id = ctx.message.author.id
        embed = discord.Embed(
        colour = discord.Colour.red())
        embed.add_field(name='<:sherbSad:732994987683217518> escaped', value="<@"+str(id)+"> did not catch the pokemon.", inline=True)
        a = await ctx.send(embed=embed)
        await discord.Message.add_reaction(a, "<:ferroSad:735707312420945940>")


    @commands.command(name = 'caught', aliases=['c', 'catch', 'CAUGHT', 'CATCH', 'CAUGHT!', 'caught!', 'catch!', 'CATCH!'])
    async def caught(self, ctx, *ball):
        id = ctx.message.author.id
        data = json_open('main/data/ball_list.json')
        ball_list = data
        
        # List of colours: (0)Light blue, (1)light green, (2)purple, (3)yellow, (4)white, (5)peach, (6)pink, (7)Blue, (8)Honey yellow
        colour = random.choice([0x96e6ff, 0x62eb96, 0x9662eb, 0xffe36f, 0xe5e5e5, 0xf7b897, 0xffb3ba, 0x21b1ff, 0xffd732])
        if ball:
            ball_used = str(ball[0])
            if ball_used in ball_list.values():
                ball_emoji = ball_used
            else:
                ball_used = ball_used.lower()
                if ball_used in ball_list.keys():
                    ball_emoji = ball_list[ball_used]
                else:
                    ball_emoji = '<:xPoke:764576089275891772>'
        else:
            ball_emoji = '<:xPoke:764576089275891772>'
        
        embed = discord.Embed(
        colour = colour)
        embed.add_field(name=ball_emoji + " Caught!", value="<:RParty:706007725070483507> <@"+str(id)+"> has caught the pokemon! <:RParty:706007725070483507>", inline=True)
        a = await ctx.send(embed=embed)
        await a.add_reaction("<:ferroHappy:734285644817367050>")
        await a.add_reaction("<:sayHeart:741079360462651474>")
        if ball_emoji != '<:xPoke:764576089275891772>':
            await a.add_reaction(ball_emoji)


    @commands.command()
    async def hi(self, ctx):
        data = json_open('main/data/user_greet.json')
        allowed_mentions = discord.AllowedMentions(users=False, roles=False, everyone=False)
        if str(ctx.author.id) in data.keys():
            if data[str(ctx.author.id)]:
                await ctx.send(data[str(ctx.author.id)], allowed_mentions=allowed_mentions)
            else:
                await ctx.send("<:ferroHappy:734285644817367050>")
        else:
            await ctx.send("<:ferroHappy:734285644817367050>")

    
    @commands.command()
    async def hi_set(self, ctx, *, greet:str=None):
        data = json_open('main/data/user_greet.json')
        data[str(ctx.author.id)] = greet
        json_write('main/data/user_greet.json', data)
        allowed_mentions = discord.AllowedMentions(users=False)
        if not greet:
            greet = "<:ferroHappy:734285644817367050>"
        await ctx.send(f"{ctx.author.mention}, I will now respond to `.hi` with {greet}", allowed_mentions=allowed_mentions)
    

    # Go to sleep commands
    @commands.command()
    async def sleep(self, ctx, str:str=None):
        if not str:
            str = ctx.author.mention

        allowed_mentions = discord.AllowedMentions(users=False)
        await ctx.send("Go to sleep, "+str+" <a:RBops2:718139698912034937>", allowed_mentions=allowed_mentions)

    # Work command
    @commands.command(name = 'work', aliases=['homework'])
    async def work(self, ctx, str:str=None):
        choice = [1,2,3,4,5,6,7,8,9,10]
        selection = random.choice(choice)
        if not str:
            str = ctx.author.mention
        allowed_mentions = discord.AllowedMentions(users=False)
        if selection >= 6:
            await ctx.send("<a:RBops:718139734693773330> "+str+"! Go be productive.", allowed_mentions=allowed_mentions)
        else:
            await ctx.send(str+"! Go do the things. <:RStudy:762627515747008512>", allowed_mentions=allowed_mentions)


    @commands.command()
    async def absleep(self, ctx):
        if ctx.message.author.id in [138411165075243008]:
            embed = discord.Embed(
            colour = discord.Colour.green())
            embed.add_field(name='*Abdur is going to sleep*', value=":zzz: :zzz: :zzz:")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
            colour = discord.Colour.green())
            embed.add_field(name='ABDUR!!', value="Go to sleep! <a:RBops2:718139698912034937>")
            await ctx.send(embed=embed)


    # Write a better code!
    @commands.command()
    async def time(self, ctx):
        timezones = ['Singapore', 'Europe/Oslo', 'Europe/Lisbon','Canada/Newfoundland', 'US/Eastern', 'US/Central','US/Pacific']
        timezone_names = ['Malaysia', 'Central Europe', 'West Europe', 'Newfoundland', 'US Eastern', 'US Central', 'US Pacific']

        output = []
        # only_tz_name = []
        # only_tz_time = []
        for i in range(0,len(timezones)):
            tz = timezones[i]
            tz = pytz.timezone(tz)
            tz_name = timezone_names[i]
            tz_hour = datetime.now(tz).strftime("%H")
            if int(tz_hour) < 5 or int(tz_hour)>22:
                time = datetime.now(tz).strftime("%I:%M %p") + ". <a:RSleep:718830355381223444>"
            else:
                time = datetime.now(tz).strftime("%I:%M %p") + ""
            
            timezone_time = tz_name + "\n" + time
            # only_tz_name.append(tz_name)
            # only_tz_time.append(time)
            output.append(timezone_time)

        times = '\n\n'.join(i for i in output)
        # only_tz_name = '\n'.join(i for i in only_tz_name)
        # only_tz_time = '\n'.join(i for i in only_tz_time)

        embed = discord.Embed(title='Afss time!  🌎🌍🌏', color=discord.Colour.green())
        embed.add_field(name='Time:', value=times, inline=True)
        # embed.add_field(name="Time zone:" value=only_tz_name)
        # embed.add_field(name="Time:", value=only_tz_time)
        await ctx.send(embed=embed)

    @Cog.listener("on_message")
    async def say_morning(self, message):
        allowed_mentions = discord.AllowedMentions(users=False)
        if message.author == self.client.user:
            return
        if message.content.lower().startswith("morning"):
            await message.channel.send(f"Morning {message.author.mention}! <:ferroHappy:734285644817367050>", allowed_mentions=allowed_mentions)


def setup(client):
    client.add_cog(fun(client))    
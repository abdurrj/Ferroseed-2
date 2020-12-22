from discord.ext.commands import Cog
from discord.ext import commands

class host(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def lite_command(self, ctx):
        print("Lite command working")



def setup(client):
    client.add_cog(host(client))
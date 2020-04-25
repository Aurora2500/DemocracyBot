import discord
from discord.ext import commands
from discord.ext.commands import Cog

class DemocracyCog(Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong")

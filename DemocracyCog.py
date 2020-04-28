import discord
from discord.ext import commands
from discord.ext.commands import Cog

import DatabaseManager as dm

class DemocracyCog(Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong")

    @commands.command()
    async def register(self, ctx):

        id = ctx.author.id
        try:
            dm.create_user(id)
        except dm.RowExistsError as e:
            await ctx.send("You already have an account!")
        else:
            await ctx.send("Successfully registered!")

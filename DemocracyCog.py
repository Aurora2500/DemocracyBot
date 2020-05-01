import asyncio

import discord
from discord.ext import commands
from discord.ext.commands import Cog

import DatabaseManager as dm

user_not_registered = "You do not have an account!"

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
        except dm.RowExistsError:
            await ctx.send("You already have an account!")
        else:
            await ctx.send("Successfully registered!")

    @commands.command()
    async def createvote(self, ctx, votename):
        if dm.vote_exists(votename):
            await ctx.send("Vote already exists!")
            return
        
        def check(m):
            return m.author.id == ctx.author.id and m.channel == ctx.channel

        await ctx.send("Send line separated choices")
        options: str
        try:
            options = await self.bot.wait_for("message", check=check, timeout=90)  
        except asyncio.TimeoutError:
            ctx.send("Timed out")
            return
        options = options.content.split("\n")
        
        dm.create_vote(votename, *options)
        await ctx.send("Vote created successfully")
        
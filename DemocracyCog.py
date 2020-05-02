import asyncio

import discord
from discord.ext import commands
from discord.ext.commands import Cog

import DatabaseManager as dm
from Ballot import Ballot
from Vote import Vote


user_not_registered = "You do not have an account!"

class DemocracyCog(Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong")

    @commands.command()
    async def createvote(self, ctx, votename):
        if dm.vote_exists(votename):
            await ctx.send("Vote with that name already exists!")
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
        
    @commands.command()
    async def vote(self, ctx, votename: str):
        if not dm.vote_exists(votename):
            await ctx.send("Vote doesn't exist!")
            return
        self._ensure_user_exists(ctx)
        vote = dm.lookup_vote_by_votename(votename)
        msg = f"Please chose the order in which you want to vote for {vote.name}:\n\n"
        for i, option in enumerate(vote):
            msg+=f"{i+1}.- {option}\n"
        await ctx.send(msg)

        def check(m):
            if not (m.content.replace(" ","").isnumeric()
            and m.channel == ctx.channel
            and m.author == ctx.author):
                print(1)
                return False
            numlist = list(map(int, m.content.split()))
            unique = bool(len(numlist) == len(set(numlist)))
            for e in vote:
                print(e)
            print(numlist)
            return (unique and len(numlist) <= len(vote)
            and max(numlist) <= len(vote))

        try:
            ranks = await self.bot.wait_for("message", timeout=60, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Timed out")
            return
        
        ranklist = list(map(int, ranks.content.split()))
        dm.cast_vote(Ballot(str(ctx.author.id), votename, ranklist))
        await ctx.send("Voted sucessfully!")
        
 




    
    def _ensure_user_exists(self, ctx)-> bool:
        if not dm.user_exists(str(ctx.author.id)):
           dm.create_user(str(ctx.author.id))
           return True
        return False
#DemocracyCog.py

import asyncio
from typing import List, Set, Optional
from queue import Queue

import discord
from discord.ext import commands
from discord.ext.commands import Cog, Context

import DatabaseManager as dm
from Ballot import Ballot
from Vote import Vote


user_not_registered = "You do not have an account!"

class DemocracyCog(Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: Context):
        await ctx.send("pong")

    @commands.command()
    async def represent(self, ctx: Context, target: discord.Member = None):
        self._ensure_user_exists(ctx.author)
        if target is None or target == ctx.author:
            dm.represent(ctx.author.id, "")
            await ctx.send("No one is representing you now!")
            return
        self._ensure_user_exists(target)
        dm.represent(ctx.author.id, target.id)
        await ctx.send(f"{target.nick} now represents you!")

    @commands.command()
    async def representing(self, ctx: Context, target: Optional[discord.Member] = None, votename: str = None):
        if target is None:
            target = ctx.author
        self._ensure_user_exists(target)

        representative_id = (dm.lookup_representative(str(target.id)))
        representative_string = "None"
        if(representative_id):
            representative = ctx.guild.get_member(representative_id)
            representative_string = representative.nick
        representing_id = self._get_representing_users(target, votename)
        representing_string = "None"
        if bool(representing_id):
            representing_string = "\n".join(ctx.guild.get_member(member_id).nick for member_id in representing_id)
        
        
        embed = discord.Embed(title= "Representation", color = 0xff0000)
        embed.add_field(name="Representative", value=representative_string, inline=False)
        embed.add_field(name="Representing", value=representing_string, inline=False)

        await ctx.send(embed=embed)

        
        


    @commands.command()
    async def createvote(self, ctx: Context, votename: str):
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
    async def vote(self, ctx: Context, votename: str):
        if not dm.vote_exists(votename):
            await ctx.send("Vote doesn't exist!")
            return
        self._ensure_user_exists(ctx.author)
        vote = dm.lookup_vote_by_votename(votename)
        msg = f"Please chose the order in which you want to vote for {vote.name}:\n\n"
        for i, option in enumerate(vote, start=1):
            msg+=f"{i}.- {option}\n"
        await ctx.send(msg)

        def check(m):
            if not (m.content.replace(" ","").isnumeric()
            and m.channel == ctx.channel
            and m.author == ctx.author):
                return False
            numlist = list(map(int, m.content.split()))
            unique = bool(len(numlist) == len(set(numlist)))
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
    
    @commands.command()
    async def countup(self, ctx: Context, votename: str):
        pass


    def _get_representing_users(self, user: discord.Member, vote: str = None) -> Set[int]:
        if vote is None:
            participating = set()
        else:
            participating = dm.lookup_voting_by_votename(vote)
        participating.add(user.id)
        total_representing_id = set()
        looking = Queue()
        looking.put_nowait(str(user.id))
        while not looking.empty():
            curent = looking.get_nowait()
            # you're not representing people who are participating
            representing = set(dm.lookup_representing(curent)) - participating - total_representing_id
            total_representing_id |= representing
            for member in representing:
                looking.put_nowait(member)
        
        return total_representing_id


    def _ensure_user_exists(self, user: discord.Member)-> bool: #return true if it needed to create an user
        if not dm.user_exists(str(user.id)):
           dm.create_user(str(user.id))
           return True
        return False
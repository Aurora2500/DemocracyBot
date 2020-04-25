import discord
from discord.ext import commands

from DemocracyCog import DemocracyCog
import Secret

description = "desc"

bot = commands.Bot(command_prefix='a!', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.add_cog(DemocracyCog(bot))

bot.run(Secret.token)
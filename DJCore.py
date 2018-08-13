import discord
import os
from discord.ext import commands

bot = commands.AutoShardedBot(case_insensitive=True, command_prefix=commands.when_mentioned_or(os.getenv('PREFIX')))
bot.remove_command('help')
bot.initials = ('modules.misc', 'modules.music', 'modules.handler', 'modules.owner')
bot.owner = int(os.getenv('OWNER'))
bot.color = int(os.getenv('COLOR'), 16)

@bot.check
async def _bot_protection(ctx):
    return not ctx.author.bot

@bot.event
async def on_ready():
    print(f'Bot is ready! Logged as in: {bot.user}')
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=f"your move | {os.getenv('PREFIX')}help"))

if __name__ == "__main__":
    for extension in bot.initials:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}: {e}')

bot.run(os.getenv('TOKEN'))

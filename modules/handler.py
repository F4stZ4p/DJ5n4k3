import traceback
import sys
from discord.ext import commands
import discord

class CommandErrorHandler:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
        
        ignored = (commands.MissingRequiredArgument, commands.BadArgument, commands.NoPrivateMessage, commands.CheckFailure, commands.CommandNotFound, commands.DisabledCommand, commands.CommandInvokeError, commands.TooManyArguments, commands.UserInputError, commands.CommandOnCooldown, commands.NotOwner, commands.MissingPermissions, commands.BotMissingPermissions)   
        error = getattr(error, 'original', error)
        

        if isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=discord.Embed(color=self.bot.color).set_footer(text=f"Seems like {error}.", icon_url=ctx.author.avatar_url))

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(color=self.bot.color).set_footer(text=f"Seems like {error}.", icon_url=ctx.author.avatar_url))

        elif isinstance(error, commands.NoPrivateMessage):
            return

        elif isinstance(error, commands.CheckFailure):
            await ctx.send(embed=discord.Embed(color=self.bot.color).set_footer(text=f"Seems like this command is thought for other users. You can't use it.", icon_url=ctx.author.avatar_url))

        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(embed=discord.Embed(color=self.bot.color).set_footer(text=f"Seems like this command in disabled.", icon_url=ctx.author.avatar_url))

        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send(embed=discord.Embed(color=self.bot.color).set_footer(text=f"Seems like something went wrong. Report this issue to the developer.", icon_url=ctx.author.avatar_url))

        elif isinstance(error, commands.TooManyArguments):
            await ctx.send(embed=discord.Embed(color=self.bot.color).set_footer(text=f"Seems like you gave too many arguments.", icon_url=ctx.author.avatar_url))

        elif isinstance(error, commands.UserInputError):
            await ctx.send(embed=discord.Embed(color=self.bot.color).set_footer(text=f"Seems like you did something wrong.", icon_url=ctx.author.avatar_url))

        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(embed=discord.Embed(color=self.bot.color).set_footer(text=f"Seems like {error}.", icon_url=ctx.author.avatar_url))

        elif isinstance(error, commands.NotOwner):
            await ctx.send(embed=discord.Embed(color=self.bot.color).set_footer(text=f"Seems like you do not own this bot.", icon_url=ctx.author.avatar_url))

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=discord.Embed(color=self.bot.color).set_footer(text=f"Seems like {error}.", icon_url=ctx.author.avatar_url))

        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(embed=discord.Embed(color=self.bot.color).set_footer(text=f"Seems like {error}.", icon_url=ctx.author.avatar_url))

def setup(bot):
    print('Error handler loaded.')
    bot.add_cog(CommandErrorHandler(bot))
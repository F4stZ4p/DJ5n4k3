import discord
from discord.ext import commands
from utils.HelpPaginator import HelpPaginator, CannotPaginate

class Misc():
    """Miscellaneous commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, *, command: str = None):
        """Shows help about a command or the bot"""
        try:
            if command is None:
                p = await HelpPaginator.from_bot(ctx)
            else:
                entity = self.bot.get_cog(command) or self.bot.get_command(command)

                if entity is None:
                    clean = command.replace('@', '@\u200b')
                    return await ctx.send(f'Command or category "{clean}" not found.')
                elif isinstance(entity, commands.Command):
                    p = await HelpPaginator.from_command(ctx, entity)
                else:
                    p = await HelpPaginator.from_cog(ctx, entity)

            await p.paginate()
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    async def ping(self, ctx):
        """Check my reaction time!"""
        resp = await ctx.send('Loading...')
        diff = resp.created_at - ctx.message.created_at
        await resp.edit(content=f':ping_pong: Pong! API latency: {1000*diff.total_seconds():.1f}ms. {self.bot.user.name} latency: {round(self.bot.latency * 1000)}ms')

def setup(bot):
    bot.add_cog(Misc(bot))
    print('Miscellaneous module loaded.')

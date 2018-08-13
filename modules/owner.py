from discord.ext import commands
import asyncio
import traceback
import discord
import inspect
import textwrap
from contextlib import redirect_stdout
import io
import re
from platform import python_version
import gc
import copy
import os, sys

# to expose to the eval command
import datetime
from collections import Counter

class Admin:

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()

    def cleanup_code(self, content):
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
        return content.strip('` \n')

    async def __local_check(self, ctx):
        if ctx.author.id == self.bot.owner:
            return True
        else:
            return


    @commands.command(pass_context=True, hidden=True, name='eval', aliases=['evaluate'])
    async def _eval(self, ctx, *, body: str):
        """Evaluates a piece of code"""
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            fooem = discord.Embed(color=0xff0000)
            fooem.add_field(name="Code evaluation was not successful.", value=f'```\n{e.__class__.__name__}: {e}\n```'.replace(self.bot.http.token, '•' * len(self.bot.http.token)))
            fooem.set_footer(text=f"Evaluated using Python {python_version()}", icon_url="http://i.imgur.com/9EftiVK.png")
            fooem.timestamp = ctx.message.created_at
            return await ctx.send(embed=fooem)

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            fooem = discord.Embed(color=0xff0000)
            fooem.add_field(name="Code evaluation was not successful.", value=f'```py\n{value}{traceback.format_exc()}\n```'.replace(self.bot.http.token, '•' * len(self.bot.http.token)))
            fooem.set_footer(text=f"Evaluated using Python {python_version()}", icon_url="http://i.imgur.com/9EftiVK.png")
            fooem.timestamp = ctx.message.created_at
            await ctx.send(embed=fooem)
        else:
            value = stdout.getvalue()

            if ret is None:
                if value:
                    sfooem = discord.Embed(color=self.bot.color)
                    sfooem.add_field(name="Code evaluation was successful!", value=f'```py\n{value}\n```'.replace(self.bot.http.token, '•' * len(self.bot.http.token)))
                    sfooem.set_footer(text=f"Evaluated using Python {python_version()}", icon_url="http://i.imgur.com/9EftiVK.png")
                    sfooem.timestamp = ctx.message.created_at
                    await ctx.send(embed=sfooem)
            else:
                self._last_result = ret
                ssfooem = discord.Embed(color=self.bot.color)
                ssfooem.add_field(name="Code evaluation was successful!", value=f'```py\n{value}{ret}\n```'.replace(self.bot.http.token, '•' * len(self.bot.http.token)))
                ssfooem.set_footer(text=f"Evaluated using Python {python_version()}", icon_url="http://i.imgur.com/9EftiVK.png")
                ssfooem.timestamp = ctx.message.created_at
                await ctx.send(embed=ssfooem)

    @commands.command(hidden=True, aliases=['die'])
    async def logout(self, ctx):
        """Logs out bot from Discord"""
        await self.bot.logout()

    @commands.command(hidden=True, aliases=["say","print"])
    async def echo(self, ctx, *, content):
        await ctx.send(content)

    @commands.command(hidden=True, aliases=["impersonate"])
    async def runas(self, ctx, member: discord.Member, *, cmd):
        """Invoke bot command as specified user"""
        msg = copy.copy(ctx.message)
        msg.content = f"{ctx.me.mention} {cmd}"
        msg.author = member
        await self.bot.process_commands(msg)

    @commands.command(hidden=True, aliases=['r'])
    async def restart(self, ctx):
        """Restarts the bot"""
        await ctx.send(embed=discord.Embed(color=self.bot.color).set_footer(text="Restarting..."))
        os.execl(sys.executable, sys.executable, * sys.argv)

    @commands.command(hidden=True, aliases=['cc'])
    async def changecolor(self, ctx, *, color):
        """Change the bot color (temporary)
        Example: changecolor 0xFF0000
        """
        try:
            self.bot.color = int(color, 16)
        except:
            await ctx.send(':thumbsdown:')
        else:
            await ctx.send(':thumbsup:')

def setup(bot):
    bot.add_cog(Admin(bot))
    print('Owner module loaded.')

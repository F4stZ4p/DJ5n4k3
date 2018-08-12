import discord
import asyncio
import random
from discord.ext import commands

class RainbowRole():
    """Rainbow role for your discord!"""
    def __init__(self, bot):
        self.bot = bot
        self._rainbow_roles = {}
        self._rainbow_cooldown = {}
        self._guild_tasks = {}

    def _do_randomize(self):
        return discord.Color(random.randint(0x000000, 0xFFFFFF))

    async def _get_role(self, role: discord.Role):
        return await discord.utils.get(ctx.guild.roles, id=role.id)

    async def _do_rainbow_role(self, ctx, guild: discord.Guild):
        while not self.bot.is_closed():
            try:
                await asyncio.sleep(self._rainbow_cooldown[guild.id])
                await self._get_role(self._rainbow_roles[guild.id]).edit(color=self._do_randomize)
            except KeyError:
                pass

    @commands.command(aliases=['rr'])
    async def rainbowrole(self, ctx, role: discord.Role, *, cooldown: int):
        """Creates a rainbow role"""
        try:
            self._guild_tasks[ctx.guild.id].cancel()
        except:
            pass
        if cooldown <= 1:
            await ctx.send(":warning: | **Cooldown can't be lesser than 1**", delete_after=5)
        else:
            self._rainbow_roles[ctx.guild.id] = role
            self._rainbow_cooldown[ctx.guild.id] = cooldown
            try:
                self._guild_tasks[ctx.guild.id] = await self.bot.loop.create_task(None, self._do_rainbow_role, ctx.guild)
            except Exception as e:
                await ctx.send(f':thumbsdown:: {e}')
            else:
                await ctx.send(':thumbsup:')

def setup(bot):
    bot.add_cog(RainbowRole(bot))
    print('Rainbow Role module loaded.')
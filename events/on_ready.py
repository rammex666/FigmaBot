from nextcord.ext import tasks, commands
import nextcord
from main import bot


class OnReadyEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("FigmaBot is ready!")
        print("By .rammex")
        await bot.change_presence(activity=nextcord.Game("Figma"))


def setup(bot):
    bot.add_cog(OnReadyEvent(bot))

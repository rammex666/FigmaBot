import nextcord
from nextcord.ext import commands


class CustomStatusCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.activities != after.activities:
            for activity in after.activities:
                if activity.type == nextcord.ActivityType.custom and "discord.gg/" in activity.name:
                    role = nextcord.utils.get(after.guild.roles, name="YourRoleName")
                    if role:
                        await after.add_roles(role)
                else:
                    role = nextcord.utils.get(after.guild.roles, name="YourRoleName")
                    if role in after.roles:
                        await after.remove_roles(role)


def setup(bot):
    bot.add_cog(CustomStatusCheck(bot))

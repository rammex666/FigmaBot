import nextcord
from nextcord.ext import commands
from config.channel import get_welcome


class MemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(get_welcome())
        if channel:
            embed = nextcord.Embed(
                title=f"{member.name} vient de rejoindre nôtre serveur",
                color=nextcord.Color.gold(),
                description=f"Bienvenue sur le serveur discord de la communauté Figma !\nN'hésite pas a regarder dans #|1264686167107043491| les informations que nous avons mis en place pour vous aider !"
            )

            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=f"Nous sommes désormais {len(member.guild.members)} membres !")
            await channel.send(embed=embed)
        else:
            print("Channel Welcome not found look in config ")


def setup(bot):
    bot.add_cog(MemberJoin(bot))

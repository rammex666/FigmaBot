import nextcord
from nextcord.ext import commands
from config.database import get_db_connection
from main import bot

class LevelCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.command(name="reset_user")
    @commands.has_permissions(administrator=True)
    async def reset_user(self, ctx, user: nextcord.Member):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE user_levels SET experience = 0, level = 1 WHERE user_id = %s", (user.id,))
        connection.commit()
        cursor.close()
        connection.close()
        await ctx.send(f"Le niveau de {user.mention} a été réinitialisé.")

    @bot.command(name="reset_all")
    @commands.has_permissions(administrator=True)
    async def reset_all(self, ctx):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE user_levels SET experience = 0, level = 1")
        connection.commit()
        cursor.close()
        connection.close()
        await ctx.send("Les niveaux de tous les utilisateurs ont été réinitialisés.")


def setup(bot):
    bot.add_cog(LevelCommand(bot))
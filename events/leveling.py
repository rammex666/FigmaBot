import nextcord
from nextcord.ext import commands
from config.database import get_db_connection
from config.channel import get_leveling
from config.roles import get_level_role

class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = message.author.id
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT experience, level FROM user_levels WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()

        if result:
            experience, level = result
            experience += 3.2
            next_level_exp = level * 105.36

            if experience >= next_level_exp:
                level += 1
                experience = 0
                channel = self.bot.get_channel(get_leveling())
                await channel.send(f"Bravo {message.author.mention}, vous venez de level up vous êtes maintenant level {level}!")

                level_roles = get_level_role()
                for level_role in level_roles:
                    if level_role["level"] == level:
                        role = nextcord.utils.get(message.guild.roles, id=level_role["roleid"])
                        if role:
                            await message.author.add_roles(role)
                            await channel.send(f"{message.author.mention} a reçu le rôle {role.name} pour avoir atteint le niveau {level}!")

            cursor.execute("UPDATE user_levels SET experience = %s, level = %s WHERE user_id = %s", (experience, level, user_id))
        else:
            cursor.execute("INSERT INTO user_levels (user_id, experience, level) VALUES (%s, %s, %s)", (user_id, 10, 1))

        connection.commit()
        cursor.close()
        connection.close()

def setup(bot):
    bot.add_cog(LevelSystem(bot))
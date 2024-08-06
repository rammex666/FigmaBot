import nextcord
from nextcord.ext import commands
import os
from config.bot import get_token
from config.database import create_table_if_not_exists

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


def load_cogs(bot):
    for folder in ['commands', 'events']:
        for filename in os.listdir(folder):
            if filename.endswith('.py'):
                bot.load_extension(f'{folder}.{filename[:-3]}')
                print(f"Loaded {filename[:-3]}")

create_table_if_not_exists()
load_cogs(bot)
bot.run(get_token())

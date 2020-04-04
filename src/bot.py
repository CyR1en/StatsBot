import logging

import discord.ext
from discord.ext import commands

from src.cogs import General
from src.configuration import ConfigFile, ConfigNode

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

config_file = ConfigFile("config")

bot = commands.Bot(command_prefix=config_file.get_node(ConfigNode.PREFIX))
bot.add_cog(General(bot, config_file))

token = config_file.get_node(ConfigNode.TOKEN)
if token == ConfigNode.TOKEN.value[1]:
    token = input("The config file is either newly generated or the token was left to its default value. \n"
                  "Please enter your bot's token:")
    config_file.set(ConfigNode.TOKEN, token)


@bot.event
async def on_ready():
    print('Successfully logged in as {}'.format(bot.user))

bot.run(token)



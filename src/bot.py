import logging
import sys

import discord.ext
from discord.ext import commands

from src.cogs import General
from src.configuration import ConfigFile, ConfigNode

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
fmt = logging.Formatter('[%(levelname)s][%(asctime)s][%(name)s]: %(message)s')
handler.setFormatter(fmt)
s_handler = logging.StreamHandler()
s_handler.setFormatter(fmt)
logger.addHandler(handler)
logger.addHandler(s_handler)

config_file = ConfigFile("config")

bot = commands.Bot(command_prefix=config_file.get_string_node(ConfigNode.PREFIX))
bot.add_cog(General(bot, config_file))

token = config_file.get_string_node(ConfigNode.TOKEN)
if token == ConfigNode.TOKEN.get_value():
    logger.warning("The config file is either newly generated or the token was left to its default value. \n"
                   "Please enter your bot's token:")
    try:
        token = input()
        config_file.set(ConfigNode.TOKEN, token)
    except KeyboardInterrupt:
        logger.error("Interrupted token input")
        sys.exit()


@bot.event
async def on_ready():
    logger.info('Successfully logged in as {}'.format(bot.user))

bot.run(token)

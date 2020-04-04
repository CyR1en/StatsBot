import discord
from configuration import ConfigFile, ConfigNode

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Lorenzo GAAY!')

config_file = ConfigFile("bot_config")

client.run(config_file.get_node(ConfigNode.TOKEN))

import asyncio
import logging
import argparse

from discord import app_commands
from utils.Collage import *
from utils.ImageSelect import *
from utils.Images import *
from utils.Config import get_config
import aiohttp
import discord



class Client(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

    async def update_status(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{len(self.guilds)} /help'))

intents = discord.Intents.default()
client = Client(intents=intents)
config: object

@client.event
async def on_ready():
    logging.info(f'Logged in as {client.user} (ID: {client.user.id})')
    await client.update_status()


@client.event
async def on_guild_join(guild: discord.Guild):
    await client.update_status()


@client.tree.command()
async def invite(interaction: discord.Interaction):
    '''Gives you a bot invite link to share.'''
    await interaction.response.send_message(f'https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=0&scope=applications.commands%20bot')


@client.tree.command()
async def generate(interaction: discord.Interaction, prompt: str):
    '''Generates images based on prompt given.'''
    logging.info(f'Got request to generate images with prompt "{prompt}" from {interaction.user} (ID: {interaction.user.id})')
    await interaction.response.defer(thinking=True)

    images = None
    attempt = 0
    while not images:
        if attempt > 0:
            logging.warning(f'Image generate request failed on attempt {attempt} for prompt "{prompt}" issued by {interaction.user} (ID: {interaction.user.id})')
        attempt += 1
        images = await generate_images(prompt, client.config)

    logging.info(f'Successfully generated images with prompt "{prompt}" from {interaction.user} (ID: {interaction.user.id}) on attempt {attempt}')
    collage = await make_collage(images, 3, client.config)
    collage = discord.File(collage, filename=f'collage.{client.config["COLLAGE_FORMAT"]}')
    images = [discord.File(images[i], filename=f'{i}.jpg') for i in range(len(images))]
    await interaction.followup.send(f'`{prompt}`', file=collage, view=ImageSelectView(collage, images, timeout=client.config['IMAGE_SELECT_TIMEOUT']))




if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())

    parser = argparse.ArgumentParser(
        prog = 'stable diffusion dicord bot',
        description= 'connects SD backend to discord')

    parser.add_argument('-c', '--config', help="Full path to config.json file")
    args = parser.parse_args()

    client.config = get_config(args.config)
    client.run(client.config['BOT_TOKEN'])
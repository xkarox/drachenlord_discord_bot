import os
import discord
import logging
from dotenv import load_dotenv


def main():
    client = discord.Client()

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    #logs errors and debug information into a discord.log file
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w+')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)


    @client.event
    async def on_ready():
        # Setting `Playing ` status
        await client.change_presence(activity=discord.Game(name="am Lümmelmann rum"))
        print(f'{client.user} has connected to the Discord!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('/update'):
            await message.channel.send('Etzala, diese Funktion habe ich noch nicht rausgemeddelt!')

        if message.content.startswith('/hello'):
            await  message.channel.send('Ich bin ned der Drache ferdammde aggsd!!!111!11!')

    client.run(TOKEN)

if __name__ == '__main__':
    main()

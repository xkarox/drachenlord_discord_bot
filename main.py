import os
import discord
import constants
from dotenv import load_dotenv

def main():
    client = discord.Client()

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    @client.event
    async def on_ready():
        print('on_ready')
        print(f'{client.user} has connected to the Discord!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('/hello'):
            await  message.channel.send('Hello!')

    client.run(TOKEN)


if __name__ == '__main__':
    main()

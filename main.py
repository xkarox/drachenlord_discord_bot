import os
import discord
import logging
from dotenv import load_dotenv
from functions import get_stats
from discord.ext import commands, tasks
from datetime import time, timedelta, datetime


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
        time = datetime.now().strftime('%H:%M:%S')
        print(f'[{time}]: {client.user} has connected to the Discord!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('/update'):
            await message.channel.send('Etzala, diese Funktion habe ich noch nicht rausgemeddelt!')

        if message.content.startswith('/stats'):
            m_Date, m_Video, m_Streams, m_Money, d_Date, d_Video, d_Streams, d_Money = get_stats()
            await message.channel.send(f'{m_Date}\n{m_Video}\n{m_Streams}\n{m_Money}\n---------------------------------------\n{d_Date}\n{d_Video}\n{d_Streams}\n{d_Money}\n')

        if message.content.startswith('/hello'):
            await  message.channel.send('Ich bin ned der Drache ferdammde aggsd!!!111!11!')

    @tasks.loop(seconds=31.0)
    async def test():
        if datetime.now().strftime('%H:%M') == time(21, 17):
            print('f')

    y = datetime.now().strftime('%H:%M:%S')
    print(y)
    test.start()
    client.run(TOKEN)

if __name__ == '__main__':
    main()

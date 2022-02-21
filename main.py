import os
import discord
import logging
import configparser
from dotenv import load_dotenv
from functions import get_stats, get_steam_status
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

    #load and read config
    config = configparser.ConfigParser()
    config.read('config.ini')

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
            embed = discord.Embed(title=f'{m_Date}', url='https://drachenchronik.com/', description=f'''
            {m_Video}
            {m_Streams}
            {m_Streams}
            ''', color=discord.Color.blue())
            embed2 = discord.Embed(title=f'{d_Date}', url='https://drachenchronik.com/', description=f'''
            {d_Video}
            {d_Streams}
            {d_Money}
            ''', color=discord.Color.blue())
            await message.channel.send(embed=embed)
            await message.channel.send(embed=embed2)

        if message.content.startswith('/steam'):
            profile_in_game_header, profile_in_game_name = get_steam_status()

            if profile_in_game_header == 'Currently In-Game':
                embed = discord.Embed(title=f'{profile_in_game_header}', url='https://steamcommunity.com/id/DrachenLord1510', description=f'{profile_in_game_name}')
                await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(title=f'{profile_in_game_header}')

        if message.content.startswith('/test'):
            m_Date, m_Video, m_Streams, m_Money, d_Date, d_Video, d_Streams, d_Money = get_stats()
            embed = discord.Embed(title='Schanzne', url='https://drachenchronik.com/', description='descdescriptiondescription', color=discord.Color.blue())
            await message.channel.send(embed=embed)

        if message.content.startswith('/hello'):
            await  message.channel.send('Ich bin ned der Drache ferdammde aggsd!!!111!11!')

    @tasks.loop(seconds=31.0)
    async def get_latest_stats():
        now = datetime.now()
        statsHour = config.get('DrachenStats', 'Hour')
        statsMin = config.get('DrachenStats', 'Minute')
        if now.hour == int(statsHour) and now.minute == int(statsMin):
            m_Date, m_Video, m_Streams, m_Money, d_Date, d_Video, d_Streams, d_Money = get_stats()
            embed = discord.Embed(title=f'{m_Date}', url='https://drachenchronik.com/', description=f'''
            {m_Video}
            {m_Streams}
            {m_Streams}
            ''', color=discord.Color.blue())
            embed2 = discord.Embed(title=f'{d_Date}', url='https://drachenchronik.com/', description=f'''
            {d_Video}
            {d_Streams}
            {d_Money}
            ''', color=discord.Color.blue())
            await message.channel.send(embed=embed)
            await message.channel.send(embed=embed2)


    get_latest_stats.start()
    client.run(TOKEN)

if __name__ == '__main__':
    main()

import os
import discord
import logging
import configparser
from dotenv import load_dotenv
from functions import get_stats, get_steam_status, get_current_steam_game
from discord.ext import commands, tasks
from datetime import time, timedelta, datetime
from pandas import DataFrame




def main():
    client = discord.Client()
    x = 1
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

    text_channel_list = []




    current_time = datetime.now()

    @client.event
    async def on_ready():
        # Setting `Playing ` status
        await client.change_presence(activity=discord.Game(name="am Lümmelmann rum"))
        time = datetime.now().strftime('%H:%M:%S')
        print(f'[{time}]: {client.user} has connected to the Discord!')

        #gets a list of all text channels
        for guild in client.guilds:
            for channel in guild.text_channels:
                text_channel_list.append(channel)
        #print (text_channel_list)

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

        if message.content.startswith('/start'):
            get_current_steam_status.start()

        if message.content.startswith('/steam'):
            profile_in_game_header = get_steam_status()
            STEAM_URL = config.get('Links', 'steam_url_drachenlord')

            if profile_in_game_header == 'Currently In-Game':
                profile_in_game_name = get_current_steam_game()
                old_steam_status[0] = profile_in_game_name
                old_steam_status[1] = profile_in_game_header
                embed = discord.Embed(title=f'{profile_in_game_header}', url=STEAM_URL, description=f'{profile_in_game_name}')
                await message.channel.send(embed=embed)


            elif profile_in_game_header == 'Currently Offline':
                old_steam_status[1] = profile_in_game_header
                embed = discord.Embed(title=f'{profile_in_game_header}', url=STEAM_URL, description=f'Der Dicke ist grad offline auf Steam')
                await message.channel.send(embed=embed)

            else:
                old_steam_status[1] = profile_in_game_header
                embed = discord.Embed(title=f'{profile_in_game_header}', url=STEAM_URL, description=f'')
                await message.channel.send(embed=embed)

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


    old_steam_status = ['placeholder', 'placeholder2']
    @tasks.loop(seconds=10.0)
    async def get_current_steam_status():
        print(f'test: {current_time}')

        profile_in_game_header = get_steam_status()

        try:
            profile_in_game_name = get_current_steam_game()
        except:
            pass

        STEAM_URL = config.get('Links', 'steam_url_drachenlord')

        channel = client.get_channel(943988010410709032)

        if old_steam_status[0] != profile_in_game_header:
            if profile_in_game_header == 'Currently In-Game':
                profile_in_game_name = get_current_steam_game()
                embed = discord.Embed(title=f'{profile_in_game_header}', url=STEAM_URL, description=f'{profile_in_game_name}')
                old_steam_status[0] = profile_in_game_header
                old_steam_status[1] = profile_in_game_name
                await channel.send(embed=embed)

            elif profile_in_game_header == 'Currently Offline':
                embed = discord.Embed(title=f'{profile_in_game_header}', url=STEAM_URL, description=f'Der Dicke ist grad offline auf Steam')
                old_steam_status[0] = profile_in_game_header
                await channel.send(embed=embed)

            else:
                embed = discord.Embed(title=f'{profile_in_game_header}', url=STEAM_URL, description=f'Der Dicke ist grad online auf Steam')
                old_steam_status[0] = profile_in_game_header
                await channel.send(embed=embed)

    get_latest_stats.start()
    client.run(TOKEN)

if __name__ == '__main__':
    main()

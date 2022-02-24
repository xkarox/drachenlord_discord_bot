import os
import discord
import logging
import configparser
from steam_checker import __get_game_image
from dotenv import load_dotenv
from functions import get_stats, get_steam_status, get_current_steam_game, get_youtube_livestream
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






    current_time = datetime.now()

    @client.event
    async def on_ready():
        # Setting `Playing ` status
        await client.change_presence(activity=discord.Game(name="am Lümmelmann rum"))

        channel = client.get_channel(946460819263197194)

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

        if message.content.startswith('/start'):
            check_current_steam_status.start()

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

            elif profile_in_game_header == 'Currently Online':
                old_steam_status[1] = profile_in_game_header
                embed = discord.Embed(title=f'{profile_in_game_header}', url=STEAM_URL, description=f'Der Dicke ist grad online auf Steam')
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
            embed = discord.Embed(title='Der Dreger in seiner vollen Pracht')
            embed.set_image(url='https://images.nordbayern.de/image/contentid/policy:1.11466966:1634893479/image/e-arc-tmp-20211022_094643-3.jpg?f=16%3A9&h=816&m=FIT&w=1680&$p$f$h$m$w=a34c85d')
            await  message.channel.send(embed=embed)

    @tasks.loop(seconds=31)
    async def check_latest_stats():
        now = datetime.now()
        statsHour = config.get('DrachenStats', 'Hour')
        statsMin = config.get('DrachenStats', 'Minute')
        if now.hour == int(statsHour) and now.minute == int(statsMin):
            m_Date, m_Video, m_Streams, m_Money, d_Date, d_Video, d_Streams, d_Money = get_stats()

            embed = discord.Embed(title=f'{m_Date}', url='https://drachenchronik.com/', description=f'''
            {m_Video}
            {m_Streams}
            {m_Money}
            ''', color=discord.Color.blue())

            embed2 = discord.Embed(title=f'{d_Date}', url='https://drachenchronik.com/', description=f'''
            {d_Video}
            {d_Streams}
            {d_Money}
            ''', color=discord.Color.blue())

            channel = client.get_channel(946460819263197194)
            await channel.send(embed=embed)
            await channel.send(embed=embed2)


    old_steam_status = ['placeholder', 'placeholder2']
    @tasks.loop(seconds=10.0)
    async def check_current_steam_status():

        profile_in_game_header = get_steam_status()

        try:
            profile_in_game_name = get_current_steam_game()
        except:
            pass

        STEAM_URL = config.get('Links', 'steam_url_drachenlord')


        if old_steam_status[0] != profile_in_game_header:
            if profile_in_game_header == 'Currently In-Game':
                profile_in_game_name = get_current_steam_game()
                game_image = __get_game_image()
                embed = discord.Embed(title=f'{profile_in_game_header}', url=STEAM_URL, description=f'{profile_in_game_name}')
                embed.set_image(game_image)
                old_steam_status[0] = profile_in_game_header
                old_steam_status[1] = profile_in_game_name
                channel = client.get_channel(946460819263197194)
                await channel.send(embed=embed)

            elif profile_in_game_header == 'Currently Offline':
                embed = discord.Embed(title=f'{profile_in_game_header}', url=STEAM_URL, description=f'Der Dicke ist grad offline auf Steam')
                old_steam_status[0] = profile_in_game_header
                channel = client.get_channel(946460819263197194)
                await channel.send(embed=embed)

            else:
                embed = discord.Embed(title=f'{profile_in_game_header}', url=STEAM_URL, description=f'Der Dicke ist grad online auf Steam')
                old_steam_status[0] = profile_in_game_header
                channel = client.get_channel(946460819263197194)
                await channel.send(embed=embed)


    #checks every 15 minutes if a specified youtube account started a livestream
    #and sends a message with the livestream link
    @tasks.loop(minutes=15)
    async def check_livestream_status():
        livestream = get_youtube_livestream()
        livestream_id = livestream['items'][0]['id']['videoId']
        livestream_title = livestream['items'][0]['snippet']['title']

        with open('livestream_id.txt', 'w') as f:

            old_livestream_id = f.read
            print(old_livestream_id)
            if livestream_id != old_livestream_id:
                embed = discord.Embed(title = livestream_title, description = f'https://www.youtube.com/watch?v={livestream_id}')


                #Note {Adrian} wieso zum fick geht diese scheisse in jeder anderen funktion aber hier nicht
                channel = client.get_channel(946460819263197194)
                #await channel.send(embed=embed)
                await channel.send(f'https://www.youtube.com/watch?v={livestream_id}')
            else:
                print(livestream)


    #check_livestream_status.start()
    check_latest_stats.start()
    client.run(TOKEN)

if __name__ == '__main__':
    main()

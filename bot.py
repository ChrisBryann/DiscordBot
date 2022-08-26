# bot.py
import os
import random
import discord
import youtube_dl
import asyncio
import webbrowser
import re
import requests
import json
from bs4 import BeautifulSoup
import giphy_client
from giphy_client.rest import ApiException
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
DANBOORU = Danbooru('danbooru')
word_headers = {
    'x-rapidapi-key': "1cbdad4150msh72e9b55eed74ad8p1fad8cjsn55ddaa3526f6",
    'x-rapidapi-host': "wordsapiv1.p.rapidapi.com"
    }
intents = discord.Intents.default()
intents.members = True
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands made by WotterMelown'
)
NOT_PRESENT = "I'm not present in any voice channel."
bot = commands.Bot(command_prefix=['yen ', 'Yen '], intents=intents, help_command=help_command)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('use yen for prefix'))
    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)
    #another way: guild = discord.utils.get(bot.guilds, name=GUILD)

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = "\n - ".join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name="general")
    lines = [
        f'Hi {member.name}, welcome to the server baby :)',
    ]
    await channel.send(
        random.choice(lines)
    )
@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.channels, name="general")
    await channel.send(f'See ya {member.name}!')

@bot.command(name="enter", help="Enter the user's voice channel")
async def join(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice:
        await ctx.send("I'm already in.")
        return

    channel = ctx.author.voice.channel

    await channel.connect()



@bot.command(name="disconnect", help="disconnect from a voice channel")
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await ctx.voice_client.disconnect()
    else:
        await ctx.send(NOT_PRESENT)

@bot.command()
async def play(ctx, *url):

        if not url:
            await ctx.send("Please provide a song title.")
            return
        url = " ".join(url)

        try:
            channel = ctx.author.voice.channel
            await channel.connect()
        except:
            await ctx.send('Currently playing. Please type "stop" to stop playing.')
            return
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'noplaylist': True,
            'default_search': 'auto',
            "format": "bestaudio/best",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
        }]
        }

        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            if "https" in url:
                info = ydl.extract_info(url, download=False)

            else:
                info = ydl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]

            title = info['title']
            info = info['url']
        voice.play(discord.FFmpegPCMAudio(info, **FFMPEG_OPTIONS))
        await ctx.send(f"**Now Playing**: {title}")

        while voice.is_playing() or voice.is_paused():  # Checks if voice is playing
            await asyncio.sleep(1)  # While it's playing it sleeps for 1 second
        else:
            await asyncio.sleep(3)  # If it's not playing it waits 15 seconds
            while voice.is_playing() or voice.is_paused():  # and checks once again if the bot is not playing
                break  # if it's playing it breaks
            else:
                await voice.disconnect()

@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice:
        await ctx.send(NOT_PRESENT)
    elif voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Music is already paused.")

@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice:
        await ctx.send(NOT_PRESENT)
    elif voice.is_paused():
        voice.resume()
    else:
        await ctx.send("Music is already playing.")

@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        voice.stop()
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I'm not present in any voice channel.")

@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx):
    dice = str(random.choice(range(1,8)))
    if dice == '7':
        await ctx.send("You are very lucky!")
    else:
        await ctx.send("You got " + dice + "!")

@bot.command(name='create-channel', help="Creates new channel (only admin allowed)")
@commands.has_role('admin')
async def create_channel(ctx, channel_name='real-python'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)



@bot.command(help="Shows gif, leave blank for random gif or specificy keyword")
async def gif(ctx, *q):

    api_key = 'dVz0BwTa4VCUOTBXrDJqKtuzzLqFmYWe'
    api_instance = giphy_client.DefaultApi()

    try:
        if not q:
            api_response = api_instance.gifs_random_get(api_key)
            await ctx.send(api_response.data.image_url)
        else:
            q = " ".join(q)
            api_response = api_instance.gifs_search_get(api_key, q, limit=5)
            aList = list(api_response.data)
            gif = random.choice(aList)
            await ctx.send(gif.embed_url)

    except ApiException as e:
        print('Exception when calling Api')

@bot.command(help='Shows temperature and weather description of Surabaya')
async def weather(ctx, *city):

    if not city:
        page = requests.get('https://api.openweathermap.org/data/2.5/weather?q=Surabaya,ID-JI&units=metric&appid=149cb83a7a2314da84bbe7f857867adb')
        resultDict = page.json()

        await ctx.send(f'Current temperature of Surabaya: {resultDict["main"]["temp"]} degrees Celcius')
        await ctx.send(f'Weather description: {resultDict["weather"][0]["description"]}')
    else:
        city = ' '.join(city)
        page = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=149cb83a7a2314da84bbe7f857867adb')
        resultDict = page.json()

        await ctx.send(f'Current temperature of {city.title()}: {resultDict["main"]["temp"]} degrees Celcius')
        await ctx.send(f'Weather description: {resultDict["weather"][0]["description"]}')

@bot.command()
async def dict(ctx, *word):
    if word:
        words = '%20'.join(word)
        word = ' '.join(word)
        page = requests.request("GET", f"https://wordsapiv1.p.rapidapi.com/words/{words}", headers=word_headers)
        resultDict = page.json()

        try:
            syllables = '-'.join(resultDict['syllables']['list'])
        except:
            syllables = None
        await ctx.send(f'Word: **{word.title()}**')
        for i, definition in enumerate(resultDict['results'], 1):
            await ctx.send(f'**{i}.** **Definition**: {definition["definition"]} ({definition["partOfSpeech"]})')
            await ctx.send(f'**Synonyms**: {", ".join(definition["synonyms"])}')

        if syllables:
            await ctx.send(f'**Syllables**: {syllables}')

    else:
        await ctx.send('Please provide a word to describe.')
        return

@bot.command()
async def love(ctx, *name):
    fname = name[0]
    sname = name[1]

    url = "https://love-calculator.p.rapidapi.com/getPercentage"

    querystring = {"fname": fname, "sname": sname}

    headers = {
        'x-rapidapi-key': "1cbdad4150msh72e9b55eed74ad8p1fad8cjsn55ddaa3526f6",
        'x-rapidapi-host': "love-calculator.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    page = response.json()
    embed = discord.Embed(title=f'{fname.title()} x {sname.title()}', color=discord.Color.purple(), description=f'Your love compability is: {page["percentage"]}%')
    embed.add_field(name='Advice of the Day', value=page['result'])

    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN)
# bot.py
import os
import random
import discord
import youtube_dl
import asyncio
import webbrowser
import re
import giphy_client
from giphy_client.rest import ApiException
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands made by WotterMelown'
)
bot = commands.Bot(command_prefix='yen ', intents=intents, help_command=help_command)


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
        f'Oh look, {member.name} is here. Fucking bitch.'
        f'Welcome to Lil Family {member.name}, motherfucker.',
        f'Konichiwa {member.name}! Ochinchin daisuki!',
        f"Hello {member.name}! You’re the reason God created the middle finger.",
        f"Hello {member.name}! You’re a grey sprinkle on a rainbow cupcake.",
        f"Hello {member.name}! If your brain was dynamite, there wouldn’t be enough to blow your hat off.",
        f"Hello {member.name}! You are more disappointing than an unsalted pretzel.",
        f"Hello {member.name}! Light travels faster than sound which is why you seemed bright until you spoke.",
        f"Hello {member.name}! We were happily married for one month, but unfortunately we’ve been married for 10 years.",
        f"Hello {member.name}! Your kid is so annoying, he makes his Happy Meal cry.",
        f"Hello {member.name}! You have so many gaps in your teeth it looks like your tongue is in jail.",
       f"Hello {member.name}! Your secrets are always safe with me. I never even listen when you tell me them.",
        f"Hello {member.name}! I’ll never forget the first time we met. But I’ll keep trying.",
        f"Hello {member.name}! I forgot the world revolves around you. My apologies, how silly of me.",
        f"Hello {member.name}! I only take you everywhere I go just so I don’t have to kiss you goodbye."
    ]
    await channel.send(
        random.choice(lines)
    )
@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.channels, name="general")
    await channel.send(f'See ya {member.name}!')

@bot.command(name="keneo", help="GET OVER HERE!")
async def join(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice:
        await ctx.send("Ak wes masuk masbro")
        return

    channel = ctx.author.voice.channel

    await channel.connect()
    await ctx.send('Opoo bro')



@bot.command(name="metuo", help="Nengkreo cok!")
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("Aku gak onok ndek channel entot")

@bot.command()
async def play(ctx, *url):

        if not url:
            await ctx.send("Ndi lagune bro")
            return
        url = " ".join(url)

        channel = ctx.author.voice.channel
        if not channel:
            await channel.connect()

        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            await ctx.send('sek')
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
            await asyncio.sleep(15)  # If it's not playing it waits 15 seconds
            while voice.is_playing() or voice.is_paused():  # and checks once again if the bot is not playing
                break  # if it's playing it breaks
            else:
                await voice.disconnect()

@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice:
        await ctx.send("Aku gak onok ndek channel entot")
    elif voice.is_playing():
        voice.pause()
    else:
        await ctx.send("wes tak pause asem")

@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice:
        await ctx.send("Aku gak onok ndek channel entot")
    elif voice.is_paused():
        voice.resume()
    else:
        await ctx.send("woi! suarane ws jalan anjengg")

@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        voice.stop()
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("Aku gak onok ndek channel entot")

@bot.command(name='kimochi', help="Responds with a loud cry of sexual tensions")
async def kimochi(ctx):
    kimochi = [
        'Daisuki!',
        'Yamete!',
        'Senpai!',
        'Oka-san!',
        'Onii-san yamete kudasai!'
    ]

    response = random.choice(kimochi)
    await ctx.send(response)
    
@bot.command(name='fuck', help='nah fam')
async def no_u(ctx):
    await ctx.send("no u.")

@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx):
    dice = str(random.choice(range(1,8)))
    if dice == '7':
        await ctx.send("You got william'ed!")
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

@bot.command(help="Ya want some sauce?")
async def sauce(ctx):
    number = str(random.choice(range(100000, 360001)))
    await ctx.send(f'Here honey {number}')
    await ctx.send(embed=discord.Embed(url=f'https://nhentai.net/g/{number}'))

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


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN)
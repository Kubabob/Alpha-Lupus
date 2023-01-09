# bot.py

#emojis:
#✅

regulamin = """
§1.1 Szanuj innych.
§1.2 Jeśli masz problem NIE bój się zapytać, po to tu jesteśmy 😉.
§1.3 Staraj się pisać na kanałach tematycznych, jeśli nie wiesz gdzie powinien znaleźć się twój problem napisz na ogólnym.
§1.4 Nie ma głupich pytań.
§1.5 Żaden język programowania nie jest gorszy od innych.
§1.6 Zakaz przeklinania na kanałach tekstowych, jeżeli naprawdę musisz, to cenzuruj, ale nie nadużywaj przekleństw;
§1.7 Zakaz wykorzystywania, oszukiwania i szantażowania innych użytkowników;
§1.8 Zakaz reklamowania jakichkolwiek serwerów, stron itp. bez zgody administracji.
"""

import os
import discord
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands
from dotenv import load_dotenv
import aiohttp
import random as r
from itertools import cycle
import time
import asyncio
import requests
from bs4 import BeautifulSoup

#openai.api_key = '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'

#ZAŁADOWANIE TOKENÓW Z .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


#NADANIE BOTOWI INTENT(PRAWA)
intents = discord.Intents.all()


#UTWORZENIE BOTA
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

#tree = app_commands.CommandTree(bot)


#ID GILDII
guild_id = 1046717079249768519


#ID KANAŁÓW
przywitanie_id = 1046717746211209267
regulamin_id = 1046725335422599208
admin_channel_id = 1046725335422599209
ogloszenia_id = 1046725510232809572
admin_bot_id = 1060904715065495552

bot_status = cycle(['!help', 'KNALT', 'Smacznej Kawusi'])
@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(bot_status)))


@tasks.loop(minutes=5)
async def ps_get_info():
    guild = bot.get_guild(guild_id)

    login_url = 'https://ps.ug.edu.pl/login.web'

    payload = {
        'licznik' : 's',
        'login' : '285665',
        'pass' : 'Szotland12'
    }

    response = requests.Session()
    web_html = response.post(login_url, data=payload).text
    parsed_html = BeautifulSoup(web_html, 'html.parser')
    ogloszenia_ilosc = parsed_html.find(id='ilNieprzeczytanychOgloszen').text

    for channel in guild.channels:
        if channel.id == ogloszenia_id:
            if ogloszenia_ilosc != '0' and czy_wyslano == False:
                await channel.send(f'Na portalu studenta czeka na nas {ogloszenia_ilosc} ogłoszeń\n'
                                f'https://ps.ug.edu.pl/login.web')
                czy_wyslano = True
            elif ogloszenia_ilosc != '0':
                czy_wyslano = False
                #print('Brak nowych ogłoszeń')

        
'''@tree.command(name='TreeTest', description='Test drzewa komenda', guild=discord.object(guild_id))
async def DrzewoTest(interaction):
    await interaction.response.send_message('TestTree')'''


#ROZPOCZĘCIE DZIAŁANIA BOTA
@bot.event
async def on_ready():

    guild = bot.get_guild(guild_id)

    roles = []
    for role in guild.roles:
        roles.append(role.name)
    
    print(f'{bot.user.name} zawył!')
    print(f'członkowie: {[member.name for member in guild.members]}\nilość członkow: {guild.member_count}')
    print(f'role: {roles}')
    change_status.start()
    ps_get_info.start()

    #await tree.sync(guild=discord.object(guild_id))

       
#PRZYŁĄCZENIE CZŁONKA
@bot.event
async def on_member_join(member):
    guild = bot.get_guild(guild_id)

    for channel in guild.channels:
        if channel.id == przywitanie_id:
            await channel.send(
                f'Witaj {member.mention} na KN ALT!\n'
                f'Nie zapomnij o zapoznaniu się z zasadami!\n'
                f'Zaznacz ✅ i baw się dobrze!'
                )


#USUNIĘCIE CZŁONKA
@bot.event
async def on_member_remove(member):
    guild = bot.get_guild(guild_id)

    for channel in guild.channels:
        if channel.id == przywitanie_id:
            await channel.send(
                f'Będzie nam Cię brakowało {member.mention} :cry:'
                )
            await tasks.asyncio.sleep(5)
            await channel.send(
                f'Anyway'
            )


#NADANIE RANGI CZŁONEK PRZEZ REGULAMIN
@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    rola_czlonek = discord.utils.get(payload.member.guild.roles, name='Czlonek')

    if payload.channel_id != regulamin_id:
        return

    print(f'{str(payload.emoji)}')
    if str(payload.emoji) == '✅':
        await payload.member.add_roles(rola_czlonek)


#HELP @EVERYONE
@bot.command()
async def help(ctx):
    help_embed = discord.Embed(color=discord.Colour.purple())

    help_embed.set_author(name='!help')
    help_embed.add_field(
        name='!ping',
        value='Grasz w pingla z botem',
        inline=False
        )
    help_embed.add_field(
        name='!dog',
        value='Pokazuje pieska',
        inline=False
        )
    help_embed.add_field(
        name='!cat',
        value='Pokazuje kotka',
        inline=False
    )
    help_embed.add_field(
        name='!echo [co chcesz żebym powiedział]',
        value='Daj mi coś powiedzieć',
        inline=False
    )
    help_embed.add_field(
        name='!rps lub !rock_paper_scissors lub !pkn',
        value='Papier/Kamien/Norzyce => Kamień, Papier, Nożyce z botem',
        inline=False
    )
    help_embed.add_field(
        name='!rock',
        value='Kamień',
        inline=False
    )
    help_embed.add_field(
        name='!paper',
        value='Papier',
        inline=False
    )
    help_embed.add_field(
        name="!scissors",
        value='Nożyce',
        inline=False
    )
    help_embed.add_field(
        name='!moneta lub !rm',
        value='Rzut monetą',
        inline=False
    )
    help_embed.add_field(
        name='!roll lub !r [[ilość_kostek]d[ilość_ścianek]]',
        value='Rzut kostką',
        inline=False
    )
    

    await ctx.channel.send(embed=help_embed)


#HELP @ADMIN
@bot.command(pass_context=True)
async def help_admin(ctx):
    admin_channel = bot.get_channel(admin_channel_id)

    help_admin_embed = discord.Embed(color=discord.Colour.purple())

    help_admin_embed.set_author(name='!help_admin')
    help_admin_embed.add_field(
        name='!regulamin_maker',
        value='Służy do stworzenia regulaminu'
        )

    await admin_channel.send(embed=help_admin_embed)


#TWORZENIE REGULAMINU
@bot.command()
@commands.has_permissions(manage_channels=True)
async def regulamin_maker(ctx):
    await ctx.message.delete()
    regulamin_message = await ctx.channel.send(regulamin)
    await regulamin_message.add_reaction('✅')


#ERROR DO TWORZENIA REGULAMINU
@regulamin_maker.error
async def regulamin_maker_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        error_text = f'''Nie masz uprawnień do komendy "regulamin_maker"'''
        await ctx.channel.send(error_text)


'''@bot.command(pass_context = True)
async def clear(ctx):
    print(f'{ctx.channel_id}')
    await ctx.channel.delete_messages(ctx.channel.messages)
    '''

#GRA W PING PONGA
@bot.command()
async def ping(ctx):
    await ctx.channel.send("pong :ping_pong:")


#BOT PISZE TO CO TY
@bot.command()
async def echo(ctx, *text):
    final_text = ' '.join(*text)
    await ctx.channel.send(final_text)


#BOT WYSWIETLA LOSOWEGO KOTA
@bot.command()
async def cat(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://aws.random.cat/meow') as r:
            if r.status == 200:
                js = await r.json()
                await ctx.channel.send(js['file'])


#BOT WYSWIETLA LOSOWEGO PSA
@bot.command()
async def dog(ctx):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://random.dog/woof.json') as r:
            if r.status == 200:
                js = await r.json()
                await ctx.channel.send(js['url'])

#cute - animal


def rps_random():
    moves = ['ROCK', 'PAPER', 'SCISSORS']
    return r.choice(moves)

def rps_game(player, bot):
    if player == bot:
        return "Tie"
    elif player == 'ROCK':
        if bot == 'PAPER':
            return 'Lose'
        else:
            return 'Win'
    elif player == 'PAPER':
        if bot == 'SCISSORS':
            return 'Lose'
        else:
            return 'Win'
    elif player == 'SCISSORS':
        if bot == 'ROCK':
            return 'Lose'
        else:
            return 'Win'
    else:
        return 'error'

@bot.command()
async def rock(ctx):
    bot=rps_random()
    wynik = rps_game(player='ROCK', bot=bot)
    if wynik == 'Tie':
        await ctx.channel.send(bot)
        await tasks.asyncio.sleep(1)
        await ctx.channel.send('Remis! Spróbujmy jeszcze raz!')
    elif wynik == 'Lose':
        await ctx.channel.send(bot)
        await tasks.asyncio.sleep(1)
        await ctx.channel.send('Przegrałeś, życzę więcej szczęścia następnym razem :wink:')
    else:
        await ctx.channel.send(bot)
        await tasks.asyncio.sleep(1)
        await ctx.channel.send('Wygrałeś!')
        await tasks.asyncio.sleep(1)
        await ctx.channel.send('Tym razem :upside_down:')

@bot.command()
async def paper(ctx):
    bot=rps_random()
    wynik = rps_game(player='PAPER', bot=bot)
    if wynik == 'Tie':
        await ctx.channel.send(bot)
        await tasks.asyncio.sleep(1)
        await ctx.channel.send('Remis! Spróbujmy jeszcze raz!')
    elif wynik == 'Lose':
        await ctx.channel.send(bot)
        await tasks.asyncio.sleep(1)
        await ctx.channel.send('Przegrałeś, życzę więcej szczęścia następnym razem :wink:')
    else:
        await ctx.channel.send(bot)
        await tasks.asyncio.sleep(1)
        await ctx.channel.send('Wygrałeś!')
        await tasks.asyncio.sleep(1)
        await ctx.channel.send('Tym razem :upside_down:')

@bot.command()
async def scissors(ctx):
    bot=rps_random()
    wynik = rps_game(player='SCISSORS', bot=bot)
    if wynik == 'Tie':
        await ctx.channel.send(bot)
        await tasks.asyncio.sleep(1)
        await ctx.channel.send('Remis! Spróbujmy jeszcze raz!')
    elif wynik == 'Lose':
        await ctx.channel.send(bot)
        await tasks.asyncio.sleep(1)
        await ctx.channel.send('Przegrałeś, życzę więcej szczęścia następnym razem :wink:')
    else:
        await ctx.channel.send(bot)
        await tasks.asyncio.sleep(1)
        await ctx.channel.send('Wygrałeś!')
        await tasks.asyncio.sleep(1)
        await ctx.channel.send('Tym razem :upside_down:')

@bot.command()
async def chat(ctx, *args):
    prompt = ' '.join(args)
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5
    )
    await ctx.message.channel.send(response.get("text"))

@bot.command(aliases=['rps', 'pkn'])
async def rock_paper_scissors(ctx, usr_msg: str):
    usr_msg = usr_msg.lower()
    if usr_msg == 'kamień':
        usr_msg = 'kamien'
    elif usr_msg == 'nożyce':
        usr_msg = 'nozyce'

    opcje = ['papier', 'kamien', 'nozyce']
    losowanko = r.choice(opcje)

    if usr_msg == losowanko:
        await ctx.send(f'{losowanko.upper()}!\nAjaj, remis. Jeszcze raz?')
    elif usr_msg == 'kamien':
        if losowanko == 'papier':
            await ctx.send(f'{losowanko.upper()}!\nWygrałeeem! Nooob ahhahahahxXDDXDXdxD11!1!!!1')
        else:
            await ctx.send(f'{losowanko.upper()}!\nNieeee...! Pokonałeś mnie :CCCC')
    elif usr_msg == 'papier':
        if losowanko == 'nozyce':
            await ctx.send(f'{losowanko.upper()}!\nWygrałeeem! Nooob ahhahahahxXDDXDXdxD11!1!!!1')
        else:
            await ctx.send(f'{losowanko.upper()}!\nNieeee...! Pokonałeś mnie :CCCC')
    elif usr_msg == 'nozyce':
        if losowanko == 'kamien':
            await ctx.send(f'{losowanko.upper()}!\nWygrałeeem! Nooob ahhahahahxXDDXDXdxD11!1!!!1')
        else:
            await ctx.send(f'{losowanko.upper()}!\nNieeee...! Pokonałeś mnie :CCCC')
    else:
        await ctx.send('Umiesz pisać???')

@bot.command(aliases=['r'])
async def roll(ctx, throw: str):
    times, dice = map(int, throw.split('d'))
    if dice > 100:
        if times > 200:
            await ctx.send('Mam tylko 200 kości!\nA największa kostka to d100')
        else:
            await ctx.send('Największa kostka to d100!')
    elif times > 200:
        await ctx.send(f'Mam tylko 200 kostek d{dice}!')
    else:
        rolls = [r.randint(1, dice) for i in range(times)]
        odp = ''
        last_roll = rolls.pop(-1)
        try:
            for i in range(-1, times):
                odp += f'{str(rolls[i+1])}, '
        except Exception:
            odp += f'{last_roll}\nSuma wynosi: {sum(rolls) + last_roll}'

    
        await ctx.send(odp)
        rolls.append(last_roll)
        await ctx.send(f'Najwyższa wartość: {max(rolls)}')

@bot.command(aliases=['rm'])
async def moneta(ctx):
    moneta = r.randint(0, 1)
    if moneta == 0:
        await ctx.channel.send('ORZEŁ')
    else:
        await ctx.channel.send('RESZKA')



#URUCHOMIENIE BOTA
bot.run(TOKEN)

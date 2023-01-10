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
bot = commands.Bot(command_prefix='/', intents=intents)
bot.remove_command('help')


#ID GILDII
guild_id = 1046717079249768519


#ID KANAŁÓW
przywitanie_id = 1046717746211209267
regulamin_id = 1046725335422599208
admin_channel_id = 1046725335422599209
ogloszenia_id = 1046725510232809572
admin_bot_id = 1060904715065495552


bot_status = cycle(['/help', 'KNALT', 'Smacznej Kawusi'])
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

    await bot.tree.sync()

       
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


@bot.tree.command(name='help', description='/help [komenda]')
async def help(interaction: discord.Interaction, komenda : str = 'all'):
    if komenda == 'all':
        help_embed = discord.Embed(color=discord.Colour.purple())

        help_embed.set_author(name='/help')
        help_embed.add_field(
            name='/ping',
            value='Grasz w pingla z botem',
            inline=False
            )
        help_embed.add_field(
            name='/dog',
            value='Pokazuje pieska',
            inline=False
            )
        help_embed.add_field(
            name='/cat',
            value='Pokazuje kotka',
            inline=False
        )
        help_embed.add_field(
            name='/echo [co chcesz żebym powiedział]',
            value='Daj mi coś powiedzieć',
            inline=False
        )
        help_embed.add_field(
            name='/rps [papier/kamien/nożyce] lub /rock_paper_scissors lub /pkn',
            value='Papier/Kamien/Nozyce => Kamień, Papier, Nożyce z botem',
            inline=False
        )
        help_embed.add_field(
            name='/rock',
            value='Kamień',
            inline=False
        )
        help_embed.add_field(
            name='/paper',
            value='Papier',
            inline=False
        )
        help_embed.add_field(
            name="/scissors",
            value='Nożyce',
            inline=False
        )
        help_embed.add_field(
            name='/moneta lub /rm',
            value='Rzut monetą',
            inline=False
        )
        help_embed.add_field(
            name='/roll lub /r [ilość_kostek] [ilość_ścianek]',
            value='Rzut kostką',
            inline=False
        )
        await interaction.response.send_message(embed=help_embed, ephemeral=True)
    elif komenda == 'ping':
        await interaction.response.send_message(f'Zagraj w ping ponga z botem', ephemeral=True)
    elif komenda == 'dog':
        await interaction.response.send_message(f'Pokazuje pieska', ephemeral=True)
    elif komenda == 'cat':
        await interaction.response.send_message(f'Pokazuje kotka', ephemeral=True)
    elif komenda == 'echo':
        await interaction.response.send_message(f'/echo [co chcesz żeby bot napisał]', ephemeral=True)
    elif komenda == 'rps':
        await interaction.response.send_message(f'/rps [papier/kamien/nożyce\nZagraj z botem w papier kamień nożyce', ephemeral=True)
    elif komenda == 'rock':
        await interaction.response.send_message(f'Rzucasz kamień', ephemeral=True)
    elif komenda == 'paper':
        await interaction.response.send_message(f'Pokazujesz papier', ephemeral=True)
    elif komenda == 'scissors':
        await interaction.response.send_message(f'Wyjmujesz nożyce', ephemeral=True)
    elif komenda == 'moneta' or komenda == 'rm':
        await interaction.response.send_message(f'Rzut monetą', ephemeral=True)
    elif komenda == 'roll' or komenda == 'r':
        await interaction.response.send_message(f'/r [ilość_kostek] [ilość_ścianek]', ephemeral=True)
    else:
        await interaction.response.send_message(f'Nie znam takiej komendy', ephemeral=True)

#HELP @ADMIN
@bot.tree.command(name='help_admin', description='/help_admin [komenda]')
@commands.has_permissions(manage_channels=True)
async def help_admin(interaction: discord.Interaction, komenda : str = 'all'):
    

    if komenda == 'all':
        help_admin_embed = discord.Embed(color=discord.Colour.purple())

        help_admin_embed.set_author(name='/help_admin')
        help_admin_embed.add_field(
        name='/regulamin_maker',
        value='Służy do stworzenia regulaminu'
        )
        await interaction.response.send_message(embed=help_admin_embed, ephemeral=True)
    elif komenda == 'regulamin_maker':
        await interaction.response.send_message(f'Służy do stworzenia regulaminu', ephemeral=True)
    else:
        await interaction.response.send_message(f'Nie znam takiej komendy', ephemeral=True)


#TWORZENIE REGULAMINU
@bot.tree.command(name='regulamin_maker', description='Słuzy do stworzenia regulaminu')
@commands.has_permissions(manage_channels=True)
async def regulamin_maker(interaction: discord.Interaction):
    regulamin_message = await interaction.channel.send(regulamin)
    await regulamin_message.add_reaction('✅')


#ERROR DO TWORZENIA REGULAMINU
@regulamin_maker.error
async def regulamin_maker_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        error_text = f'''Nie masz uprawnień do komendy "regulamin_maker"'''
        await ctx.channel.send(error_text)


'''@bot.komenda(pass_context = True)
async def clear(ctx):
    print(f'{ctx.channel_id}')
    await ctx.channel.delete_messages(ctx.channel.messages)
    '''

#GRA W PING PONGA
@bot.tree.command(name='ping', description='zwraca PONG')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("pong :ping_pong:")

@bot.tree.command(name='slash', description='test')
async def slash(interaction: discord.Interaction, number: int, string: str):
    await interaction.response.send_message(f'Modify {number=} {string=}', ephemeral=True)


#BOT PISZE TO CO TY
@bot.tree.command(name='echo', description='Zmuś bota do napisania czegoś')
async def echo(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(f'{text}')


#BOT WYSWIETLA LOSOWEGO KOTA
@bot.tree.command(name='kot', description='Pokazuje kota')
async def kot(interaction: discord.Interaction):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://aws.random.cat/meow') as r:
            if r.status == 200:
                js = await r.json()
                await interaction.response.send_message(js['file'])


#BOT WYSWIETLA LOSOWEGO PSA
@bot.tree.command(name='pies', description='Pokazuje psa')
async def pies(interaction: discord.Interaction):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://random.dog/woof.json') as r:
            if r.status == 200:
                js = await r.json()
                await interaction.response.send_message(js['url'])

#cute - animal


def rps_random():
    moves = ['KAMIEN', 'PAPIER', 'NOZYCE']
    return r.choice(moves)

def rps_game(player, bot):
    if player == bot:
        return "Tie"
    elif player == 'KAMIEN':
        if bot == 'PAPIER':
            return 'Lose'
        else:
            return 'Win'
    elif player == 'PAPIER':
        if bot == 'NOZYCE':
            return 'Lose'
        else:
            return 'Win'
    elif player == 'NOZYCE':
        if bot == 'KAMIEN':
            return 'Lose'
        else:
            return 'Win'
    else:
        return 'error'

@bot.tree.command(name='kamień', description='Rzucasz kamień')
async def kamień(interaction: discord.Interaction):
    bot=rps_random()
    wynik = rps_game(player='ROCK', bot=bot)
    if wynik == 'Tie':
        await interaction.response.send_message(f'{bot}\nRemis! Spróbujmy jeszcze raz!', ephemeral=True)
    elif wynik == 'Lose':
        await interaction.response.send_message(f'{bot}\nPrzegrałeś, życzę więcej szczęścia następnym razem :wink:', ephemeral=True)
    else:
        await interaction.response.send_message(f'{bot}\nWygrałeś!', ephemeral=True)
        await tasks.asyncio.sleep(1)
        await interaction.channel.send('Tym razem :upside_down:', ephemeral=True)

@bot.tree.command(name='papier', description='Pokazujesz papier')
async def papier(interaction: discord.Interaction):
    bot=rps_random()
    wynik = rps_game(player='PAPIER', bot=bot)
    if wynik == 'Tie':
        await interaction.response.send_message(f'{bot}\nRemis! Spróbujmy jeszcze raz!', ephemeral=True)
    elif wynik == 'Lose':
        await interaction.response.send_message(f'{bot}\nPrzegrałeś, życzę więcej szczęścia następnym razem :wink:', ephemeral=True)
    else:
        await interaction.response.send_message(f'{bot}\nWygrałeś!', ephemeral=True)
        await tasks.asyncio.sleep(1)
        await interaction.channel.send('Tym razem :upside_down:', ephemeral=True)

@bot.tree.command(name='nozyce', description='Wyjmujesz nozyce')
async def nozyce(interaction: discord.Interaction):
    bot=rps_random()
    wynik = rps_game(player='NOZYCE', bot=bot)
    if wynik == 'Tie':
        await interaction.response.send_message(f'{bot}\nRemis! Spróbujmy jeszcze raz!', ephemeral=True)
    elif wynik == 'Lose':
        await interaction.response.send_message(f'{bot}\nPrzegrałeś, życzę więcej szczęścia następnym razem :wink:', ephemeral=True)
    else:
        await interaction.response.send_message(f'{bot}\nWygrałeś!', ephemeral=True)
        await tasks.asyncio.sleep(1)
        await interaction.channel.send('Tym razem :upside_down:', ephemeral=True)

'''@bot.komenda()
async def chat(ctx, *args):
    prompt = ' '.join(args)
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5
    )
    await ctx.message.channel.send(response.get("text"))'''

@bot.tree.command(name='rps', description='Zagraj w papier kamień nozyce')
async def rps(interaction: discord.Interaction, wybor: str):
    wybor = wybor.lower()
    if wybor == 'kamień':
        wybor = 'kamien'
    elif wybor == 'nożyce':
        wybor = 'nozyce'

    opcje = ['papier', 'kamien', 'nozyce']
    losowanko = r.choice(opcje)

    if wybor == losowanko:
        await interaction.response.send_message(f'{losowanko.upper()}!\nAjaj, remis. Jeszcze raz?', ephemeral=True)
    elif wybor == 'kamien':
        if losowanko == 'papier':
            await interaction.response.send_message(f'{losowanko.upper()}!\nWygrałeeem! Nooob ahhahahahxXDDXDXdxD11!1!!!1', ephemeral=True)
        else:
            await interaction.response.send_message(f'{losowanko.upper()}!\nNieeee...! Pokonałeś mnie :CCCC', ephemeral=True)
    elif wybor == 'papier':
        if losowanko == 'nozyce':
            await interaction.response.send_message(f'{losowanko.upper()}!\nWygrałeeem! Nooob ahhahahahxXDDXDXdxD11!1!!!1', ephemeral=True)
        else:
            await interaction.response.send_message(f'{losowanko.upper()}!\nNieeee...! Pokonałeś mnie :CCCC', ephemeral=True)
    elif wybor == 'nozyce':
        if losowanko == 'kamien':
            await interaction.response.send_message(f'{losowanko.upper()}!\nWygrałeeem! Nooob ahhahahahxXDDXDXdxD11!1!!!1', ephemeral=True)
        else:
            await interaction.response.send_message(f'{losowanko.upper()}!\nNieeee...! Pokonałeś mnie :CCCC', ephemeral=True)
    else:
        await interaction.response.send_message('Umiesz pisać???', ephemeral=True)

@bot.tree.command(name='roll', description='Rzuć x kostkami y ściennymi')
async def roll(interaction: discord.Interaction, kostki: int, scianki: int):
    if scianki > 100:
        if kostki > 200:
            await interaction.response.send_message('Mam tylko 200 kości!\nA największa kostka to d100', ephemeral=True)
        else:
            await interaction.response.send_message('Największa kostka to d100!', ephemeral=True)
    elif kostki > 200:
        await interaction.response.send_message(f'Mam tylko 200 kostek d{scianki}!', ephemeral=True)
    else:
        rolls = [r.randint(1, scianki) for i in range(kostki)]
        odp = ''
        last_roll = rolls.pop(-1)
        try:
            for i in range(-1, kostki):
                odp += f'{str(rolls[i+1])}, '
        except Exception:
            odp += f'{last_roll}\nSuma wynosi: {sum(rolls) + last_roll}'

        rolls.append(last_roll)
    
        await interaction.response.send_message(
            f'{odp}\n'
            f'Najwyższa wartość: {max(rolls)}', ephemeral=True)

@bot.tree.command(name='moneta', description='Rzut monetą')
async def moneta(interaction: discord.Interaction):
    moneta = r.randint(0, 1)
    if moneta == 0:
        await interaction.response.send_message('ORZEŁ', ephemeral=True)
    else:
        await interaction.response.send_message('RESZKA', ephemeral=True)


#URUCHOMIENIE BOTA
bot.run(TOKEN)

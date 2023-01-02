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

#ZAŁADOWANIE TOKENÓW Z .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#NADANIE BOTOWI INTENT(PRAWA)
intents = discord.Intents.all()

#UTWORZENIE BOTA
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

#ID GILDII
guild_id = 1058493924089548810

#ID KANAŁÓW
przywitanie_id = 1058535484344766474
regulamin_id = 1058543121824227389
admin_channel_id = 1059491305522221086

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
    
#GRA W PING PONGA
@bot.command()
async def ping(ctx):
    await ctx.channel.send("pong :ping_pong:")

#HELP @EVERYONE
@bot.command()
async def help(ctx):
    help_embed = discord.Embed(color=discord.Colour.purple())

    help_embed.set_author(name='!help')
    help_embed.add_field(
        name='!ping',
        value='Grasz w pingla z botem',
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


#URUCHOMIENIE BOTA
bot.run(TOKEN)

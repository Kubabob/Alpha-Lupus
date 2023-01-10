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

from ast import Await, alias
from asyncio import events
from cgi import test
from copyreg import add_extension
from datetime import datetime, timedelta
from dis import disco
from email import message
from email.errors import MessageError
from http import client
from mimetypes import init
from multiprocessing import Event
from multiprocessing.connection import wait
from random import getstate, random
from secrets import choice
from shutil import which
from site import PREFIXES
from sqlite3 import Timestamp
from sys import prefix
import time
from tkinter.messagebox import NO
from alive_progress import alive_bar
import discord
import aiosqlite
import random
import asyncio
from discord.ext import commands,tasks
from itertools import cycle
import json
import os
import requests
from discord import Intents
from discord import Streaming
from discord.utils import get
from pypresence import Presence



############# Inicialização ##############################



intents = discord.Intents(messages=True,guilds=True,reactions=True,members=True,presences=True)
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), intents=intents)
intents = True




@bot.event ## Info Bot Online
async def on_ready():
##### função do level #####
  setattr(bot, "db", await aiosqlite.connect("levels.db")) #nome banco de dados 
  await asyncio.sleep(3)
  async with bot.db.cursor() as cursor:  #tabelas para serem criadas 
    await cursor.execute("CREATE TABLE IF NOT EXISTS levels (level INTEGER, xp INTEGER, user INTEGER, guild INTEGER)")
    await cursor.execute("CREATE TABLE IF NOT EXISTS levelSettings (levelsys BOOL, role INTEGER, levelreq INTEGER, guild INTEGER)")
      #tabelas para serem criadas

    print("Banco de Dados levels Conectado")


      
######## Fim func level #######



######### Func barra de att #####
  for i in range(0): 
    with alive_bar(100, ctrl_c=False, title=f'Atualização {i}') as bar:
        for i in range(100):
            time.sleep(0.02)
            bar()
########## Fimm func barra #####


######## inicializações texto ####
  print("\n")   
  #change_status.start()
  print(f'Bot Online')
  print("\n")   
  print('Feito Por SkillOnex e Benvenutti')
  print("\n")   
  print(f"Logado em  {bot.user}")
  print("\n")   
  #bot.get_chaneel(id do canal pra mandar a msg automatica)
  channel = bot.get_channel(123)
  await channel.send("Entou pronto para trabalhar!")


@bot.event
async def ch_pr():
  await bot.wait_until_ready()

  statues = [f"Em Desenvolvimento", f"Ativo em  {len(bot.guilds)} Servers / !userhelp ","SkillOnex & Benvenutti"] #msg de status do bot
  
  while not bot.is_closed():

    status = random.choice(statues)
    

    await bot.change_presence(activity=discord.Game(name=status))

    await asyncio.sleep(10)

bot.loop.create_task(ch_pr())



##################### Fim Inicialização #####################






############################ Eventos ####################################

@bot.event ##Membro entou no Servidor 
async def on_member_join(member):

  #name = nome da tag no discord 
  autorole = discord.utils.get(member.guild.roles, name='membro') ##Tag quando entra de membro
  await member.add_roles(autorole)
  print(f'{member} Entrou e ganhou a tag de {autorole}')

  
  #bot.get_chaneel(id do canal pra mandar a msg automatica)
  channel = bot.get_channel(123)
  embed = discord.Embed(
        title = f"Seja bem vindo {member}",
        description = 'Descanse aqui viajante cansado !',
        color = member.color
    )
  embed.set_footer(text=f'Você recebeu a tag de @{autorole}')
  embed.set_image(url='https://i.kym-cdn.com/photos/images/newsfeed/002/336/753/653.gif')
  embed.set_thumbnail(url=member.avatar_url)
  embed.set_author(name=member,icon_url='https://www.tibiawiki.com.br/images/7/7c/Fire_Field.gif')
  await channel.send(embed=embed)



@bot.event ##Membro Saiu no Servidor 
async def on_member_remove(member):
  autorole = discord.utils.get(member.guild.roles, name='membro') ##Tag quando entra de membro
  print(f'{member} Saiu do Servidor {member.guild}')
  autorole = discord.utils.get(member.guild.roles)

  #bot.get_chaneel(id do canal pra mandar a msg automatica)
  channel = bot.get_channel(123)
  embed = discord.Embed(
        title = f"Tenha uma Boa jornada {member} !",
        description = 'Aguardamos sua volta ',
        color = member.color
    )
  embed.set_footer(text=f'Você recebeu a tag de {autorole}')
  embed.set_image(url='http://criticalhits.com.br/wp-content/uploads/2015/10/1454745043660382759.gif')
  embed.set_thumbnail(url=member.avatar_url)
  embed.set_author(name=member,icon_url='https://www.tibiawiki.com.br/images/d/d8/Brocade_Backpack.gif')
  await channel.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound): ##Evento de Comando Não encontrado
      await ctx.send('Comando Não Encontrado!')


@bot.event ##reacão para cargo 
async def on_raw_reaction_add(payload):

  if payload.member.bot:
    pass

  else:
      with open('reactrole.json') as react_file:
        data = json.load(react_file)
        for x in data:
          if x['message_id'] == payload.message_id:  # verificar se o id do membro encontrado é igual ao da msg
            
            if x['emoji'] == payload.emoji.name:  # verifica se o emoji encontrado é igual ao emoji reagido
              role = discord.utils.get(bot.get_guild(
               payload.guild_id).roles, id=x['role_id'])

            await payload.member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload): #remover cargo na reação

    with open('reactrole.json') as react_file:
        data = json.load(react_file)
        for x in data:

            if x['message_id'] == payload.message_id:  # verificar se o id do membro encontrado é igual ao da msg
                                                        
                if x['emoji'] == payload.emoji.name:  # verificar se o emoji encontrado é igual ao emoji reagido
                    role = discord.utils.get(bot.get_guild(
                        payload.guild_id).roles, id=x['role_id'])

                
                await bot.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)
                    

############## Func/event level dos usuraios ######################
@bot.event
async def on_message(messages):
    if messages.author.bot:
        return
    author = messages.author
    guild = messages.guild
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?", (author.id, guild.id,))
        xp = await cursor.fetchone()
        await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?", (author.id, guild.id,))
        level = await cursor.fetchone()

        if not xp or not level: 
            await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)", (0, 0, author.id, guild.id,))
                
        try:
            xp = xp[0]
            level = level[0]
        except TypeError:
            xp = 0
            level = 0
        if level < 5:
            xp += random.randint(1, 10)
            await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (xp, author.id, guild.id,))
        else:
            rand = random.randint(1, (level//4))
            if rand == 1:
                xp += random.randint(1, 10)
                await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (xp, author.id, guild.id,))
        if xp >= 100:
            level += 1
            await cursor.execute("UPDATE levels SET level = ? WHERE user = ? AND guild = ?", (level, author.id, guild.id,))
            await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?", (0, author.id, guild.id,))
            await messages.channel.send(f"{author.mention} voce subiu para o nivel {level}")
            

    await bot.db.commit()
    await bot.process_commands(messages)



####################### Fim enventos ###################################




########## Canal De Comandos###############



################### commando inicio user info ###################
@bot.command()
async def userinfo(ctx,user:discord.Member=None):

    if user==None:
        user=ctx.author

    rlist = []
    for role in user.roles:
      if role.name != "@everyone":
        rlist.append(role.mention)
    b = ", ".join(rlist)
    embed = discord.Embed(colour=user.color,timestamp=ctx.message.created_at)
    embed.set_author(name=f"User Info - {user}"),
    embed.set_thumbnail(url=user.avatar_url),
    embed.set_author(name=user,icon_url='https://www.tibiawiki.com.br/images/1/12/Mandrake.gif')
    embed.set_footer(text=f'Comando usado por - {ctx.author}',
  icon_url=ctx.author.avatar_url)
    embed.add_field(name='Nome:',value=f'`{user.display_name}`',inline=False)
    embed.add_field(name='Criado em:',value=f'`{user.created_at}`',inline=False)
    embed.add_field(name='Entrou em:',value=f'`{user.joined_at}`',inline=False)
    embed.add_field(name=f'Cargos:({len(rlist)})',value=''.join([b]),inline=False)
    embed.add_field(name='Maior cargo:',value=user.top_role.mention,inline=False)

    await ctx.send(embed=embed) 


    #commands.get_channel(id do canal pra mandar a msg) 

    #log de comandos simples
    z = commands.get_channel(123)

    embed = discord.Embed(title = f"log bot", description = f"Comando !user usado por \nAuthor: {ctx.author}", timestamp = datetime.now(), color = discord.Colour.red())
    embed.set_footer(text=f'Comando usado por - {ctx.author}',icon_url=ctx.author.avatar_url)
    await z.send(embed = embed)
    #log de comandos simples

##################### Comando Rank level #############
@bot.command(aliases=['lvl', 'rank', 'r'])
async def level(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?", (member.id, ctx.guild.id,))
        xp = await cursor.fetchone()
        await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?", (member.id, ctx.guild.id,))
        level = await cursor.fetchone()

        if not xp or not level: 
            await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)", (0, 0, member.id, ctx.guild.id,))
            await bot.db.commit()
        
        try:
            xp = xp[0]
            level = level[0]
        except TypeError:
            xp = 0
            level = 0
        em = discord.Embed(title=f'{member.name} Level !', description=f"**Level**: `{level}`\n**XP**: `{xp}`", color=member.color)

        em.set_thumbnail(url=member.avatar_url),
        em.set_footer(text=f'Comando usado por - {ctx.author}',
        icon_url=ctx.author.avatar_url)
        em.add_field(name='Nome:',value=f'`{member.display_name}`',inline=False)
        em.add_field(name='Entrou em:',value=f'`{member.joined_at}`',inline=False)
        em.add_field(name='Maior cargo:',value=member.top_role.mention,inline=False)
        #em.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=em)
        c = bot.get_channel()

        #commands.get_channel(id do canal pra mandar a msg) 
        #log de comandos simples
        z = bot.get_channel(123)

        embed = discord.Embed(title = f"log bot", description = f"Comando !lvl usado por \nAuthor: {ctx.author}", timestamp = datetime.now(), color = discord.Colour.red())
        embed.set_footer(text=f'Comando usado por - {ctx.author}',icon_url=ctx.author.avatar_url)
        await z.send(embed = embed)



 ####### Fim comando Rank level ####################### 

############### Comando LeaderBoard
@bot.command(aliases=["lb","leader"])
async def leaderboard(ctx):
  async with bot.db.cursor() as cursor:
    await cursor.execute("SELECT levelsys FROM levelSettings WHERE guild = ?",(ctx.guild.id,))
    levelsys = await cursor.fetchone()
    if levelsys:
      if not levelsys[0] == 1:
        return await ctx.send("Level esta desativado")
    await cursor.execute("SELECT level,xp,user FROM levels WHERE guild = ? ORDER BY level DESC, xp DESC LIMIT 10", (ctx.guild.id,))
    data = await cursor.fetchall()
    if data:
      user=ctx.author
      em = discord.Embed(title="LeaderBoard",description="Tabela de membros mais ativos !",color=user.color,timestamp=ctx.message.created_at)
      count = 0
      for table in data:
        member = ctx.author
        count += 1

        user = ctx.guild.get_member(table[2])
        em.set_thumbnail(url="https://www.tibiawiki.com.br/images/c/c3/Tibiapedia.gif"),
        em.set_footer(text=f'Comando usado por - {ctx.author}',icon_url=ctx.author.avatar_url)
        em.add_field(name=f"{count}. {user.name} ", value=f"Level - **{table[0]}** / XP - **{table[1]}**", inline=False)
      return await ctx.send(embed=em)
      

############ Fim comando leaderboard ##################

############# Fim userinfo ##############################


####comandos verificação
@bot.command()
@commands.has_permissions(administrator=True, manage_roles=True) #permissao de adm pra criar um embed pra reacão por cargo

async def reactrole(ctx, emoji, role: discord.Role, *, message):

    emb = discord.Embed(title='Para ver os demais canais, você precisa ser Verificado!',description="Reaja com ✅ para ganhar sua tag de Verificado.",color=discord.Colour.dark_red())
    emb.set_footer(text=f"V0.1.0")
    emb.set_author(name='Verificação 🍥',icon_url='https://www.tibiawiki.com.br/images/b/bc/Receipt.gif')
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(emoji)

    with open('reactrole.json') as json_file:
        data = json.load(json_file)

        new_react_role = {'role_name': role.name, 
        'role_id': role.id,
        'emoji': emoji,
        'message_id': msg.id}

        data.append(new_react_role)

    with open('reactrole.json', 'w') as f:
        json.dump(data, f, indent=4)



######### Commando Server Info ###########
@bot.command(aliases=['svinfo','infosv','sv']) 
async def serverinfo(ctx):        
  user=ctx.author
  embed= discord.Embed(color= discord.Color(0xffff),
                       title='Server Info',
                       description=f'**Nome do Servidor** `{ctx.guild.name}`{os.linesep}**Quantos Membros** `{ctx.guild.member_count}`{os.linesep}**Dono** {ctx.guild.owner.mention}{os.linesep}')
  embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
  embed.set_footer(text=f"V0.1.0")
  embed.set_author(name=user,icon_url='https://www.tibiawiki.com.br/images/c/ce/The_Epic_Wisdom.gif')
  await ctx.send(embed=embed)

  #bot.get_channel(id canal pra mandar msg)
  #log simples de comandos
  z = bot.get_channel(123)

  embed = discord.Embed(title = f"log bot", description = f"Comando !serverinfo usado por \nAuthor: {ctx.author}", timestamp = datetime.now(), color = discord.Colour.red())
  embed.set_footer(text=f'Comando usado por - {ctx.author}',icon_url=ctx.author.avatar_url)
  await z.send(embed = embed)
  #log simples de comandos

########## comando Fim server Info #######################

@bot.command() ## Comando Ping
async def ping(ctx):
    await ctx.send(f'pong {round(bot.latency * 1000)} ms atualmente :flag_br: ')
     #bot.get_channel(id canal pra mandar msg)
     #log simples de comandos
    z = bot.get_channel(123)

    embed = discord.Embed(title = f"log bot", description = f"Comando !ping usado por \nAuthor: {ctx.author}", timestamp = datetime.now(), color = discord.Colour.red())
    embed.set_footer(text=f'Comando usado por - {ctx.author}',icon_url=ctx.author.avatar_url)
    await z.send(embed = embed)

  
######################### Mensagem embed bonitinha #####################
# @bot.command()
# @commands.has_permissions(administrator=True)

# async def mensagem(ctx,*,title,messege):
#     embed = discord.Embed(
#         title = title,
#         description = messege,
#         colour = discord.Colour.blue()
#     )

#     embed.set_footer(text="text")
#     embed.set_image(url="https://www.tibiawiki.com.br/images/c/ce/The_Epic_Wisdom.gif")
#     embed.set_thumbnail(url="https://www.tibiawiki.com.br/images/c/ce/The_Epic_Wisdom.gif")
#     embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

#     await ctx.send(embed=embed)

# desativada queria fazer com que o usuario pudesse fazer sua propia msg mas desisti 

#################################### Fim mensagem bonitinha #################







#####Comando Clear######

@bot.command()
@commands.has_permissions(administrator=True)
@commands.bot_has_permissions(administrator=True)

async def clear(ctx,amount : int): ##limpar canal
  await ctx.channel.purge(limit=amount)


  #bot.get_channel(id canal pra mandar msg)
  #log simples de comandos
  z = bot.get_channel(123)

  embed = discord.Embed(title = f"log bot", description = f"Comando !clear usado por \nAuthor: {ctx.author}", timestamp = datetime.now(), color = discord.Colour.red())
  embed.set_footer(text=f'Comando usado por - {ctx.author}',icon_url=ctx.author.avatar_url)
  await z.send(embed = embed)

@clear.error #func erro caso/caso
async def clear_error(ctx,error):
  if isinstance(error,commands.MissingRequiredArgument):
    await ctx.send('Por favor informe o numero de mensagens para serem deletadas!')
  if isinstance(error,commands.MissingPermissions):
    await ctx.send('Desclupe, você não tem permissão para ultilizar este comando.')






#####Fim Comando Clear######




#################### Comando Unban ###################################
@bot.command()
@commands.has_permissions(ban_members=True)
@commands.bot_has_permissions(ban_members=True)

async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.member_discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')


            #bot.get_channel(id canal pra mandar msg)
            #log simples de comandos
            z = bot.get_channel(123)

            embed = discord.Embed(title = f"log bot", description = f"Comando !unban usado por \nAuthor: {ctx.author}", timestamp = datetime.now(), color = discord.Colour.red())
            embed.set_footer(text=f'Comando usado por - {ctx.author}',icon_url=ctx.author.avatar_url)
            await z.send(embed = embed)


            #bot.get_channel(id canal pra mandar msg)
            #log simples de comandos
            ub = bot.get_channel(123)

            embed = discord.Embed(title = f"log Unban", description = f"Usuario **{member}** Foi Desbanido por **{ctx.author}**", timestamp = datetime.now(), color = discord.Colour.red())

            embed.set_footer(text=f'Usuario {ctx.author} Usou o !unban',icon_url=ctx.author.avatar_url)
            await ub.send(embed = embed)


            return
           
            

@unban.error #func erro caso/caso
async def unban_error(ctx,error):
  if isinstance(error,commands.MissingRequiredArgument):
    await ctx.send('Por favor informe o Comando Correto, para mais informação use /help')
  if isinstance(error,commands.MissingPermissions):
    await ctx.send('Desclupe, você não tem permissão para ultilizar este comando.')


################# Fim Comando Unban ######################



###################### ban comando ########################
@bot.command()
@commands.has_permissions(ban_members=True)
@commands.bot_has_permissions(ban_members=True)

async def ban(ctx, member : discord.Member, *, reason=None):

    if (ctx.message.author.permissions_in(ctx.message.channel).ban_members):

        await member.ban(reason=reason) 
        print(f'{member} Foi banido do Servidor!')



        #bot.get_channel(id canal pra mandar msg)
        #log simples de comandos
        z = bot.get_channel(123)

        embed = discord.Embed(title = f"log bot", description = f"Comando !ban usado por \nAuthor: {ctx.author}", timestamp = datetime.now(), color = discord.Colour.red())
        embed.set_footer(text=f'Comando usado por - {ctx.author}',icon_url=ctx.author.avatar_url)
        await z.send(embed = embed)

        #bot.get_channel(id canal pra mandar msg)
        #log simples de comandos
        b = bot.get_channel(123)

        embed = discord.Embed(title = f"log Bans", description = f"Usuario **{member}** Foi Banido por **{ctx.author}**", timestamp = datetime.now(), color = discord.Colour.red())
        embed.set_image(url="https://i.pinimg.com/originals/88/08/0c/88080c99d67776ae7785207745a1f2ae.gif")
        embed.set_footer(text=f'Usuario {ctx.author} Usou o !ban',icon_url=ctx.author.avatar_url)
        await b.send(embed = embed)

@ban.error #func erro caso/caso
async def ban_error(ctx, error): 
    if isinstance(error,commands.MissingRequiredArgument):
      await ctx.send('Por favor informe o Comando correto, para mais informação use /help')
    if isinstance(error, commands.MissingPermissions):
      await ctx.send('Desclupe, você não tem permissão para ultilizar este comando.')


#################### Fim Comando Ban ###################################





#################### Kick Comando #########################

@bot.command() ## kick Comando
@commands.has_permissions(kick_members=True)
@commands.bot_has_permissions(kick_members=True)

async def kick(ctx, member : discord.Member, *, reason=None):

    if (ctx.message.author.permissions_in(ctx.message.channel).kick_members):

        await member.kick(reason=reason) 
        print(f'{member} Foi Kickado do Servidor!')


        #bot.get_channel(id canal pra mandar msg)
        #log simples de comandos
        z = bot.get_channel(123)

        embed = discord.Embed(title = f"log bot", description = f"Comando !kick usado por \nAuthor: {ctx.author}", timestamp = datetime.now(), color = discord.Colour.red())
        embed.set_footer(text=f'Comando usado por - {ctx.author}',icon_url=ctx.author.avatar_url)
        await z.send(embed = embed)

        #bot.get_channel(id canal pra mandar msg)
        #log simples de comandos
        k = bot.get_channel(123)

        embed = discord.Embed(title = f"log Kick", description = f"Usuario **{member}** Foi kick por **{ctx.author}**", timestamp = datetime.now(), color = discord.Colour.red())
        embed.set_image(url="https://c.tenor.com/_ONt70eHG-kAAAAC/expulso.gif")
        embed.set_footer(text=f'Usuario {ctx.author} Usou o !kick',icon_url=ctx.author.avatar_url)
        await k.send(embed = embed)


@kick.error #func erro caso/caso

async def kick_error(ctx, error):
  if isinstance(error,commands.MissingRequiredArgument):
    await ctx.send('Por favor, informe o comando correto. Para mais informações, use o /help kick.')
  if isinstance(error, commands.MissingPermissions):
    await ctx.send('Desclupe, você não tem permissão para ultilizar este comando.')

####################### Fim Comando Kick ###################################




################## Comando Userhelp ###########################
@bot.command()
async def userhelp(ctx):
    user = ctx.author
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        title='Comandos Usuario',
        description="Lista de Comandos",
        )
    embed.set_author(name=user,icon_url='https://www.tibiawiki.com.br/images/9/9c/Umbral_Master_Spellbook.gif')
    embed.add_field(name="Ping 🛠️", value="!ping",inline=False)
    
    embed.add_field(name="Verificar Usuario 🤡", value="!user <usuario>",inline=False)
    embed.add_field(name="Infos do Servidor 📊", value="!svinfo",inline=False)
    
    embed.add_field(name="Verificar Level 👨‍💻", value="!lvl ou !lvl <usuario>",inline=False)
    embed.add_field(name='LeaderBoard', value='!lb',inline=False)
    embed.set_footer(text='V0.1.0')

    await ctx.send(embed=embed)


    #bot.get_channel(id canal pra mandar msg)
    #log simples de comandos
    z = bot.get_channel(123)

    embed = discord.Embed(title = f"log bot", description = f"Comando !userhelp usado por \nAuthor: {ctx.author}", timestamp = datetime.now(), color = discord.Colour.red())
    embed.set_footer(text=f'Comando usado por - {ctx.author}',icon_url=ctx.author.avatar_url)
    await z.send(embed = embed)


    

################## Fim Comando Help ###########################

@bot.command()
@commands.has_permissions(administrator=True)
@commands.bot_has_permissions(administrator=True)
async def adminhelp(ctx):
    user = ctx.author
    embed = discord.Embed(
        colour=discord.Colour.red(),
        title='Comandos Admin',
        description="Lista de Comandos",
        )
    embed.set_author(name=user,icon_url='https://www.tibiawiki.com.br/images/3/3c/Spellbook_of_Ancient_Arcana.gif')
    embed.add_field(name="Ban 🚫", value="!ban <usuario>", inline=False)
    embed.add_field(name="kick❌", value="!kick <usuario>", inline=False)
    embed.add_field(name="Unban 🃏", value="!Unban <usuario>", inline=False)
    embed.add_field(name="clear🧺", value="!clear <valor>", inline=False)
    embed.add_field(name="reactrole para criar um embed de cargo por reação", value="!reactrole <emoji> <cargo> <.>", inline=False)
    
    embed.set_footer(text='V0.1.0')

    await ctx.send(embed=embed)

    #bot.get_channel(id canal pra mandar msg)
    #log simples de comandos
    z = bot.get_channel(123)

    embed = discord.Embed(title = f"log bot", description = f"Comando !adminhelp usado por \nAuthor: {ctx.author}", timestamp = datetime.now(), color = discord.Colour.red())
    embed.set_footer(text=f'Comando usado por - {ctx.author}',icon_url=ctx.author.avatar_url)
    await z.send(embed = embed)

@adminhelp.error #func erro sem perm
async def adminhelp_error(ctx,error):
  if isinstance(error,commands.MissingPermissions):
    await ctx.send('Desclupe, você não tem permissão para ultilizar este comando.')


############## Fim Canal dos Comandos ############################

from config import token
bot.run(token) #token importada da config
          

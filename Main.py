import discord
import asyncio
import info
from project_scrapper import recent_info

from discord import channel

TOKEN = info.get_token()
HELP = "[명령어 모음]" \
       "\n[$updateall] --> 모든 정보 받아오기" \
       "\n[$showproject] --> 사업단소식" \
       "\n[$showbachelor] --> 학사공지" \
       "\n[$shownotice] --> 일반소식" \
       "\n[$showjob] --> 취업정보" \
       "\n[$showcse] --> 우리학부 News"
client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith('$help'):
        h_channel = message.channel
        await h_channel.send(HELP)

    if message.content.startswith('$showproject'):
        p_channel = message.channel
        project_info = recent_info()
        index = project_info['index']
        date = project_info['date']
        title = project_info['title']
        content = project_info['content']
        show = f"[사업단소식]\n[번호]: {index} [작성일]: {date}\n[제목]: {title}\n-------------\n{content}"
        await p_channel.send(show)

client.run(TOKEN)

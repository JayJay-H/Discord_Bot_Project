import discord
import asyncio
from project_scrapper import recent_info

from discord import channel

TOKEN = 'NjU4OTczOTA1NDM1NzU0NTI2.XgHl9A.VevXgn0wOHpP48J_NecER1eluwA'
HELP = "[$showproject] --> 사업단 소식"
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
        channel = message.channel
        await channel.send(HELP)

    if message.content.startswith('$showproject'):
        channel = message.channel
        Info = recent_info()
        index = Info['index']
        date = Info['date']
        title = Info['title']
        content = Info['content']
        show = f"[사업단소식]\n[번호]: {index}          [작성일]: {date}\n[제목]: {title}\n-------------\n{content}"
        await channel.send(show)



client.run(TOKEN)

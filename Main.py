import discord
import asyncio
import info
from project_scrapper import send as project_send
from bachelor_scrapper import send as bachelor_send
from notice_scrapper import send as notice_send
from job_scrapper import send as job_send
from cse_scrapper import send as cse_send

TOKEN = info.get_token()
HELP = "[명령어 모음]" \
        "\n[$update] --> 모든 정보 받아오기" \
        "\n[$showb] --> 학사공지" \
        "\n[$shown] --> 일반소식" \
        "\n[$showp] --> 사업단소식" \
        "\n[$showj] --> 취업정보" \
        "\n[$showc] --> 우리학부 News"
line = "------------------------------------------------------------------------------------------------"
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
        last_update = info.get_last_update()
        date = f"20{last_update[0]}년 {last_update[1]}월 {last_update[2]}일"
        await h_channel.send(HELP)
        await h_channel.send(f'마지막 업데이트 날짜 : {date}')

    if message.content.startswith('$update'):
        await bachelor_send(message)
        await notice_send(message)
        await project_send(message)
        await job_send(message)
        await cse_send(message)
        info.set_last_update()
        await message.channel.send('업데이트 완료!')

    if message.content.startswith('$showb'):
        await bachelor_send(message)

    if message.content.startswith('$shown'):
        await notice_send(message)

    if message.content.startswith('$showp'):
        await project_send(message)

    if message.content.startswith('$showj'):
        await job_send(message)

    if message.content.startswith('$showc'):
        await cse_send(message)

client.run(TOKEN)

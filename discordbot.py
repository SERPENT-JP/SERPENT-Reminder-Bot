from datetime import datetime, timedelta
from discord.ext import tasks
import discord
import os
import traceback

token = os.environ['DISCORD_BOT_TOKEN']

client = discord.Client()

task_data = []


@client.event
async def on_ready():
    # print('やっほー！お前ら怠惰だからリマインダーちゃんが来てやったぜ！怠けんなよ')
    print(f'ログインしました{datetime.now()}')


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == '/rm help':
        embed = discord.Embed(
            title="HELP", description="リマインダーを設定します。\n/rm set [日時] [頻度(日)] [内容(空白開けずに)]\n例) /rm set 2021/1/1/8:00 1 朝活しようぜ", color=0xff0000)
        await message.channel.send(embed=embed)
    if '/rm set' in message.content:
        global task_data
        data = message.content.split()
        task = {
            'time': datetime.strptime(data[2], "%Y/%m/%d/%H:%M"),
            'frequency': data[3],
            'comment': data[4],
            'channel': message.channel
        }
        task_data.append(task)
        print(task_data)
        await message.channel.send(f"{task['time']}にリマインダーを設定しました")


@tasks.loop(seconds=60)
async def loop():
    global task_data
    now = datetime.now().strftime('%Y-%m-%d %H:%M:00')
    removelist = []
    for i in task_data:
        if f'{now}' == f"{i['time']}":
            if str(i['frequency']) == 'なし':
                removelist.append(i)
            else:
                new_task = {
                    'time': i['time'] + timedelta(days=int(i['frequency'])),
                    'frequency': i['frequency'],
                    'comment': i['comment'],
                    'channel': i['channel']
                }
                task_data.append(new_task)
                removelist.append(i)
            await i['channel'].send(embed=discord.Embed(
                title="通知", description=f"{now}{i['comment']}", color=0xff0000))
    for i in removelist:
        task_data.remove(i)
    print(task_data)


loop.start()
client.run(token)

from loguru import logger
# from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.onebot.v11 import Bot,Event, MessageEvent
from nonebot.exception import ActionFailed
from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.params import State
from nonebot import require
import sys
import asyncio
import aiohttp
import hashlib
import aiofiles

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
scheduler = require("nonebot_plugin_apscheduler").scheduler

yande=on_command("yande")

@yande.handle()
async def _(bot:Bot,event:Event,state: T_State = State()):
    #print(event.message)
    await main(str(event.message))

async  def dl(url,tags):
   
    loop = asyncio.get_event_loop()
    proxy = "http://127.0.0.1:10808"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}
    async with aiohttp.ClientSession(headers=headers,loop=loop, trust_env=True) as session:
        async with session.get(url, proxy=proxy) as response:
            #fileName = hashlib.sha256(url.encode('utf-8')).hexdigest()+'.png'
            fileName=url.replace('https://',"").replace(".","").replace("/","")+".png"
            async with aiofiles.open(f'png\{tags}\{fileName}', 'wb') as afp:
                  await afp.write(await response.content.read())


async def main(tags):
    proxy = "http://127.0.0.1:10808"
    loop = asyncio.get_event_loop()
    async with aiohttp.ClientSession(loop=loop, trust_env=True) as session:
        param = {'tags': tags, 'limit': '20'}
        async with session.get(f'https://yande.re/post.json', proxy=proxy, params=param) as resp:
            res = await resp.json()
            if setu := [x['source'] if x['source']!="" else x['file_url'] for x in res]:
                for setuurl in setu:
                    try:
                        await dl(setuurl.replace('i.pximg.net','i.pixiv.re'),tags)
                        
                    except Exception as e:
                        print(e)


@scheduler.scheduled_job(
    'cron',
    minute='*/30')
async def _():
    taglist=['loli','cat']
    for i in taglist:
        await main(i)

from fastapi import Path
import nonebot
from nonebot.permission import SUPERUSER
from nonebot import on_command,logger
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
import httpx
from typing import Optional
from nonebot import logger
import random

proxy = '127.0.0.1:10809'
proxies = {
    'http://': 'http://' + proxy,
    'https://': 'http://' + proxy,
}



headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39',
}
# with httpx.Client(headers=headers,proxies=proxies) as client:
#     r = client.get('https://konachan.net/post.json?tags=black_hair').json()
#     print(r[2]['file_url'])
    


sixty=on_command("来张壁纸",aliases={"!!图来"},priority=2,block=True)
@sixty.handle()
async def _(bot:Bot,event:MessageEvent):
    img_url=(await get_url())
    a = random.randint(0,20)
    if img_url[a]['rating']=='e':      
        await sixty.send(message=MessageSegment.text('太涩了不给你看！'))
    else:
        # logger.info('太涩了不给你看！')
        image_con = (await get_image(img_url[a]['file_url']))
        await sixty.send(message=MessageSegment.image(image_con))

async def get_url() -> Optional[str]:
   
    page = random.randint(0,1280)
    url = 'https://konachan.net/post.json?page='+str(page)+'&tags='
    async with httpx.AsyncClient(headers=headers) as client:
        r = (await client.get(url=url)).json()
        return r
    
async def get_image(image_url_to_down):
    async with httpx.AsyncClient(headers=headers) as client:
        image =  (await client.get(url=image_url_to_down)).content
        
        return image

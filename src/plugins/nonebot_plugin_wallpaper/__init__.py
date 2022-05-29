import asyncio

from nonebot.adapters.onebot.v11.helpers import CooldownIsolateLevel, Cooldown
from nonebot.permission import SUPERUSER
from nonebot import on_command,logger
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment,GroupMessageEvent,Message
import httpx
from typing import Optional, List
from nonebot import logger
import random
from nonebot.params import Arg,CommandArg
# from .withdraw import add_withdraw_job
proxy = '127.0.0.1:10809'
proxies = {
    'http://': 'http://' + proxy,
    'https://': 'http://' + proxy,
}
# proxies = None

group_admin = False

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39',
}

wallpaper=on_command("来张壁纸",aliases={"图来"},priority=2,block=True)
@wallpaper.handle(parameterless=[Cooldown(cooldown=1,
                                          prompt='冲的太快了，等会再冲吧！',
                                          isolate_level=CooldownIsolateLevel.USER)])
# @wallpaper.handle()
async def _(bot:Bot,event:GroupMessageEvent,args:Message = CommandArg()):
    """尝试撤回指令消息，以减少指令刷屏，需要管理员权限"""
    if group_admin:
        try:
            await bot.delete_msg(message_id=event.message_id)
        except:
            pass
    tags = args.extract_plain_text()
    # if tags:
        # await wallpaper.send(tags)
    img_url = (await get_url(tags))
    # else:
    #     img_url=(await get_url())
    if img_url==[]:
        await wallpaper.finish('搜索结果为空！请检查输入的标签是否正确！')
    a = random.randint(0,20)
    if img_url[a]['rating']=='e':
        """太se了就转为聊天记录发送"""
        # await wallpaper.send('太涩了不给你看！')
        image_con = (await get_image(img_url[a]['file_url']))
        msg = Message(MessageSegment.image(image_con))
        msg_list: List[Message] = []
        msg_list.append(msg) # type: ignore
        await send_forward_msg(bot,event,'很涩的色图',bot.self_id,msg_list)
    else:
        try:
            image_con = (await get_image(img_url[a]['file_url']))
            msg = Message(MessageSegment.image(image_con))
            msg_info = await wallpaper.send(message="90s后撤回"+msg,at_sender =True)
            # add_withdraw_job(bot,**msg_info)
            await async_recall(bot, msg_info['message_id'])
            # msg_list: List[Message] = []
            # msg_list.append(msg) # type: ignore
            # await send_forward_msg(bot,event,'这是一张色图',bot.self_id,msg_list)
        except Exception:
            logger.debug("获取失败")
            await wallpaper.finish("图片获取失败！")

async def get_url(tags:str='') -> Optional[str]:
   
    page = random.randint(0,100)
    url = 'https://danbooru.donmai.us/posts.json?page='+str(page)+'&tags='+tags
    logger.debug(url)
    async with httpx.AsyncClient(headers=headers,proxies=proxies) as client:
        r = (await client.get(url=url)).json()
        if r == []:
            url_new = 'https://danbooru.donmai.us/posts.json?page=1&tags=' + tags
            async with httpx.AsyncClient(headers=headers, proxies=proxies) as client:
                r = (await client.get(url=url_new)).json()
        return r
    
async def get_image(image_url_to_down):
    async with httpx.AsyncClient(headers=headers,proxies=proxies) as client:
        image =  (await client.get(url=image_url_to_down)).content
        logger.debug("图片下载成功")
        return image

async def send_forward_msg(
    bot: Bot,
    event: GroupMessageEvent,
    name: str,
    uin: str,
    msgs: List[str],
):
    def to_json(msg):
        return {"type": "node", "data": {"name": name, "uin": uin, "content": msg}}

    messages = [to_json(msg) for msg in msgs]
    await bot.call_api(
        "send_group_forward_msg", group_id=event.group_id, messages=messages
    )

async def async_recall(bot: Bot, event_id):
    """用于定时撤回机器人发出的消息"""
    await asyncio.sleep(90)
    await bot.delete_msg(message_id=event_id)
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
from .withdraw import add_withdraw_job
# proxy = '127.0.0.1:10809'
# proxies = {
#     'http://': 'http://' + proxy,
#     'https://': 'http://' + proxy,
# }
proxies = None
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36 Edg/101.0.1210.39',
}

wallpaper=on_command("来张壁纸",aliases={"图来"},priority=2,block=True)
@wallpaper.handle(parameterless=[Cooldown(cooldown=10,  prompt='冲的太快了，等会再冲吧！', isolate_level=CooldownIsolateLevel.USER)])
# @wallpaper.handle()
async def _(bot:Bot,event:GroupMessageEvent,args:Message = CommandArg()):
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
        await wallpaper.finish('搜索结果为空！')
    a = random.randint(0,20)
    if img_url[a]['rating']=='e':      
        await wallpaper.send('太涩了不给你看！')
    else:
        # logger.info('太涩了不给你看！')
        try:
            image_con = (await get_image(img_url[a]['file_url']))
            msg = Message(MessageSegment.image(image_con))
            # msg_list: List[Message] = []
            msg_info = await wallpaper.send(message="90s后撤回"+msg,at_sender =True)
            add_withdraw_job(bot,**msg_info)
            # msg_list.append(msg) # type: ignore
            # await send_forward_msg(bot,event,'这是一张色图',bot.self_id,msg_list)
        except Exception:
            logger.debug("获取失败")
            await wallpaper.finish("图片获取失败！")

async def get_url(tags:str='origional') -> Optional[str]:
   
    page = random.randint(0,100)
    url = 'https://danbooru.donmai.us/posts.json?page='+str(page)+'&tags='+tags
    logger.debug(url)
    async with httpx.AsyncClient(headers=headers,proxies=proxies) as client:
        r = (await client.get(url=url)).json()

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
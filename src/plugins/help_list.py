#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/5/25 21:10
# @Author  : QYB
# @File    : test_sese.py
# @Software: PyCharm
from multiprocessing import Event
from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent,MessageSegment,Bot,MessageEvent
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters import Message
import asyncio
help_list = on_command("帮助",aliases={"help","指令","功能列表"},priority=1,block=True)
help_detail = """
1、今天吃啥啊? 随机推荐菜单
2、爬/膜拜+人 沙雕表情包生成 
3、人生重来 进行人生重来游戏
4、搜图+图片 搜索图片来源
5、色图/涩涩 获取色图（暂时停用）
6、壁纸 获取高清壁纸
7、随机唐可可 锻炼视力(bushi
8、emoji+emoji 表情合成
9、疯狂星期四  发送抽风文案
10、反闪照(被动) 让我康康！
11、抽签/今日人品  看看运势
12、缩写/sx+缩写字母 查询缩写
13、回复bot撤回  撤回bot消息
14、点歌+歌名 给群友来首歌
"""
@help_list.handle()
async def _(bot:Bot,event:MessageEvent):
    await help_list.finish(help_detail)

sese_stop = on_command("涩涩",aliases={"色图","sese"},priority=10,block=True)
@sese_stop.handle()
async def stop_sese(bot:Bot,event:MessageEvent):
    await sese_stop.finish("受不可抗力影响，该功能暂时停用！")
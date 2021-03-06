#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter

# Custom your logger
# 
# from nonebot.log import logger, default_format
# logger.add("error.log",
#            rotation="00:00",
#            diagnose=False,
#            level="ERROR",
#            format=default_format)

# You can pass some keyword args config to init function
nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)

nonebot.load_builtin_plugins("echo")
nonebot.load_plugin("nonebot_plugin_hikarisearch")
nonebot.load_plugin("src.plugins.nonebot_plugin_fortune")
nonebot.load_plugin("src.plugins.nonebot_plugin_randomtkk")

nonebot.load_plugin("src.plugins.YetAnotherPicSearch")
nonebot.load_plugin("src.plugins.nonebot_plugin_emojimix")
nonebot.load_plugin("src.plugins.nonebot_plugin_antiflash")
nonebot.load_plugin("src.plugins.nonebot_plugin_crazy_thursday")
nonebot.load_plugin("src.plugins.nonebot_plugin_withdraw")
# nonebot.load_plugin("src.plugins.nonebot_plugin_remake")
nonebot.load_plugin("src.plugins.nonebot_plugin_wallpaper")
nonebot.load_plugin("src.plugins.nonebot_plugin_simplemusic")
#nonebot.load_plugin("src.plugins.nonebot_plugin_shindan")
nonebot.load_plugin("src.plugins.nonebot_plugin_what2eat")
nonebot.load_plugin("src.plugins.help_list")
nonebot.load_plugin("src.plugins.nonebot_plugin_abbrreply")
# nonebot.load_plugin("src.plugins.nonebot_plugin_poke_status")
nonebot.load_plugin("src.plugins.nonebot_plugin_petpet")
#nonebot.load_plugin("src.plugins.nonebot_plugin_setu_now")
#此处添加的为单个模块
nonebot.load_plugin("src.plugins.nonebot_mod_ji")
# nonebot.load_plugin("src.plugins.nonebot_mod_yande")
# nonebot-plugin-htmlrender(通过浏览器渲染图片)
# Please DO NOT modify this file unless you know what you are doing!
# As an alternative, you should use command `nb` or modify `pyproject.toml` to load plugins
# nonebot.load_from_toml("pyproject.toml")

# Modify some config / config depends on loaded configs
# 
# config = driver.config
# do something...


if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")

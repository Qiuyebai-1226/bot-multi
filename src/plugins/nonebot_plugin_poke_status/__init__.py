import psutil
from nonebot import get_driver, on_notice
from nonebot.rule import Rule
from nonebot.typing import T_State
from nonebot.params import State
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, Event, PokeNotifyEvent
from nonebot.adapters.onebot.v11.permission import PRIVATE_FRIEND, GROUP_ADMIN
from .config import Config

# global_config = get_driver().config
# config = Config.parse_obj(global_config)


#使用psutil库获取系统的信息状态
def cpu_info():
    cpu = str(psutil.cpu_times())
    user = float(cpu.split('user=')[1].split(',')[0])
    system = float(cpu.split('system=')[1].split(',')[0])
    idle = float(cpu.split('idle=')[1].split(',')[0])
    return {
        'used': round(user + system, 1),
        'user': round(user, 1),
        'syst': round(system, 1),
        'free': round(idle, 1),
        'prec': round((1 - idle / (user + system + idle)) * 100, 1)
    }


def mem_info():
    mem = str(psutil.virtual_memory())
    return {
        'total':
        round(float(mem.split('total=')[1].split(',')[0]) / (1024**3), 1),
        'available':
        round(float(mem.split('available=')[1].split(',')[0]) / (1024**3), 1),
        'percent':
        float(mem.split('percent=')[1].split(',')[0])
    }


def disk_info():
    disk = str(psutil.disk_usage('/'))
    return {
        'total':
        round(float(disk.split('total=')[1].split(',')[0]) / (1024**3), 1),
        'free':
        round(float(disk.split('free=')[1].split(',')[0]) / (1024**3), 1),
        'percent': float(disk.split('percent=')[1].split(',')[0].strip(')'))
    }


#判断是不是戳一戳事件，并判断是不是对本人（机器人）的事件
async def _is_poke(bot: Bot, event: Event, state: T_State = State()) -> bool:
    return isinstance(event, PokeNotifyEvent) and event.is_tome()


sys_info = on_notice(Rule(_is_poke), priority=50)


@sys_info.handle()
async def sys_info_handle(bot: Bot, event: Event, state: T_State = State()):
    cpu = cpu_info()
    mem = mem_info()
    disk = disk_info()
    await sys_info.finish(f'CPU占用率:{cpu["prec"]}%\
        \n内存占用率:{mem["percent"]}%\
        \n磁盘占用率:{disk["percent"]}%')

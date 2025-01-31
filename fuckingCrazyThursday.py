import random
import json
import os
import requests

from hoshino import Service
from hoshino.typing import MessageSegment, CQEvent
from hoshino.util import DailyNumberLimiter, FreqLimiter

time_limit = DailyNumberLimiter(3)
freq_limit = FreqLimiter(30)

sv = Service('疯狂星期四')

# 暂时采用@Pr0pHesyer提出的方案，使用线上json raw对象
@sv.on_fullmatch(('来点疯狂星期四文案', "疯狂星期四"))
async def random_post(bot, ev: CQEvent):
    # json数据存放路径
    filePath = os.path.join(os.path.dirname(__file__), 'post.json')
    # 将json对象加载到数组
    kfc = json.load(open(filePath, 'r', encoding="UTF-8")).get('post')
    # 随机选取数组中的一个对象
    randomPost = random.choice(kfc)

    # 限流
    if (time_limit.check(ev.user_id)):
        if (freq_limit.check(ev.user_id)):
            await bot.send(ev,randomPost)
            time_limit.increase(ev.user_id, 1)
            freq_limit.start_cd(ev.user_id)
        else:
            await bot.send(ev, "吮指原味鸡刚刚下锅，请过一会再来！")
    
# gitee屏蔽部分敏感词 暂时停用线上json raw对象
#     # json数据存放路径
#     filePath = os.path.join(os.path.dirname(__file__), 'post.json')
#     # 获取json数据
#     r = requests.get('https://gitee.com/Nicr0n/fucking_crazy_thursday/raw/master/post.json')
#     # 将json对象加载到数组
#     kfc = r.json().get('post')
#     # 随机选取数组中的一个对象
#     randomPost = random.choice(kfc)
#     await bot.send(ev,randomPost)

# 保留更新本地文件方案
# @sv.on_fullmatch('更新文案')
# async def update_post():
#     try:
#         r = requests.get('https://gitee.com/Nicr0n/fucking_crazy_thursday/raw/master/post.json')
#         # json数据存放路径
#         filePath = os.path.join(os.path.dirname(__file__), 'post.json')
#         post = open(filePath, 'w', encoding='utf-8')
#         kfc = json.dump(r.json(), post, ensure_ascii=False, indent=2)
#         print("更新成功")
#     except Exception:
#         print("更新失败")

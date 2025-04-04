from pkg.plugin.context import (
    register,
    handler,
    llm_func,
    BasePlugin,
    APIHost,
    EventContext,
)
from pkg.plugin.events import NormalMessageResponded   # 导入事件类
from mirai import Image, MessageChain
import re
import httpx
import random
import logging

# 注册插件


@register(name="weather", description="Weather", version="0.1", author="zzseki")
class WeatherPlugin(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        self.logger = logging.getLogger(__name__)


    @handler(NormalMessageResponded)
    async def normal_message_responded(self, ctx: EventContext, **kwargs):
        response_text = ctx.event.response_text

        #今天|明天|后天|大后天|一天后|两天后|三天后|四天后|五天后|六天后|1天后|2天后|3天后|4天后|5天后|6天后|
        # 一天之后|两天之后|三天之后|四天之后|五天之后|六天之后|1天之后|2天之后|3天之后|4天之后|5天之后|6天之后|
        # 一天以后|两天以后|三天以后|四天以后|五天以后|六天以后|1天以后|2天以后|3天以后|4天以后|5天以后|6天以后

        # 定义正则表达式模式，匹配形如 城市:xxx 的字符串
        CITY_PATTERN = re.compile(r"城市:(.*?)(今天|明天|后天|大后天|一天后|两天后|三天后|四天后|五天后|六天后|1天后|2天后|3天后|4天后|5天后|6天后|一天之后|两天之后|三天之后|四天之后|五天之后|六天之后|1天之后|2天之后|3天之后|4天之后|5天之后|6天之后|一天以后|两天以后|三天以后|四天以后|五天以后|六天以后|1天以后|2天以后|3天以后|4天以后|5天以后|6天以后)的天气情况")
        #TIME_PATTERN = re.compile(r"为你查询城市：\w+([^天]+)天的天气情况")

        match = CITY_PATTERN.search(response_text)
        # 如果找到匹配的字符串，则处理
        if match:
            if match.group(2) == "今天" or match.group(2) == "0" or match.group(2) == "零":
                W_time = 0  # 0表示当天的天气，1表示明天的天气，以此类推最高查询七天



            elif match.group(2) == "明天" or match.group(2) == "1天后" or match.group(2) == "一天后"or match.group(2) == "1天之后" or match.group(2) == "一天之后"or match.group(2) == "1天以后" or match.group(2) == "一天以后":
                W_time = 1


            elif match.group(2) == "后天" or match.group(2) == "2天后" or match.group(2) == "两天后"or match.group(2) == "2天之后" or match.group(2) == "两天之后"or match.group(2) == "2天以后" or match.group(2) == "两天以后":
                W_time = 2


            elif match.group(2) == "大后天" or match.group(2) == "3天后" or match.group(2) == "三天后"or match.group(2) == "3天之后" or match.group(2) == "三天之后"or match.group(2) == "3天以后" or match.group(2) == "三天以后":
                W_time = 3


            elif match.group(2) == "大大后天" or match.group(2) == "4天后" or match.group(2) == "四天后"or match.group(2) == "4天之后" or match.group(2) == "四天之后"or match.group(2) == "4天以后" or match.group(2) == "四天以后":
                W_time = 4


            elif match.group(2) == "大大大后天" or match.group(2) == "5天后" or match.group(2) == "五天后"or match.group(2) == "5天之后" or match.group(2) == "五天之后"or match.group(2) == "5天以后" or match.group(2) == "五天以后":
                W_time = 5


            elif match.group(2) == "大大大大后天" or match.group(2) == "6天后" or match.group(2) == "六天后"or match.group(2) == "6天之后" or match.group(2) == "六天之后"or match.group(2) == "6天以后" or match.group(2) == "六天以后":
                W_time = 6

            else:
                W_time = 0

        # 如果找到匹配的字符串，则处理
        if match:
            city = match.group(1)

            #for city in match.group(1):

                # 处理每一个匹配到的城市名称

            self.logger.info(city)
            text = await self.get_weather(city, W_time)

            if text:
                await ctx.event.query.adapter.reply_message(
                    ctx.event.query.message_event, [(text)], False
                )
            else:
                self.logger.warning("没有找到符合条件的城市信息。")

    async def get_weather(self, city, W_time):
        url = "https://v.api.aa1.cn/api/api-tianqi-3/index.php"  # 修改API地址
        params = {
            "msg": city,  # 使用msg参数传递城市名
            "type": "1"   # 固定类型参数
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()

        response_data = response.json()
        if response_data["code"] != "1":  # 检查返回状态码
            return None
        data = response_data["data"]

        if W_time < 0 or W_time >= len(data):  # 防止索引越界
            return None

        day_weather = data[W_time]
        result = (f"城市：{city}\n"  # 直接使用传入的城市名
                  f"日期：{day_weather['riqi']}\n"
                  f"天气：{day_weather['tianqi']}\n"
                  f"温度：{day_weather['wendu']}\n"
                  f"风力：{day_weather['fengdu']}\n"
                  f"空气质量：{day_weather['pm']}\n")

        return result

    # 插件卸载时触发
    def __del__(self):
        pass

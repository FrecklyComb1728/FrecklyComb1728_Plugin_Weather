from pkg.plugin.context import register, handler, BasePlugin, APIHost, EventContext
from pkg.plugin.events import PersonMessageReceived, GroupMessageReceived
from mirai import Image, MessageChain, Plain
import re
import httpx
import logging
import json

@register(name="Weather", description="天气查询插件", version="0.1", author="RockChinQ")
class WeatherPlugin(BasePlugin):

    def __init__(self, host: APIHost):
        self.logger = logging.getLogger(__name__)

    @handler(PersonMessageReceived)
    @handler(GroupMessageReceived)
    async def message_received(self, ctx: EventContext):
        msg = str(ctx.event.message_chain).strip()
        match = re.match(r"^/天气(?:\s+(.*))?$", msg)
        if not match:
            return
        args_str = match.group(1) or ""
        result = await self.query_weather_logic(args_str)
        await ctx.reply(MessageChain([Plain(result)]))
        ctx.prevent_default()

    async def query_weather_logic(self, args_str: str) -> str:
        args = args_str.split()
        city = None
        time = None

        if len(args) >= 1:
            city = args[0].strip()

        if len(args) >= 2:
            time = args[1].strip()

        if not city:
            return "请使用格式：/天气 [城市] [时间]（如：/天气 北京 今天 或 /天气 北京）"

        try:
            if not time:
                return await self.get_multi_day_weather(city)
            else:
                return await self.get_single_day_weather(city, time)
        except Exception as e:
            self.logger.error(f"天气查询整体异常：{str(e)}")
            return "天气查询发生异常，请稍后再试"

    async def get_single_day_weather(self, city: str, time: str) -> str:
        time_mapping = {
            "今天": 0,
            "明天": 1,
            "后天": 2,
        }
        W_time = time_mapping.get(time, None)
        if W_time is None:
            return f"不支持的时间参数：{time}，可选：今天、明天、后天"

        try:
            data = await self.fetch_weather_data(city)
        except Exception as e:
            self.logger.error(f"天气接口调用失败：{str(e)}")
            return "天气接口调用失败，请稍后再试"

        if not isinstance(data, list) or len(data) < 3:
            return "API返回数据异常，请稍后再试"

        # 确保索引在有效范围内
        if W_time < 0 or W_time >= 3:
            return "查询时间超出范围（支持今天、明天、后天）"

        day_weather = data[W_time]
        return (
            f"城市：{city}\n"
            f"日期：{day_weather.get('date', 'N/A')}\n"
            f"天气：{day_weather.get('weather', 'N/A')}\n"
            f"温度：{day_weather.get('temperature', 'N/A')}\n"
            f"风力：{day_weather.get('wind', 'N/A')}\n"
            f"空气质量：{day_weather.get('air_quality', 'N/A')}\n"
        )

    async def get_multi_day_weather(self, city: str) -> str:
        try:
            data = await self.fetch_weather_data(city)
            if not isinstance(data, list) or len(data) < 3:
                return "无法获取未来三天天气数据，请稍后再试"

            result = f"城市：{city}\n未来三天天气预报：\n"
            for i in range(3):
                day = data[i]
                result += (
                    f"日期：{day.get('date', 'N/A')}\n"
                    f"天气：{day.get('weather', 'N/A')}\n"
                    f"温度：{day.get('temperature', 'N/A')}\n"
                    "---------------------\n"
                )
            return result
        except Exception as e:
            self.logger.error(f"多天天气查询失败: {str(e)}")
            return "天气查询发生异常，请稍后再试"

    async def fetch_weather_data(self, city: str) -> list:
        url = "https://v2.api-m.com/api/weather"
        params = {"city": city}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10)
                response.raise_for_status()
                response_data = response.json()
            
            if response_data.get("code") != 200:
                error_msg = response_data.get("msg", "未知错误")
                raise ValueError(f"API返回错误：{error_msg}")
            
            # 获取数据并调整索引：
            # 假设原始数据包含昨天、今天、明天、后天...
            # 截取今天及未来两天（索引1、2、3）
            raw_data = response_data.get("data", {}).get("data", [])
            adjusted_data = []
            if len(raw_data) >= 4:
                adjusted_data = raw_data[1:4]  # 今天、明天、后天
            else:
                adjusted_data = raw_data[:3]   # 若数据不足，取前3条
            
            return adjusted_data
            
        except httpx.RequestError as e:
            raise Exception(f"网络请求失败：{str(e)}")
        except (json.JSONDecodeError, KeyError) as e:
            raise Exception("API响应格式错误")
        except Exception as e:
            raise Exception(f"未知错误：{str(e)}")
    def __del__(self):
        # 如果需要清理资源，可以在这里添加逻辑
        pass
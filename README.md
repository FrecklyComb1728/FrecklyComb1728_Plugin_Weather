# Langbot天气查询插件

## 安装

# 在QChatGPT主程序配置完成后，使用管理员账号向机器人发送：
!plugin get https://github.com/FrecklyComb1728/Langbot_Weather

## 🌟 核心功能

### 多维度天气数据
- **未来3日预报**：支持当天至未来3天的天气查询
- **数据维度**：
  - 当天日期 （如：星期六）
  - 天气情况（晴/雨/雪等）
  - 温度范围（最高/最低）
  - 风力等级与方向（修复中）
  - 空气质量指数（修复中）
  - 相对湿度（修复中）


## 📖 使用示例

### 查询语法格式
```text
" /天气 [城市名] [时间描述]" 结构：
• 城市名：需包含省级行政单位（如"上海"）
• 时间：支持自然语言时间描述
```
**用户请求**：
```text
/天气 北京
```
**机器人响应**：
```text
未来三天天气预报：
日期：周六
天气：阵雨
温度：20-26℃
---------------------
日期：周日
天气：阴
温度：20-25℃
---------------------
日期：周一
天气：阵雨
温度：20-25℃
---------------------
```


## 📬 技术支持
[![GitHub Issues](https://img.shields.io/github/issues/FrecklyComb1728/QChatGPT_Plugin_Weather)](https://github.com/FrecklyComb1728/QChatGPT_Plugin_Weather/issues)

## 感谢
本插件基于zzseki的QChatGPT_Plugin_Weather修改而来
[https://github.com/zzseki/QChatGPT_Plugin_Weather](https://socialify.git.ci/zzseki/QChatGPT_Plugin_Weather/image?language=1&owner=1&name=1&stargazers=1&theme=Light)

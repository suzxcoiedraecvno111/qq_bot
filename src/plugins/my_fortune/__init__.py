import httpx
from nonebot import on_command, get_driver
from nonebot.adapters.onebot.v11 import GroupMessageEvent, GROUP
from nonebot.log import logger

from src.plugins.auto_summary.db import get_latest_summary_content

driver = get_driver()
global_config = driver.config

# AI 配置（复用硅基流动的配置）
AI_API_KEY = getattr(global_config, "ai_api_key", "") or getattr(global_config, "auto_summary_api_key", "")
AI_API_BASE = getattr(global_config, "ai_api_base", "https://api.siliconflow.cn/v1")
AI_MODEL = getattr(global_config, "ai_model", "deepseek-ai/DeepSeek-V4-Flash")

async def call_ai(prompt: str) -> str:
    """调用大模型生成运势解读"""
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                f"{AI_API_BASE}/chat/completions",
                headers={
                    "Authorization": f"Bearer {AI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": AI_MODEL,
                    "messages": [
                        {"role": "system", "content": "你是一位占卜大师，根据用户提供的群聊对话总结，为今天该群的运势进行占卜解读。回复要简洁、有趣、贴合群聊氛围，可以适当使用颜文字。字数控制在80字以内。"},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 150,
                    "temperature": 0.7
                },
                timeout=15.0
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            logger.error(f"AI 调用失败: {e}")
            return "✨ 今日运势：诸事皆宜，心情愉快～"

fortune_cmd = on_command("今日运势", permission=GROUP, priority=10, block=True)

@fortune_cmd.handle()
async def handle_fortune(event: GroupMessageEvent):
    group_id = event.group_id
    # 从数据库获取该群的最新总结
    summary = get_latest_summary_content(group_id) or ""
    if summary:
        prompt = f"以下是本群最近的对话总结：\n{summary}\n\n请根据这些内容，为今天的群运势写一段占卜解读。"
        logger.info(f"群 {group_id} 今日运势使用总结: {summary[:100]}...")
    else:
        prompt = "本群暂无对话总结，请随机生成一段今日群运势占卜解读。"
        logger.info(f"群 {group_id} 今日运势无总结，使用随机占卜")

    reply = await call_ai(prompt)
    await fortune_cmd.finish(reply)
import httpx
from nonebot import on_message, get_driver
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageEvent
from nonebot.rule import Rule
from nonebot.log import logger

from src.plugins.auto_summary.db import get_latest_summary_content
from .config import Config

driver = get_driver()
global_config = driver.config
plugin_config = Config(**global_config.dict())

def keyword_rule(event: MessageEvent) -> bool:
    if not isinstance(event, GroupMessageEvent):
        return False
    text = event.get_plaintext().strip()
    if text.startswith("/"):
        return False
    lower_text = text.lower()
    for kw in plugin_config.keyword_ai_list:
        if kw.lower() in lower_text:
            return True
    return False

keyword_matcher = on_message(rule=Rule(keyword_rule), priority=9, block=False)

@keyword_matcher.handle()
async def handle_keyword_ai(event: GroupMessageEvent):
    user_msg = event.get_plaintext().strip()
    group_id = event.group_id
    logger.info(f"[关键词AI] 群 {group_id} 触发词匹配，消息：{user_msg}")

    # 从数据库获取该群的最新总结（纯文本）
    summary = get_latest_summary_content(group_id) or ""
    if summary:
        logger.info(f"[关键词AI] 加载群 {group_id} 最新总结")
    else:
        logger.info(f"[关键词AI] 群 {group_id} 暂无总结")

    # 构造系统提示：基础人设 + 对话总结
    system_prompt = plugin_config.ai_system_prompt
    if summary:
        system_prompt += f"\n\n以下是本群最近的对话总结：\n{summary}"

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                f"{plugin_config.ai_api_base}/chat/completions",
                headers={
                    "Authorization": f"Bearer {plugin_config.ai_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": plugin_config.ai_model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_msg}
                    ],
                    "max_tokens": plugin_config.ai_max_tokens,
                    "temperature": plugin_config.ai_temperature
                },
                timeout=plugin_config.ai_timeout
            )
            resp.raise_for_status()
            data = resp.json()
            reply = data["choices"][0]["message"]["content"].strip()
            if reply:
                await keyword_matcher.finish(reply)
            else:
                await keyword_matcher.finish("嗯？")
        except Exception as e:
            logger.error(f"[关键词AI] 调用失败: {e}")
            await keyword_matcher.finish("抱歉，我有点忙，稍后再试~")
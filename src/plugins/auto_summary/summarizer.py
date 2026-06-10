import asyncio
from datetime import datetime, timedelta
from pathlib import Path
import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from nonebot import get_driver, logger
from .config import plugin_config
from .message_cache import cache
from . import db

BASE_DIR = Path(__file__).parent.parent.parent.parent
SAVE_DIR = BASE_DIR / "data" / "auto_summary" / "summaries"
SAVE_DIR.mkdir(parents=True, exist_ok=True)

scheduler = None

async def summarize_messages(group_id: int, messages: list[str]) -> str:
    if not messages:
        return "无新消息。"
    content = "\n".join(messages)
    if len(content) > 3000:
        content = content[:3000] + "...(已截断)"
    prompt = plugin_config.auto_summary_prompt + "\n\n" + content
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                f"{plugin_config.auto_summary_api_base}/chat/completions",
                headers={
                    "Authorization": f"Bearer {plugin_config.auto_summary_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": plugin_config.auto_summary_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 200,
                    "temperature": 0.3
                },
                timeout=30.0
            )
            resp.raise_for_status()
            data = resp.json()
            summary = data["choices"][0]["message"]["content"].strip()
            return summary
        except Exception as e:
            logger.error(f"总结群 {group_id} 失败: {e}")
            return f"总结失败: {e}"

async def summarize_group(group_id: int):
    messages = cache.get_and_clear(group_id)
    if not messages:
        return
    logger.info(f"开始总结群 {group_id}，共 {len(messages)} 条消息")
    summary = await summarize_messages(group_id, messages)
    interval = plugin_config.auto_summary_interval
    end_time = datetime.now()
    start_time = end_time - timedelta(seconds=interval)
    db.save_summary(group_id, start_time, end_time, summary, keywords=None)
    timestamp = end_time.strftime("%Y%m%d_%H%M%S")
    save_path = SAVE_DIR / f"group_{group_id}_{timestamp}.txt"
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(f"群号: {group_id}\n时间: {end_time}\n消息数量: {len(messages)}\n\n总结:\n{summary}")
    logger.info(f"群 {group_id} 总结已保存至 {save_path} 及数据库")

async def summarize_all_groups():
    groups = cache.get_all_groups()
    if not groups:
        logger.info("没有需要总结的群消息")
        return
    for group_id in groups:
        await summarize_group(group_id)

def start_scheduler():
    global scheduler
    if not plugin_config.auto_summary_enabled:
        logger.info("自动总结插件未启用")
        return
    scheduler = AsyncIOScheduler()
    scheduler.add_job(summarize_all_groups, "interval", seconds=plugin_config.auto_summary_interval, id="auto_summary")
    scheduler.start()
    logger.info(f"自动总结已启动，间隔 {plugin_config.auto_summary_interval} 秒")

def stop_scheduler():
    global scheduler
    if scheduler:
        scheduler.shutdown()
        scheduler = None
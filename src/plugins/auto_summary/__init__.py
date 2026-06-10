from nonebot import get_driver, require
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageEvent, GROUP_ADMIN, GROUP_OWNER
from nonebot.message import event_preprocessor
from nonebot.permission import SUPERUSER
from nonebot import on_command
from datetime import datetime, timedelta

from .config import Config, plugin_config
from .summarizer import start_scheduler, stop_scheduler
from .message_cache import cache
from . import db

__plugin_meta__ = PluginMetadata(
    name="自动群聊总结",
    description="每3小时自动总结群聊消息，清除历史缓存，减少 token 消耗，支持历史查询和长期记忆",
    usage="自动运行，管理员可使用 /群总结 查询最近总结或按日期/关键词检索",
    config=Config,
)

driver = get_driver()
require("nonebot_plugin_apscheduler")


@driver.on_startup
async def on_startup():
    start_scheduler()


@driver.on_shutdown
async def on_shutdown():
    stop_scheduler()


@event_preprocessor
async def collect_group_messages(event: MessageEvent):
    """监听群消息，将纯文本消息存入缓存（排除指令和过短内容）"""
    if not isinstance(event, GroupMessageEvent):
        return
    msg_text = event.get_plaintext().strip()
    if msg_text.startswith("/"):
        return
    if len(msg_text) < 2:
        return
    # 可选：如果配置了特定群列表且当前群不在列表中，则不缓存
    if plugin_config.auto_summary_group_ids and event.group_id not in plugin_config.auto_summary_group_ids:
        return
    cache.add_message(event.group_id, event.user_id, msg_text)


# 管理员命令：查询历史总结
history_cmd = on_command("群总结", permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=8, block=True)


@history_cmd.handle()
async def handle_group_summary(event: GroupMessageEvent):
    args = event.get_message().extract_plain_text().strip().split()
    group_id = event.group_id

    if not args:
        summaries = db.get_recent_summaries(group_id, limit=3)
        if not summaries:
            await history_cmd.finish("本群暂无历史总结。")
        reply = "📜 最近群总结：\n"
        for s in summaries:
            end_time = datetime.fromisoformat(s['end_time']).strftime("%Y-%m-%d %H:%M")
            reply += f"\n[{end_time}] {s['content'][:100]}..."
        await history_cmd.finish(reply)

    elif args[0].isdigit():
        try:
            date_obj = datetime.strptime(args[0], "%Y-%m-%d")
            start = datetime.combine(date_obj, datetime.min.time())
            end = datetime.combine(date_obj, datetime.max.time())
            summaries = db.get_summaries_by_time_range(group_id, start, end)
            if not summaries:
                await history_cmd.finish(f"未找到 {args[0]} 的群总结。")
            reply = f"📅 {args[0]} 群总结：\n"
            for s in summaries:
                reply += f"\n{s['content']}"
            await history_cmd.finish(reply)
        except ValueError:
            await history_cmd.finish("日期格式错误，请使用 YYYY-MM-DD 格式。")

    elif args[0] == "关键词":
        keyword = ' '.join(args[1:])
        if not keyword:
            await history_cmd.finish("请提供关键词。")
        summaries = db.get_summaries_by_keyword(group_id, keyword, limit=5)
        if not summaries:
            await history_cmd.finish(f"未找到包含关键词「{keyword}」的总结。")
        reply = f"🔍 包含「{keyword}」的总结：\n"
        for s in summaries:
            end_time = datetime.fromisoformat(s['end_time']).strftime("%Y-%m-%d %H:%M")
            reply += f"\n[{end_time}] {s['content'][:80]}..."
        await history_cmd.finish(reply)

    else:
        await history_cmd.finish("用法：\n/群总结 - 最近3条\n/群总结 2026-06-09 - 指定日期\n/群总结 关键词 xxx - 关键词检索")
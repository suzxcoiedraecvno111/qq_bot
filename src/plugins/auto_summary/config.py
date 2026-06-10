from pydantic import BaseModel, Field
from nonebot import get_plugin_config

class Config(BaseModel):
    auto_summary_group_ids: list[int] = Field(default_factory=list)
    auto_summary_interval: int = 10800
    auto_summary_max_cache: int = 500
    auto_summary_batch_size: int = 100
    auto_summary_prompt: str = "请用200字以内总结以下群聊内容，要求简洁明了，提取重点。"
    auto_summary_api_key: str = ""
    auto_summary_api_base: str = "https://api.siliconflow.cn/v1"
    auto_summary_model: str = "deepseek-ai/DeepSeek-V3"
    auto_summary_enabled: bool = True

plugin_config = get_plugin_config(Config)
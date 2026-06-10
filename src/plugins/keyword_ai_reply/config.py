from pydantic import BaseModel, Field
from typing import List, Optional

class Config(BaseModel):
    keyword_ai_list: List[str] = Field(default_factory=list)

    # AI 接口配置
    ai_api_key: str = ""
    ai_api_base: str = "https://api.siliconflow.cn/v1"
    ai_model: str = "deepseek-ai/DeepSeek-V4-Flash"
    ai_system_prompt: str = "你是花碎，一个温暖、真诚的朋友。请根据用户消息和对话总结生成简短、自然的回复，可以适当使用颜文字。回复尽量控制在20字以内。"
    ai_max_tokens: int = 100
    ai_temperature: float = 0.7
    ai_timeout: float = 10.0

    # 自动总结的存储目录（相对于项目根目录）
    summary_base_dir: str = "data/auto_summary/summaries"
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
插件及环境验证脚本
用法: 在虚拟环境中执行 python check_plugins.py
"""

import sys
import os
from pathlib import Path

# 确保能加载项目配置
sys.path.insert(0, str(Path(__file__).parent))

# 待检查的插件模块列表
PLUGINS_TO_CHECK = [
    "nonebot_plugin_llmchat",
    "nonebot_plugin_resolver2",
    "nonebot_plugin_poke",
]

def check_imports():
    """检查插件模块是否可导入"""
    print("=" * 50)
    print("检查插件导入...")
    print("=" * 50)
    failed = []
    for plugin in PLUGINS_TO_CHECK:
        try:
            __import__(plugin)
            print(f"[✓] {plugin} 导入成功")
        except ImportError as e:
            print(f"[✗] {plugin} 导入失败: {e}")
            failed.append(plugin)
    return failed

def check_env_file():
    """检查 .env 文件是否存在并包含必要的配置项"""
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        print("\n[✗] .env 文件不存在，请先创建配置文件")
        return False

    print("\n" + "=" * 50)
    print("检查 .env 配置...")
    print("=" * 50)
    
    required_keys = [
        "HOST", "PORT",            # NoneBot 基础配置
        "SUPERUSERS",
        "LLMCHAT__API_PRESETS",
    ]
    
    missing = []
    with open(env_path, "r", encoding="utf-8") as f:
        content = f.read()
        for key in required_keys:
            if key not in content:
                missing.append(key)
    
    if missing:
        print(f"[✗] 缺失以下配置项: {', '.join(missing)}")
        return False
    else:
        print("[✓] 所有必需配置项均存在")
        return True

def main():
    print("正在验证 NoneBot2 插件环境...\n")
    # 检查 .env
    env_ok = check_env_file()
    # 检查插件导入
    failed_plugins = check_imports()
    
    print("\n" + "=" * 50)
    if not env_ok:
        print("[结论] .env 配置有问题，请修正后重试。")
    elif failed_plugins:
        print(f"[结论] 以下插件导入失败: {', '.join(failed_plugins)}，请检查是否已正确安装。")
    else:
        print("[结论] 所有检查通过！可以尝试启动机器人: python bot.py")
    print("=" * 50)

if __name__ == "__main__":
    main()
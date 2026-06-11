# 🌸 花碎机器人 (HuSuiBot)

基于 [NoneBot2](https://github.com/nonebot/nonebot2) 和 [OneBot V11](https://github.com/botuniverse/onebot-11) 协议的智能 QQ 群聊机器人。

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| **🤖 AI 对话** | 基于 LLM（DeepSeek）的自然语言对话，温暖人设，自然回复 |
| **📝 自动群聊总结** | 每 3 小时自动总结群聊消息，支持按日期/关键词查询历史总结 |
| **🎯 关键词触发回复** | 检测关键词自动调用 AI 结合群聊上下文回复 |
| **🔮 今日运势** | 命令 `/今日运势`，根据群聊内容生成趣味占卜 |
| **👆 戳一戳回应** | 被戳时随机回复文字+图片 |
| **🔗 链接解析** | 自动解析分享链接内容 |
| **🌐 消息翻译** | 内置翻译功能 |

## 📋 环境要求

- Python 3.10+
- QQ 账号（用于登录机器人）
- 协议端：NapCat 或 go-cqhttp（任选其一）
- 签名服务：Qsign（NapCat 需要）

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/suzxcoiedraecvno111/qq_bot.git
cd qq_bot
```

### 2. 创建虚拟环境并安装依赖

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并填写配置：

```bash
copy .env.example .env   # Windows
cp .env.example .env     # Linux/macOS
```

编辑 `.env` 文件，填入你的信息：

| 配置项 | 说明 | 获取方式 |
|--------|------|----------|
| `SUPERUSERS` | 机器人管理员的 QQ 号 | 你自己的 QQ 号 |
| `LLMCHAT__API_PRESETS` | AI 接口配置（API Key + 模型） | [硅基流动](https://cloud.siliconflow.cn) 注册获取 |

### 4. 部署协议端

机器人需要通过 OneBot 协议连接 QQ。有两种方式：

#### 方式 A：NapCat（推荐）

1. 下载 [NapCat.Shell.Windows.OneKey.zip](https://github.com/NapNeko/NapCatQQ/releases)（在 Releases 中下载）
2. 解压后运行 `napcat.bat`，扫码登录 QQ
3. NapCat 默认在 `ws://127.0.0.1:8081` 提供 OneBot WebSocket 接口

#### 方式 B：go-cqhttp

1. 下载 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp/releases)
2. 配置正向 WebSocket 连接，地址填写 `ws://127.0.0.1:8081`

### 5. 启动机器人

```bash
python bot.py
```

看到 `OneBot V11 | 已连接` 表示启动成功。

## ⚙️ 配置详解

### 插件配置（在 .env 中设置）

#### 自动群聊总结

```ini
auto_summary_api_key=你的API_Key
auto_summary_api_base=https://api.siliconflow.cn/v1
auto_summary_model=deepseek-ai/DeepSeek-V3
auto_summary_interval=10800  # 总结间隔（秒），默认3小时
auto_summary_max_cache=500   # 最大缓存消息数
```

#### 关键词 AI 回复

```ini
ai_api_key=你的API_Key
ai_api_base=https://api.siliconflow.cn/v1
ai_model=deepseek-ai/DeepSeek-V4-Flash
keyword_ai_list=["关键词1","关键词2"]  # 触发关键词列表
ai_system_prompt="你的人设提示词"
```

### 命令列表

| 命令 | 说明 | 权限 |
|------|------|------|
| `/群总结` | 查看最近 3 条群总结 | 群主/管理/SuperUser |
| `/群总结 YYYY-MM-DD` | 查看指定日期总结 | 同上 |
| `/群总结 关键词 xxx` | 按关键词检索总结 | 同上 |
| `/今日运势` | 生成群运势占卜 | 群成员 |

## 📦 一键部署（Windows）

下载安装包：[HuSuiBot_Setup.exe](https://github.com/suzxcoiedraecvno111/qq_bot/releases)（Releases 页面）

安装包会自动部署 Python 环境、安装依赖、创建快捷方式。

## 🏗️ 项目结构

```
HuSuiBot/
├── bot.py                 # 主入口
├── pyproject.toml          # 项目配置
├── requirements.txt        # Python 依赖
├── .env.example            # 配置模板
├── .gitignore
├── LICENSE                 # MIT 许可证
├── README.md
├── src/
│   └── plugins/            # 自定义插件
│       ├── auto_summary/   # 自动群聊总结
│       ├── keyword_ai_reply/ # 关键词 AI 回复
│       └── my_fortune/     # 今日运势
├── data/
│   └── poke/               # 戳一戳资源
│       ├── poke.txt
│       └── pic/
├── scripts/                # 启动脚本
│   ├── start_bot.bat
│   └── start_all.bat       # 一键启动所有服务
├── installer/              # 安装程序相关
│   └── installer.iss
└── docs/                   # 文档
```

## 🔧 常见问题

**Q: 提示 `ModuleNotFoundError`？**
A: 请确认已激活虚拟环境并执行了 `pip install -r requirements.txt`。

**Q: 机器人无法连接？**
A: 检查协议端（NapCat/go-cqhttp）是否已启动且 WebSocket 端口为 8081。

**Q: AI 返回空响应？**
A: 检查 `.env` 中的 API Key 是否正确，以及硅基流动账户余额是否充足。

## 📜 许可证

本项目使用 [MIT License](LICENSE)。

## 🙏 致谢

- [NoneBot2](https://github.com/nonebot/nonebot2) - 优秀的 Python 机器人框架
- [NapCat](https://github.com/NapNeko/NapCat) - QQ NT 协议实现
- [SiliconFlow](https://cloud.siliconflow.cn) - AI 推理 API 服务

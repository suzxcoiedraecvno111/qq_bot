import nonebot
from nonebot.adapters.onebot.v11 import Adapter as OneBotAdapter

nonebot.init()

driver = nonebot.get_driver()
driver.register_adapter(OneBotAdapter)

# 加载需要的插件
nonebot.load_plugin("nonebot_plugin_llmchat")
nonebot.load_plugin("nonebot_plugin_resolver2")
nonebot.load_plugin("nonebot_plugin_poke")
nonebot.load_plugin("src.plugins.auto_summary")
nonebot.load_plugin("src.plugins.keyword_ai_reply")
nonebot.load_plugin("nonebot_plugin_easy_translate")
nonebot.load_plugin("src.plugins.my_fortune")

if __name__ == "__main__":
    nonebot.run()
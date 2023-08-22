"""."""
import sys

from alicebot.bot import Bot

PLUGIN_MODULE_NAME = sys.argv[1]

print(f"PLUGIN_MODULE_NAME: {PLUGIN_MODULE_NAME}")  # noqa: T201

if PLUGIN_MODULE_NAME == "null":
    sys.exit(1)

bot = Bot(config_file=None)
bot.load_plugins(PLUGIN_MODULE_NAME)

print(f"bot.plugins: {bot.plugins}")  # noqa: T201

@bot.bot_run_hook
async def bot_run_hook(bot: Bot) -> None:
    """在 Bot 启动后直接退出。."""
    print("bot_run_hook")  # noqa: T201
    bot.should_exit.set()


if __name__ == "__main__":
    print("bot.run()")  # noqa: T201
    bot.run()


"""用于测试插件的脚本。"""
import sys

from alicebot.bot import Bot

MODULE_NAME = sys.argv[1]
TYPE = sys.argv[2]
if MODULE_NAME == "null":
    sys.stdout.write("Invalid MODULE_NAME value. Must be a valid Python module name.")
    sys.exit(1)

if TYPE not in {"plugin", "adapter", "bot"}:
    sys.stdout.write(
        "Invalid TYPE value. Must be one of 'plugin', 'adapter', or 'bot'."
    )
    sys.exit(1)

bot = Bot(config_file=None)

old_error_or_exception = Bot.error_or_exception


def error_or_exception(self: Bot, message: str, exception: Exception) -> None:
    """出现错误直接退出."""
    old_error_or_exception(self, message, exception)
    sys.stdout.write(message)
    sys.exit(1)


Bot.error_or_exception = error_or_exception

if TYPE == "plugin":
    bot.load_plugins(MODULE_NAME)
if TYPE == "adapter":
    bot.load_adapters(MODULE_NAME)
if TYPE == "bot":
    sys.exit(0)


@bot.bot_run_hook
async def bot_run_hook(bot: Bot) -> None:
    """在 Bot 启动后直接退出。"""
    if TYPE == "plugin":
        bot.should_exit.set()
    sys.exit(0)


if __name__ == "__main__":
    bot.run()

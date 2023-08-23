"""."""
import sys

from alicebot.bot import Bot

PLUGIN_MODULE_NAME = sys.argv[1]
TYPE = sys.argv[2]

if PLUGIN_MODULE_NAME == "null":
    sys.exit(1)

if TYPE != "plugin":
    sys.exit(1)

bot = Bot(config_file=None)
bot.load_plugins(PLUGIN_MODULE_NAME)


@bot.bot_run_hook
async def bot_run_hook(bot: Bot) -> None:
    """在 Bot 启动后直接退出。."""
    bot.should_exit.set()


if __name__ == "__main__":
    bot.run()


# pylint: disable=unused-argument, wrong-import-position

"""
Don't forget to enable inline mode with @BotFather

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Ensure that you have the .env file with env.example variables set at the root of the project.
Run python romsretro.py and then talk to the bot using inline mode.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging
import os
from dotenv import load_dotenv
from telegram import Update, __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_markdown_v2(
        r"Hola, soy @romsretrobot, un bot con funciones inline capaz de proporcionar juegos de"
        r" múltiples consolas de Nintendo, PlayStation y Sega\."
        "\n"
        r"Ya que soy un _inline bot_, puedes usarme en cualquier chat dentro de Telegram\."
        "\n\n"
        r"Para mayor información, usa el comando /help\."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_markdown_v2(
        r"*_Inline bot_\.\.\. ¿Qué significa esto?*"
        "\n\n"
        r"Significa que puedes usar mis funciones sin importar en qué lugar estés\."
        "\n"
        "Antes de empezar, usa el comando /settings para seleccionar la consola de la cual deseas"
        r"obtener juegos\."
        "\n"
        "Una vez hecho esto, solo debes escribir `@romsretrobot` en el campo de mensajes seguido"
        r"del nombre de la rom que deseas buscar\."
        "\n"
        "A continuación, debes elegir uno de los resultados y yo enviaré el archivo en en el chat"
        r"que te encuentres\."
    )


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(os.getenv("API_TOKEN")).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()

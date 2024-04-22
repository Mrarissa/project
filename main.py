import logging
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

NEWS_DATA = {
    "news1": {
        "title": "Breaking News 1",
        "url": "https://example.com/news1",
    },
    "news2": {
        "title": "Latest Update",
        "url": "https://example.com/news2",
    },
    "news3": {
        "title": "Important News Alert",
        "url": "https://example.com/news3",
    },
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Hi! I'm a news bot. Send me a query to get news articles.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("I can fetch news articles based on your queries. Just type your query.")


async def news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send all news articles."""
    news_text = ""
    for key, news_item in NEWS_DATA.items():
        news_text += f"{news_item['title']}\n{news_item['url']}\n\n"

    await update.message.reply_text(news_text)


async def command_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a list of available commands."""
    commands = [
        "/start - Start the bot",
        "/help - Get help about using the bot",
        "/news - Show all news articles",
    ]
    commands_text = "\n".join(commands)
    await update.message.reply_text(commands_text)


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.inline_query.query

    if not query:
        return

    results = []
    for key, news_item in NEWS_DATA.items():
        if query.lower() in news_item['title'].lower():
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid4()),
                    title=news_item['title'],
                    input_message_content=InputTextMessageContent(f"{news_item['title']}\n{news_item['url']}"),
                )
            )

    await update.inline_query.answer(results)


def main() -> None:
    application = Application.builder().token("Token").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("news", news))
    application.add_handler(CommandHandler("command", command_list))

    application.add_handler(InlineQueryHandler(inline_query))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

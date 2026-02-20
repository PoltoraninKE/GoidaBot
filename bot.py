import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


TOKEN = ""



def style_text(original: str) -> str:
    # 🇷🇺 чаще других
    EMOJIS = ['🇷🇺', '❤️', '✅', '💪', '⚡️', '🙏']
    WEIGHTS = [3, 1, 1, 1, 1, 1]  # увеличенный шанс для 🇷🇺

    replacements = {
        'В': 'V', 'в': 'V',
        'З': 'Z', 'з': 'Z',
        'B': 'V', 'b': 'V',
        '3': 'Z',
    }

    result = []

    for word in original.split():
        # Замена букв
        transformed = ''.join(replacements.get(c, c) for c in word)

        # Случайное количество эмодзи (0–3)
        emoji_count = random.randint(0, 3)

        if emoji_count > 0:
            emoji = random.choices(EMOJIS, weights=WEIGHTS, k=1)[0]
            emojis = emoji * emoji_count
        else:
            emojis = ""

        result.append(f"{transformed}{emojis}")

    return ' '.join(result)


async def ukras(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверяем, есть ли reply
    if update.message.reply_to_message and update.message.reply_to_message.text:
        original_text = update.message.reply_to_message.text
        styled_text = style_text(original_text)
        await update.message.reply_text(styled_text)
    else:
        await update.message.reply_text("Ответь на сообщение командой /goida")


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("goida", ukras))

    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
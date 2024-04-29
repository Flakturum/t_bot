# Импортирование библиотек
import logging
import random

from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ConversationHandler

# Уникальный токен
BOT_TOKEN = "7046924771:AAFA2JYlSgm4f976gGHJhxCYZxx9uDANU54"

# Логгирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Клавиатуры
general_keyboard = [['/start', '/stop'], ['/status', '/help'], ['/startGame']]
markup0 = ReplyKeyboardMarkup(general_keyboard, one_time_keyboard=False)

keyboard_1 = [['Ok'], ['/status', '/help', '/stop']]
markup1 = ReplyKeyboardMarkup(keyboard_1, one_time_keyboard=False)

keyboard_2 = [['Yes', 'No'], ['/status', '/help', '/stop']]
markup2 = ReplyKeyboardMarkup(keyboard_2, one_time_keyboard=False)

# Показатели сессии
time_gov = -1

people = -1
money = -1
army = -1
science = -1


async def next_step(update, context):
    scenes = ['Население', 'Бюджет', 'Армия', 'Наука']
    extra = random.choice(scenes)
    with open(f'data/Сценарии/{extra}', mode='r', encoding='UTF8') as scene:
        await update.message.reply_text(scene.read(), reply_markup=markup2)
        return 2


async def start(update, context):
    name = update.effective_user
    await update.message.reply_html(f'Здравствуйте, {name.mention_html()}. Добро пожаловать в ваше государство!',
                                    reply_markup=markup0)


async def startGame(update, context):
    global people, money, army, science, time_gov
    people = 50
    money = 50
    army = 50
    science = 50
    time_gov = 1
    await update.message.reply_text(f'Начало игры, все показатели на половине. Удачи!', reply_markup=markup1)
    return 1


async def help_command(update, context):
    with open('data/help.txt', mode='r', encoding='UTF8') as f:
        await update.message.reply_text(f.read())


async def status(update, context):
    await update.message.reply_text(f'Население: {people}\n'
                                    f'Бюджет: {money}\n'
                                    f'Армия: {army}\n'
                                    f'Наука: {science}\n'
                                    f'Времени у власти: {time_gov}')


async def stop(update, context):
    await update.message.reply_text("Сессия прервана. До новых встреч!")
    return ConversationHandler.END


def main():
    # Создаём объект Application.
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [CommandHandler('Ok', next_step)],
            2: [CommandHandler('Ok', next_step)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("startGame", startGame))
    application.add_handler(CommandHandler("stop", stop))

    # Запускаем приложение.
    application.run_polling()


if __name__ == '__main__':
    main()

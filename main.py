import telebot
import config
import sqlite3


def read_sql_column(record_num):
    try:
        con = sqlite3.connect("Aufgabe.db")
        cur = con.cursor()
        cur.execute("""SELECT * from tests""")
        records = cur.fetchall()
        answer = records[record_num]
        cur.close()
        return answer
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)


class MyBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)

        @self.bot.message_handler(commands=['start'])
        def start(message):
            try:
                keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

                trainingButton = telebot.types.KeyboardButton(text="Тренування")
                AnswersButton = telebot.types.KeyboardButton(text="Відповіді")

                keyboard.add(trainingButton, AnswersButton)
                self.bot.send_message(message.chat.id,
                                      "Я - телеграм бот, призначений допомогти тобі із підготовкою до "
                                      "Orientirungskurs.\n\nОбери варіант взаємодії.", reply_markup=keyboard)
            except TypeError as e:
                start(message)
                print("Wild Type Error occured! It uses \033[93m", e)
                print('\033[0m')
                pass

        @self.bot.message_handler(commands=['help'])
        def help_func(message):
            try:
                self.bot.send_message(message.chat.id,
                                      "Привіт. Ти щойно викликав інструкцію до використання цього бота.\n\n"
                                      "Наразі в мені реалізована лише одна функція Відповідей. Ти можеш викликати її "
                                      "через кнопку унизу екрану. Вона допоможе тобі швидко знаходити відповіді до "
                                      "конкретного тесту.\n\nНаразі проект на ранньому етапі розробки й можуть виникати"
                                      " складнощі, які будуть усунуті із часом.")
            except TypeError as e:
                start(message)
                print("Wild Type Error occured! It uses \033[93m", e)
                print('\033[0m')
                pass

        @self.bot.message_handler(content_types=['text'])
        def choose_menu(message):
            try:
                if message.text == 'Тренування':
                    self.bot.send_message(message.chat.id, 'Функціонал поки не реалізован. Обери іншу функцію.')
                elif message.text == 'Відповіді':

                    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                    closeButton = telebot.types.KeyboardButton(text="Меню")
                    keyboard.add(closeButton)

                    self.bot.send_message(message.chat.id, "Цей режим призначений для вивчення правильних відповідей. "
                                                           "Надсилай мені номер завдання, а я показиватиму тобі саме "
                                                           "питання, варіанти й правильне рішення. "
                                                           "\n\nОчікую номер тесту...", reply_markup=keyboard)
                    self.bot.register_next_step_handler(message, answers_nummer)
                else:
                    self.bot.send_message(message.chat.id, 'Мені нема що відповісти на це. Якщо тобі потрібна '
                                                           'допомога, уведи команду /help')
            except TypeError as e:
                start(message)
                print("Wild Type Error occured! It uses \033[93m", e)
                print('\033[0m')
                pass

        def answers_nummer(message):
            try:
                if message.text == "Меню" or message.text == "/start":
                    start(message)
                if message.text == "/help":
                    help_func(message)
                elif message.text:
                    if message.text in config.my_list:
                        a, b, c = read_sql_column(int(message.text) - 1)[1], read_sql_column(int(message.text) - 1)[2], \
                            read_sql_column(int(message.text) - 1)[3]
                        self.bot.send_message(message.chat.id, "{}\n{}\nAntwort: {}".format(a, b, c))
                        self.bot.register_next_step_handler(message, answers_nummer)
                    else:
                        self.bot.send_message(message.chat.id, 'На жаль, тесту із таким номером не існує. '
                                                               'Я очікую від тебе цифру від 1 до 300. Спробуй ще раз'
                                                               '\n\nЯкщо хочеш вийти, натисни кнопку "Меню", або '
                                                               'уведи команду /start')
                        self.bot.register_next_step_handler(message, answers_nummer)
                else:
                    self.bot.send_message(message.chat.id, 'Я очікую від тебе цифру від 1 до 300. Спробуй ще раз.'
                                                           '\n\nЯкщо хочеш вийти, натисни кнопку "Меню", або уведи '
                                                           'команду /start')
                    self.bot.register_next_step_handler(message, answers_nummer)
            except TypeError as e:
                self.bot.send_message(message.chat.id, 'Я очікую від тебе цифру від 1 до 300. Спробуй ще раз.'
                                                       '\n\nЯкщо хочеш вийти, натисни кнопку "Меню", або уведи '
                                                       'команду /start')
                self.bot.register_next_step_handler(message, answers_nummer)
                print("Wild Type Error occured! It uses \033[93m", e)
                print('\033[0m')
                pass

        self.bot.polling()


if __name__ == '__main__':
    bot = MyBot(config.ActiveBotToken)

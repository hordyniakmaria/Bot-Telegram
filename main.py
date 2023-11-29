import telebot
import requests
from bs4 import BeautifulSoup as Bs
from telebot import types

token = '6833838539:AAEAht707CbjcHPUHRU_GOrIHUjKn8Ut77w'
bot = telebot.TeleBot(token=token)


@bot.message_handler(commands=['start'])
def main(message):
    button = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                       row_width=2)
    button_first = types.KeyboardButton(text='OLX Search')
    button_second = types.KeyboardButton(text='Said Word')

    button.add(button_first, button_second)

    text = bot.send_message(message.chat.id, text="Доброго здоров'я!",
                            reply_markup=button)
    bot.register_next_step_handler(text, after_main)


def after_main(message):
    if message.text == 'OLX Search':
        word_search(message)
    elif message.text == 'Said Word':
        zero_return(message)


def zero_return(message):
    text = bot.send_message(message.chat.id, text='My Simple Bot For University')
    return text


def word_search(message):
    buttons = types.ReplyKeyboardRemove(selective=False)
    word = bot.send_message(message.chat.id, text='Що потрібно знайти:', reply_markup=buttons)
    bot.register_next_step_handler(word, search)


def search(word):
    url = f'https://www.olx.ua/d/uk/list/q-{word.text}/'
    print(url)
    response = requests.get(url)
    src = response.text
    soup = Bs(src, 'lxml')

    house_info = soup.find_all(class_='css-1sw7q4x')
    try:
        for house in house_info:
            get_house_title = house.find(class_='css-16v5mdi er34gjf0')
            house_name = get_house_title.text

            get_house_link = house.find(class_='css-rc5s2u')
            house_link = get_house_link.get("href")

            get_house_price = house.find(class_='css-10b0gli er34gjf0')
            house_price = get_house_price.text

            bot.send_message(word.chat.id,
                             text=f'{house_name}\n'
                                  f'Ціна: {house_price}\n'
                                  f"https://www.olx.ua/{house_link}\n")
    except AttributeError or NameError:
        print('Дані завершились')


if __name__ == '__main__':
    bot.polling(non_stop=True)

from random import randint
import os
import logging
import requests

from dotenv import load_dotenv
from telebot import TeleBot, types

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHAT_ID = 7950838601
URL = "https://api.thecatapi.com/v1/images/search"

bot = TeleBot(TOKEN)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def get_new_image():
    """
    Метод для получения случайного изображения котика.
    Возвращает URL изображения котика.
    Если запрос к API не удался, отправляет сообщение в чат
    и возвращает URL изображения собачки.
    """
    try:
        response = requests.get(URL)
    except Exception as error:
        logging.error(f"Ошибка при запросе к основному API: {error}")
        bot.send_message(
            CHAT_ID,
            "Мы не можем отправить вам котика из-за системной"
            " ошибки, так что мы отправим собачку",
        )
        new_url = "https://api.thedogapi.com/v1/images/search"
        response = requests.get(new_url)

    response = response.json()
    random_cat = response[0].get("url")
    return random_cat


@bot.message_handler(
        func=lambda m: m.text == "Автоматическая рассылка котиков")
def auto_cat(message):
    """
    Метод для обработки кнопки "Автоматическая рассылка котиков".
    Отправляет сообщение о том, что функция разрабатывается.
    """
    bot.send_message(message.chat.id, "Разрабатывается...")


@bot.message_handler(func=lambda m: m.text == "Случайное число 🎲")
def random_digit(message):
    """Метод для обработки кнопки "Случайное число 🎲"."""
    bot.send_message(message.chat.id, randint(1, 100))


@bot.message_handler(func=lambda m: m.text == "Показать котика 🐱")
def new_cat(message):
    """Метод для обработки кнопки "Показать котика 🐱"."""
    bot.send_photo(message.chat.id, get_new_image())


@bot.message_handler(commands=["start"])
def wake_up(message):
    """
    Метод для обработки команды /start.
    Отправляет приветственное сообщение и кнопки для взаимодействия.
    """
    chat_id = message.chat.id
    name = message.chat.first_name
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_automatic_cat = types.KeyboardButton("Автоматическая рассылка котиков")
    button_random_digit = types.KeyboardButton("Случайное число 🎲")
    button_newcat = types.KeyboardButton("Показать котика 🐱")
    keyboard.row(button_automatic_cat)
    keyboard.row(button_newcat, button_random_digit)
    bot.send_message(
        chat_id=chat_id,
        text=f"Привет, {name}. Посмотри, какого котика я тебе нашёл",
        reply_markup=keyboard,
    )
    bot.send_photo(chat_id, get_new_image())


@bot.message_handler()
def say_hi(message):
    """
    Метод для обработки сообщений, которые не соответствуют
    ни одной из кнопок.
    """
    print(message)
    chat_id = message.chat.id
    bot.send_message(
        chat_id,
        "Я не пониамаю, что ты имеешь в виду. Попробуй нажать на одну из кнопок ниже!",
    )


def send_message(message):
    """Метод для отправки сообщения в чат."""
    bot.send_message(message.chat.id, message)


def main():
    """Основная функция для запуска бота."""
    bot.send_message(CHAT_ID, "Бот запущен!")
    bot.polling()


if __name__ == "__main__":
    main()

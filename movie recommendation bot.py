import telebot
import requests
from bs4 import BeautifulSoup


def recommend(movie):
    results = []
    movie = movie.replace(" ", "+").lower()
    url = 'https://www.movie-map.com/' + movie
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    a = soup.findAll('div', attrs={'id': 'gnodMap'})[0]
    elements = []
    for x in a:
        elements.append(str(x))
    counter = sum('<a class="S"' in s for s in elements)
    for i in range(1, counter):
        name = a.find('a', attrs={'id': 's' + str(i)})
        results.append(name.text)
    results = ", ".join(results)
    return results


bot = telebot.TeleBot(token)


# users = []

@bot.message_handler(commands=['start'])
def handle_command(message):
    markup_inline= types.InlineKeyboardMarkup ()
    item_yes= types.InlineKeyboardButton (text= 'Accept', callback_data= 'yes')
    item_no= types.InlineKeyboardButton (text= 'Refuse', callback_data= 'no')
    markup_inline.add (item_yes, item_no)
    bot.send_message (message.chat.id, 'Make your choice', reply_markup= markup_inline)
    bot.reply_to(message, "Salam, xoş gəlmisiniz! Sevdiyiniz filmi daxil edin")


@bot.message_handler(func=lambda message: True)
def handle_all_message(message):
    # name = bot.get_me()
    # users.append(name)
    try:
        movie = recommend(message.text)
        bot.send_message(chat_id=message.chat.id, text=movie)
    except:
        bot.reply_to(message,
                     "Daxil etdiyiniz filmə oxşar film tapa bilmədik, zəhmət olmasa filmin adını düzgün daxil etdiyinizdən əmin olun :)")


bot.polling()
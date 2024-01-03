import telebot
from telebot import types
import config as cfg
from game import Game

bot = telebot.TeleBot(cfg.TELEGRAM_TOKEN)

active_games = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    '''Handle '/start' '''
    markup = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton(text="Начать игру", callback_data='Начать игру')
    help_button = types.InlineKeyboardButton(text="Научиться различать...", 
                                             url='https://pikabu.ru/story/kak_otlichit_zaytsarusaka_ot_zaytsabelyaka_5682135')
    markup.add(start_button, help_button)
    bot.send_message(message.chat.id, 
                     '''Привет, {0.first_name}! 
Если ты пока не умеешь отличать беляков от русаков, то перейди по ссылке, нажав на кнопку "Научиться различать...". 
Чтобы сыграть, нажми на кнопку "Начать игру"'''.format(message.from_user), 
                     reply_markup=markup)
    


@bot.message_handler(commands=['help'])
def send_help_url(message):
    '''Handle '/help' '''
    markup = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton(text="Начать игру заново", callback_data='Начать игру')
    help_button = types.InlineKeyboardButton(text="Научиться различать...", 
                                             url='https://pikabu.ru/story/kak_otlichit_zaytsarusaka_ot_zaytsabelyaka_5682135')
    markup.add(start_button, help_button)
    bot.send_message(message.chat.id, '''Если хочешь начать игру с начала, нажми на "Начать игру заново". 
Если хочешь уточнить, чем отличаются беляки от русаков, перейди по ссылке, нажав на кнопку "Научиться различать..."''', 
                     reply_markup=markup)



@bot.message_handler(content_types=['text', 'audio', 'document', 'animation', 'game', 'photo', 'sticker', 'video', 
                                    'video_note', 'voice', 'location', 'contact', 'venue', 'dice', 'story', 'poll'])
def default_answer(message):
    '''Handle all inputs'''
    markup = types.InlineKeyboardMarkup()
    start_button = types.InlineKeyboardButton(text="Начать игру заново", callback_data='Начать игру')
    help_button = types.InlineKeyboardButton(text="Научиться различать...", 
                                             url='https://pikabu.ru/story/kak_otlichit_zaytsarusaka_ot_zaytsabelyaka_5682135')
    markup.add(start_button, help_button)
    bot.send_message(message.chat.id, 
                     text='''Прости, я не умею распознавать текст, документы и выполнять любые команды, отличающиеся от запрограммированных 😔 
Если хочешь начать игру с начала, нажми на "Начать игру заново". 
Если хочешь уточнить, чем отличаются беляки от русаков, перейди по ссылке, нажав на кнопку "Научиться различать..."''', 
                     reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data == 'Начать игру')
def start_callback_inline(call):
    '''
    The beginning of the game.
    Game shows 10 random photos and ask question with two answer options.
    To set more than 10 photos you need to write new number as 'active_games[call.from_user.id] = Game(max_iter=new_number)'
    At the end of the game bot shows result and offers to continue the game.
    This method create an empty class Game() for the user and store it into global active_games.
    Method shows 3 buttons to choose game difficulty: ['Низкий', 'Средний', 'Тяжелый']
    '''
    global active_games

    # Block last button
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.data, reply_markup=None)

    # Difficulty buttons
    active_games[call.from_user.id] = Game()
    markup = types.InlineKeyboardMarkup()
    easy_button   = types.InlineKeyboardButton(text="Низкий", callback_data='Низкий')
    middle_button = types.InlineKeyboardButton(text="Средний", callback_data='Средний')
    hard_button   = types.InlineKeyboardButton(text="Тяжелый", callback_data='Тяжелый')
    markup.add(easy_button, middle_button, hard_button)
    bot.send_message(call.message.chat.id, 'Выбери уровень сложности', reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data in ['Низкий', 'Средний', 'Тяжелый'])
def difficulty_callback_inline(call):
    '''
    The beginning of the game.
    Download photo's URLs, labels and ML model's predictions for choosen difficulty.
    Display first question of the game with two options: ['Беляк', 'Русак']
    '''
    global active_games

    # Block last button
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.data, reply_markup=None)
    
    # Try-exception block for the case of problems with the Internet
    try:
        # Upload dataset of photos, labels, model predictions for choosen difficulty
        active_games[call.from_user.id].set_difficulty(call.data)
    
        # Show current photo and buttons to choose correct answer
        img = open(active_games[call.from_user.id].get_curr_photo_url(), 'rb')
        bot.send_photo(call.message.chat.id, img)
        markup = types.InlineKeyboardMarkup()
        timidus_button = types.InlineKeyboardButton(text="Беляк", callback_data='Беляк')
        europaeus_button = types.InlineKeyboardButton(text="Русак", callback_data='Русак')
        markup.add(timidus_button, europaeus_button)
        bot.send_message(call.message.chat.id, 'На фото беляк или русак?', reply_markup=markup)
    except:
        markup = types.InlineKeyboardMarkup()
        start_button = types.InlineKeyboardButton(text="Начать игру заново", callback_data='Начать игру')
        markup.add(start_button)
        bot.send_message(call.message.chat.id, text='Простите, произошел сбой 😔 Пожалуйста, начните игру заново', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in ['Беляк', 'Русак'])
def answer_callback_inline(call):
    '''
    The continuation and the end of the game.
    While current iter is less than max_iters, method display question with two options: ['Беляк', 'Русак']
    If current iter == max_iters, show game result and offers to continue the game
    '''
    global active_games

    # Block last button
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.data, reply_markup=None)
    
    # Try-exception block for the case of problems with the Internet
    try:
        # Continuation of the game
        if active_games[call.from_user.id].get_iter() < active_games[call.from_user.id].max_iters-1:
            # Check last answer and show correct value
            bot.send_message(call.message.chat.id, active_games[call.from_user.id].check_answer(call.data))
            # Show current photo and buttons to choose correct answer
            img = open(active_games[call.from_user.id].get_curr_photo_url(), 'rb')
            bot.send_photo(call.message.chat.id, img)
            markup = types.InlineKeyboardMarkup()
            timidus_button = types.InlineKeyboardButton(text="Беляк", callback_data='Беляк')
            europaeus_button = types.InlineKeyboardButton(text="Русак", callback_data='Русак')
            markup.add(timidus_button, europaeus_button)
            bot.send_message(call.message.chat.id, 'На фото беляк или русак?', reply_markup=markup)
        # End of the game
        else:
            # Check last answer and show correct value
            bot.send_message(call.message.chat.id, active_games[call.from_user.id].check_answer(call.data))
            # Buttons for new game
            markup = types.InlineKeyboardMarkup()
            start_button = types.InlineKeyboardButton(text="Сыграть еще раз", callback_data='Начать игру')
            help_button = types.InlineKeyboardButton(text="Научиться различать...", 
                                                     url='https://pikabu.ru/story/kak_otlichit_zaytsarusaka_ot_zaytsabelyaka_5682135')
            markup.add(start_button, help_button)
            bot.send_message(call.message.chat.id, text=active_games[call.from_user.id].get_result(), reply_markup=markup)
    except:
        markup = types.InlineKeyboardMarkup()
        start_button = types.InlineKeyboardButton(text="Начать игру заново", callback_data='Начать игру')
        markup.add(start_button)
        bot.send_message(call.message.chat.id, text='Простите, произошел сбой 😔 Пожалуйста, начните игру заново', reply_markup=markup)


bot.polling(none_stop=True)
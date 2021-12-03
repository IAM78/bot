import telebot
import random
from khayyam import JalaliDatetime
import qrcode
from gtts import gTTS


bot = telebot.TeleBot('5072345535:AAHZ-mzIJC9W-p3sMyHmdmNMBjwTC0_NlTI')
number=0

markup=None

@bot.message_handler(commands=['start'])
def register(message):
    bot.reply_to(message, "Welcome " +  message.from_user.first_name +  " !")

@bot.message_handler(commands=['max'])
def max_arr(message):
    arr=bot.send_message(message.chat.id,'Enter your array for example:1,35,3,4')
    bot.register_next_step_handler(arr,find_max)
    
def find_max(message):    
    numbers=list(map(int,message.text.split(',')))
    bot.send_message(message.chat.id,max(numbers))

@bot.message_handler(commands=['maxpos'])
def max_arr_(message):
    arr=bot.send_message(message.chat.id,'Enter your array for example :1,35,3,4')
    bot.register_next_step_handler(arr,max_index_array)
    
def max_index_array(message):    
    numbers=list(map(int,message.text.split(',')))
    bot.send_message(message.chat.id,numbers.index(max(numbers)))

@bot.message_handler(commands=['game'])
def game(message):
    global number,markup
    number = random.randint(0,100)
    bot.reply_to(message,"number Please between ") 

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    text = telebot.types.KeyboardButton('repeat')
    markup.add(text)

    bot.register_next_step_handler(message , game_compeletation)
   
def game_compeletation(message):
    global markup
    if message.text=='repeat':
        message=bot.send_message(message.chat.id,"resetting game")
        game(message)
    elif int(message.text) > number:
        bot.reply_to(message, "is loweer!",reply_markup=markup)
        bot.register_next_step_handler(message,game_compeletation)
    elif int(message.text) < number :
        bot.reply_to(message, "is bigger!",reply_markup=markup)
        bot.register_next_step_handler(message , game_compeletation)
    elif int(message.text) == number:
        bot.reply_to(message, "you win")
        markup=None




@bot.message_handler(commands=['age'])
def age(message):
    bot.reply_to(message,"Please enter your birth date : ") 
    bot.register_next_step_handler(message ,age_cal)

def age_cal(message):
    date = message.text.split('/')
    dif = JalaliDatetime.now()-JalaliDatetime(date[0],date[1],date[2])
    dif=str(dif).split()
    days=int(dif[0])
    bot.reply_to(message,days//365)

@bot.message_handler(commands=['qrcode'])
def text_to_qrcode(message):
    bot.reply_to(message,"Enter your text :") 
    bot.register_next_step_handler(message ,toqrcode)

def toqrcode(message):
    img = qrcode.make(message) 
    img.save("qrcode.png")
    photo = open("qrcode.png", 'rb')
    bot.send_photo(message.chat.id, photo)


@bot.message_handler(commands=['voice'])
def voice(message):
    bot.reply_to(message,"please enter your text :") 
    bot.register_next_step_handler(message , text_to_voice)

def text_to_voice(message):
    voiceobj = gTTS(text=message.text ,  lang= 'en', slow=False)
    voiceobj.save("voice.ogg")
    voiceobj = open("voice.ogg", 'rb')
    bot.send_voice(message.chat.id,voiceobj)

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message,"""
    /start
    /game 
    /max
    /maxpos
    /age
    /voice
    /qrcode
    /help
    """)


bot.infinity_polling()
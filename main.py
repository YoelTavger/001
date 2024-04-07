import telebot
import random
import threading
from searchCar import searchCar
import time

TOKEN = '6309037100:AAFz7e8FmI53--cM1s0oR6cXIw1ECcxAyAU'
bot = telebot.TeleBot(TOKEN)
texts = [
    "המספר הבא: {number}",
    "יאללה חפשו את: {number}",
    "בא נראה מי מוצא את: {number}",
    "מי המלך שמוצא: {number}",
    "תנו לי ב: {number}",
    "זה היה קל תביאו: {number}",
    "איפה: {number}",
    "צלמו לי: {number}",
    "מי יהיה מספיק אמיץ למצוא: {number}",
]
random_number = random.randint(1, 1000)

def send_loading_message(chat_id, random_number):
    message = bot.send_message(chat_id, "מעבד...")

    i = 0
    while True:
        time.sleep(1)
        dots = '.' * (i + 1)
        bot.edit_message_text(f"מעבד{dots}", chat_id, message.message_id)
        i = (i + 1) % 3

        newText = searchCar()
        if newText:
            break

    bot.delete_message(chat_id, message.message_id)
@bot.message_handler(func=lambda message: True, content_types=['photo'])
def handle_photos(message):
    
    global random_number
    try:
        if message.chat.type == "group" or message.chat.type == "supergroup":
            file_id = message.photo[-1].file_id
            file_info = bot.get_file(file_id)
            file_path = file_info.file_path
            downloaded_file = bot.download_file(file_path)
            with open(f"image.jpg", 'wb') as new_file:
                new_file.write(downloaded_file)

            threading.Thread(target=send_loading_message, args=(message.chat.id, random_number)).start()

            newText = searchCar()
            print(newText)

            if newText and str(random_number).zfill(3) in newText:
                bot.reply_to(message, f" המספר שזוהה: {newText}")
                bot.reply_to(message, "Success")
                random_number = random.randint(0, 1000)
                random_text = random.choice(texts)
                response_text = random_text.format(number=random_number)
                bot.send_message(message.chat.id, response_text)
            else:
                bot.reply_to(message, f" המספר שזוהה: {newText}")
                bot.reply_to(message, "המספר המבוקש לא נמצא בתמונה, \nנסה לשלוח תמונה אחרת או תמונה במצב ברור יותר")
    except Exception as e:
        print(f"An error occurred: {e}")

@bot.message_handler(func=lambda message: "/number" in message.text)
def respond_to_what(message):
    global random_number
    user_name = message.from_user.first_name
    bot.reply_to(message, f"{user_name}, המספר הנוכחי הוא: {random_number}")

@bot.message_handler(func=lambda message: "/next" in message.text)
def replace_number(message):
    global random_number
    random_number = random.randint(0, 1000)
    user_name = message.from_user.first_name
    bot.reply_to(message, f"{user_name}, המספר הוחלף.\nהמספר החדש הוא: {random_number}")

if __name__ == "__main__":
    bot.polling(none_stop=True)


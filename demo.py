import telebot
import requests
import os

# הכנס את טוקן הבוט שלך מטלגרם
TELEGRAM_BOT_TOKEN = '6309037100:AAFz7e8FmI53--cM1s0oR6cXIw1ECcxAyAU'
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# הכנס את מפתח ה-API של Plate Recognizer
PLATE_RECOGNIZER_API_KEY = '3a0effff73919f898b69ac65a32dc12347769564'

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "ברוך הבא! שלח תמונה כדי לקבל מידע על לוח הרישוי בה.")

@bot.message_handler(content_types=['photo'])
def handle_image(message):
    # בדוק אם קיבלנו תמונה
    if message.photo:
        # נשתמש בתמונה הגדולה ביותר (האחרונה ברשימה)
        photo_file_id = message.photo[-1].file_id
        photo_file_info = bot.get_file(photo_file_id)

        # הורד את התמונה
        photo_url = f'https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{photo_file_info.file_path}'
        photo_path = 'image.jpg'
        download_photo(photo_url, photo_path)

        # שלח את התמונה ל-Plate Recognizer
        plate_data = recognize_plate(photo_path)

        # שלח את תוצאות הזיהוי למשתמש
        bot.reply_to(message, f'זיהוי לוח רישוי: {plate_data}')
    else:
        bot.reply_to(message, 'אנא שלח תמונה כדי לבצע זיהוי רישוי.')

def download_photo(url, path):
    response = requests.get(url)
    with open(path, 'wb') as file:
        file.write(response.content)

def recognize_plate(image_path):
    url = 'https://api.platerecognizer.com/v1/plate-reader/'
    headers = {'Authorization': f'Token {PLATE_RECOGNIZER_API_KEY}'}
    files = {'upload': open(image_path, 'rb')}

    response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        plate_data = response.json()
        return f"רכב: {plate_data['results'][0]['vehicle']['make_model']}, לוח רישוי: {plate_data['results'][0]['plate']}"
    else:
        return 'לא ניתן היה לזהות לוח רישוי.'

if __name__ == '__main__':
    bot.polling(none_stop=True)

from telegram import Poll, Bot
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
import os
import logging

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

quiz_questions = [
    ("भारत के पहले प्रधानमंत्री कौन थे?", ["लाल बहादुर शास्त्री", "इंदिरा गांधी", "जवाहरलाल नेहरू", "राजीव गांधी"]),
    ("भारत का राष्ट्रीय पशु कौन सा है?", ["गाय", "शेर", "बाघ", "हाथी"]),
]

def send_quiz():
    for question, options in quiz_questions:
        bot.send_poll(
            chat_id=CHAT_ID,
            question=question,
            options=options,
            is_anonymous=False,
            type=Poll.QUIZ,
            correct_option_id=None,
        )

scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
for hour in [9, 11, 13, 16, 20]:
    scheduler.add_job(send_quiz, 'cron', hour=hour, minute=0)
scheduler.start()

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    send_quiz()  # Optional initial test quiz
    app.run(host="0.0.0.0", port=8080)
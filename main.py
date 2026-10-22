import os
import telebot
from yt_dlp import YoutubeDL

TOKEN = "8920653591:AAHIqnNsiyT5u-kGGDIzJQ5rPP3Ke8eTG9c"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
  bot.reply_to(
      message,
      "Salom! Menga YouTube havolasini yuboring, men uni MP3 qilib tashlab"
      " beraman.",
  )


@bot.message_handler(func=lambda message: True)
def download_music(message):
  url = message.text.strip()
  if not url.startswith("http"):
    bot.reply_to(message, "Iltimos, to'g'ri YouTube havolasini (linkini) yuboring!")
    return

  msg = bot.reply_to(message, "📥 Qo'shiq yuklab olinmoqda, biroz kuting...")

  try:
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "outtmpl": "song.%(ext)s",
        "quiet": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
      ydl.download([url])

    audio_file = "song.mp3"
    if os.path.exists(audio_file):
      with open(audio_file, "rb") as audio:
        bot.send_audio(
            message.chat.id, audio, caption="🎵 @XC_music_bot orqali yuklandi"
        )
      os.remove(audio_file)
      bot.delete_message(message.chat.id, msg.message_id)
    else:
      bot.edit_message_text(
          "❌ Xatolik: Fayl topilmadi.", message.chat.id, msg.message_id
      )

  except Exception as e:
    bot.edit_message_text(
        f"❌ Xatolik yuz berdi: {e}", message.chat.id, msg.message_id
    )


bot.infinity_polling()

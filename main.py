import os
import requests
import telebot

# 1. आपका बॉट टोकन
BOT_TOKEN = "9230801222:AAELbvk_AC4LOPsM6q747NromJcalHOFldI"

# 2. आपकी असली Telegram ID (Admin)
ADMIN_ID = 8417306426

# 3. आपका सीक्रेट पासवर्ड
SECRET_CODE = "kaushal123"

bot = telebot.TeleBot(BOT_TOKEN)
approved_users = {ADMIN_ID}


def unshorten_url(url):
  try:
    # ब्राउज़र की तरह दिखने के लिए हेडर जोड़ रहे हैं ताकि शॉर्टनर ब्लॉक न करे
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
            " like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.5",
    }

    session = requests.Session()
    response = session.get(
        url, headers=headers, allow_redirects=True, timeout=15
    )

    # अगर बीच में कोई रीडायरेक्ट हिस्ट्री है तो आखिरी और सही URL निकालें
    if response.history:
      final_url = response.url
      return final_url
    else:
      return response.url

  except Exception as e:
    return f"लिंक चेक करने में समस्या आई: {str(e)}"


@bot.message_handler(commands=["start"])
def send_welcome(message):
  user_id = message.from_user.id
  if user_id in approved_users:
    bot.reply_to(
        message,
        "नमस्ते मालिक! 👋\nबॉट अपडेट हो गया है। कोई भी शॉर्ट लिंक भेजें!",
    )
  else:
    bot.reply_to(
        message,
        "🔒 **प्राइवेट बॉट!**\nयूनिक कोड भेजने के लिए कमांड दें:\n`/auth"
        " kaushal123`",
        parse_mode="Markdown",
    )


@bot.message_handler(commands=["auth"])
def authenticate_user(message):
  user_id = message.from_user.id
  text = message.text.strip()

  try:
    parts = text.split(" ", 1)
    entered_code = parts[1]
  except IndexError:
    bot.reply_to(
        message,
        "⚠️ सही फॉर्मेट में लिखें। उदाहरण:\n`/auth kaushal123`",
        parse_mode="Markdown",
    )
    return

  if entered_code == SECRET_CODE:
    approved_users.add(user_id)
    bot.reply_to(message, "🎉 परमिशन मिल गई है! अब लिंक भेजें।")
  else:
    bot.reply_to(message, "❌ गलत कोड!")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  user_id = message.from_user.id

  if user_id not in approved_users:
    bot.reply_to(
        message, "🚫 परमिशन नहीं है! पहले `/auth kaushal123` भेजें।"
    )
    return

  text = message.text.strip()
  if text.startswith("http://") or text.startswith("https://"):
    wait_msg = bot.reply_to(message, "⏳ लिंक बाईपास किया जा रहा है...")
    final_url = unshorten_url(text)
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=wait_msg.message_id,
        text=f"✅ **नतीजा / असली लिंक:**\n`{final_url}`",
        parse_mode="Markdown",
    )
  else:
    bot.reply_to(message, "⚠️ कृपया सही URL (`http://` या `https://`) भेजें।")


print("Advanced Unshortener Bot is running...")
bot.infinity_polling()

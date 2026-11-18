import os
import requests
import telebot

# आपका बॉट टोकन
BOT_TOKEN = "9230801222:AAELbvk_AC4LOPsM6q747NromJcalHOFldI"

# आपकी असली Telegram ID (आप Admin हैं)
ADMIN_ID = 8417306426

# आपका सीक्रेट पासवर्ड (दूसरों के लिए)
SECRET_CODE = "kaushal123"

bot = telebot.TeleBot(BOT_TOKEN)
approved_users = {ADMIN_ID}


def unshorten_url(url):
  try:
    response = requests.get(url, allow_redirects=True, timeout=10, stream=True)
    return response.url
  except Exception as e:
    return f"लिंक चेक करने में समस्या आई: {str(e)}"


@bot.message_handler(commands=["start"])
def send_welcome(message):
  user_id = message.from_user.id
  if user_id in approved_users:
    bot.reply_to(
        message,
        "नमस्ते मालिक! 👋\nआप वेरिफाइड हैं। मुझे कोई भी शॉर्ट लिंक भेजें, मैं असली"
        " लिंक ढूंढ कर दे दूंगा।",
    )
  else:
    bot.reply_to(
        message,
        "🔒 **प्राइवेट बॉट!**\nइस बॉट को इस्तेमाल करने के लिए आपके पास यूनिक कोड"
        " होना चाहिए।\n\nकृपया इस तरह कमांड भेजें:\n`/auth kaushal123`",
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
        "⚠️ कृपया सही फॉर्मेट में लिखें। उदाहरण:\n`/auth kaushal123`",
        parse_mode="Markdown",
    )
    return

  if entered_code == SECRET_CODE:
    approved_users.add(user_id)
    bot.reply_to(
        message,
        "🎉 **बधाई हो!**\nपरमिशन मिल गई है। अब आप इस बॉट का इस्तेमाल कर सकते"
        " हैं। कोई भी लिंक भेजें!",
    )
  else:
    bot.reply_to(
        message, "❌ गलत कोड! कृपया सही यूनिक कोड दर्ज करें।"
    )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  user_id = message.from_user.id

  if user_id not in approved_users:
    bot.reply_to(
        message,
        "🚫 आपके पास इस बॉट को इस्तेमाल करने की परमिशन नहीं है!\nकृपया पहले"
        " `/auth kaushal123` लिखकर एक्सेस लें።",
    )
    return

  text = message.text.strip()
  if text.startswith("http://") or text.startswith("https://"):
    wait_msg = bot.reply_to(message, "⏳ लिंक चेक किया जा रहा है...")
    final_url = unshorten_url(text)
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=wait_msg.message_id,
        text=f"✅ **असली लिंक:**\n`{final_url}`",
        parse_mode="Markdown",
    )
  else:
    bot.reply_to(
        message,
        "⚠️ कृपया एक सही URL भेजें जो `http://` या `https://` से शुरू होता हो।",
    )


print("Secured Bot with Auth Code is running...")
bot.infinity_polling()

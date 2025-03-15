import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import requests

# توكن البوت
TOKEN = '7724221611:AAGr7CfMCEluBwpoW33rdxYRHRSfodnEh7k'

# API لأسعار الصرف
EXCHANGE_RATE_API = 'https://api.exchangerate-api.com/v4/latest/USD'

# تفعيل اللوغينغ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# دالة للحصول على أسعار الصرف
def get_exchange_rates():
    response = requests.get(EXCHANGE_RATE_API)
    data = response.json()
    return data['rates']

# دالة لبدء البوت
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('مرحبًا! أنا بوت صرف العملات. استخدم /rates لرؤية أسعار الصرف.')

# دالة لعرض أسعار الصرف
def rates(update: Update, context: CallbackContext) -> None:
    rates = get_exchange_rates()
    message = "أسعار الصرف الحالية:\n"
    for currency, rate in rates.items():
        message += f"{currency}: {rate}\n"
    update.message.reply_text(message)

# دالة لتبديل العملات
def exchange(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="اختر العملة التي تريد التحويل منها:")

# دالة لمعالجة الأخطاء
def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f'Update {update} caused error {context.error}')

# الدالة الرئيسية لتشغيل البوت
def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # تعريف الأوامر
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("rates", rates))
    dispatcher.add_handler(CallbackQueryHandler(exchange))

    # معالجة الأخطاء
    dispatcher.add_error_handler(error)

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

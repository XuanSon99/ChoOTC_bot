from telegram import *
from telegram.ext import *
import requests
import json
from types import SimpleNamespace
import math

client = "🙎🏼‍♂️ Khách hàng"
merchant = "👨🏻‍💼 Merchant"
kyc = "👨‍💻 KYC"

domain = "https://chootc.com"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    buttons = [[KeyboardButton(client), KeyboardButton(merchant)], [
        KeyboardButton(kyc)]]

    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Chọn phương án bên dưới. Bạn là?", reply_markup=reply_markup)


async def messageHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.effective_user.username
    chat_id = update.effective_chat.id

    if update.message.chat.type != "private":
        return

    if username is None:
        await context.bot.send_message(chat_id, text="Vui lòng cập nhật Username của bạn!")
        return

    if client in update.message.text:
        link = f"{domain}/captcha/{username}-{chat_id}"

        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='Xác minh', url=link)]],
        )

        text = f"<b>🔥 Xác minh bạn không phải Robot!</b> \n\n<i>Nhấn vào nút bên dưới để xác minh</>"

        await context.bot.send_message(chat_id, text=text, reply_markup=reply_markup, parse_mode=constants.ParseMode.HTML)

    if merchant in update.message.text or kyc in update.message.text:
        link = f"{domain}/kyc/{username}-{chat_id}"

        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='Tiến hành KYC', url=link)]],
        )

        text = "<b>🔥 Xác minh danh tính của bạn!</b> \n \n<i>Hãy thực hiện theo các bước dưới đây</i> \n1. Chuẩn bị thiết bị của bạn: cho phép trình duyệt truy cập định vị, camera và micro. \n2. Nhấn vào nút <b>Tiến hành KYC</b>. \n3. Làm theo hướng dẫn trên trình duyệt."

        await context.bot.send_message(chat_id, text=text, reply_markup=reply_markup, parse_mode=constants.ParseMode.HTML)

    if "/uytin" in update.message.text:

        if "@" in update.message.text:

            username = update.message.text[8:]
            res = requests.get(
                f"{domain}/api/check-user/{username}")

            if res.text == "":
                text = f"@{username} không tồn tại trong hệ thống!"
            else:
                text = f"@{username} đã giao dịch thành công {res.json()['transaction']} lần"
            await context.bot.send_message(chat_id, text=text)
            return

        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='|<', callback_data='first'),
             InlineKeyboardButton(text='<', callback_data='prev'),
             InlineKeyboardButton(text='>', callback_data='next'),
             InlineKeyboardButton(text='>|', callback_data='last')]],
        )

        await context.bot.send_message(chat_id, text=content(1), reply_markup=reply_markup, parse_mode=constants.ParseMode.HTML)

    if "/kyc" in update.message.text:
        username = update.message.text[6:]
        res = requests.get(
            f"{domain}/api/check-user/{username}")

        if res.text == "":
            text = f"@{username} chưa gửi thông tin KYC!"
            await context.bot.send_message(chat_id, text=text)
            return

        if res.json()['kyc'] == 'pending':
            text = f"@{username} KYC đang chờ xét duyệt!"
        if res.json()['kyc'] == 'success':
            text = f"@{username} đã KYC thành công!"
        if res.json()['kyc'] == 'failed':
            text = f"@{username} KYC thất bại! Liên hệ Admin để được hỗ trợ."

        await context.bot.send_message(chat_id, text=text)


def content(page):
    res = requests.get(f"{domain}/api/get-top?page={page}")

    text = "<b>🔥 Xếp hạng uy tín 🔥</b>\n\n<i>Xếp hạng dựa theo số lần giao dịch thành công</i>\n"

    for index, item in enumerate(res.json()['data']):
        text += f"{index-1+res.json()['current_page']*res.json()['per_page']}: @{item['username']} ({item['transaction']} lần)\n"

    text += f"\nTrang: {page}/{math.ceil(res.json()['total']/res.json()['per_page'])}"
    return text


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_id = update.effective_message.id
    chat_id = update.effective_chat.id
    page = update.effective_message.text[-3:]
    current_page = int(page[:1])
    last_page = int(page[-1:])

    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text='|<', callback_data='first'),
          InlineKeyboardButton(text='<', callback_data='prev'),
          InlineKeyboardButton(text='>', callback_data='next'),
          InlineKeyboardButton(text='>|', callback_data='last')]],
    )

    query = update.callback_query
    await query.answer()

    if query.data == "first":
        if current_page == 1:
            return
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=content(1), reply_markup=reply_markup, parse_mode=constants.ParseMode.HTML)
    if query.data == "prev":
        if current_page > 1:
            p = current_page - 1
        else:
            return
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=content(p), reply_markup=reply_markup, parse_mode=constants.ParseMode.HTML)
    if query.data == "next":
        if current_page < last_page:
            p = current_page + 1
        else:
            return
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=content(p), reply_markup=reply_markup, parse_mode=constants.ParseMode.HTML)
    if query.data == "last":
        if current_page == last_page:
            return
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=content(page[-1:]), reply_markup=reply_markup, parse_mode=constants.ParseMode.HTML)


app = ApplicationBuilder().token(
    "5839467716:AAFZLmO_BB9XTuws32wvj72q299PhEsXJLQ").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.ALL, messageHandler))

app.run_polling()

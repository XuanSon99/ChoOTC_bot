from telegram import *
from telegram.ext import *
import requests
import json
from types import SimpleNamespace
import math

kyc = "👨‍💻 Xác minh KYC"
uytin = "💎 DS Uy tín"

domain = "https://chootc.com"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    buttons = [[KeyboardButton(kyc), KeyboardButton(uytin)]]

    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Chào mừng bạn đến với <b>Chợ OTC VN</b>. Hãy chọn phương án bên dưới:", reply_markup=reply_markup, parse_mode=constants.ParseMode.HTML)


async def messageHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.effective_user.username
    chat_id = update.effective_chat.id

    if update.message.chat.username in ["minatabar", "quocusdt"]:

        if "/postwithbutton" in update.message.text:
            text = update.message.text.split("|")

            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton(
                    text=text[2], url="https://t.me/ChoOTCVN_bot")]],
            )

            await context.bot.send_message(chat_id="-1001871429218", text=text[1], reply_markup=reply_markup, parse_mode=constants.ParseMode.HTML)

        if "/postnormal" in update.message.text:
            text = "<b>Thành viên uy tín là ai ?</b>\nLà những thành viên buôn bán thâm niên, chuyên nghiệp, có uy tín cao trong cộng đồng.\n<b>Làm thế nào để trở thành TV uy tín ?</b>\n- Không ít hơn 6 tháng hoạt động buôn bán tại Chợ OTC VN.\n- Không ít hơn 30 lần giao dịch thành công.\n- Và ít nhất 3 admin cho bạn uy tín.\n\n<i>Hãy chat ngay với bot để kiểm tra danh sách uy tín</i>"

            await context.bot.send_message(chat_id="-1001871429218", text=text, parse_mode=constants.ParseMode.HTML)

    if update.message.chat.type != "private":

        if "/uytin" in update.message.text:
            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='|<', callback_data='first'),
                  InlineKeyboardButton(text='<', callback_data='prev'),
                  InlineKeyboardButton(text='>', callback_data='next'),
                  InlineKeyboardButton(text='>|', callback_data='last')]],
            )

            await context.bot.send_message(chat_id, text=content(1), reply_markup=reply_markup, parse_mode=constants.ParseMode.HTML)
        return

    if username is None:
        await context.bot.send_message(chat_id, text="Vui lòng cập nhật Username của bạn!")
        return

    if kyc in update.message.text:
        link = f"{domain}/kyc/{username}-{chat_id}"

        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='Tiến hành KYC', url=link)]],
        )

        text = "<b>🔥 Xác minh danh tính của bạn!</b> \n \n<i>Hãy thực hiện theo các bước dưới đây</i> \n1. Chuẩn bị thiết bị của bạn: cho phép trình duyệt truy cập định vị và camera. \n2. Nhấn vào nút <b>Tiến hành KYC</b>. \n3. Làm theo hướng dẫn trên trình duyệt."

        await context.bot.send_message(chat_id, text=text, reply_markup=reply_markup, parse_mode=constants.ParseMode.HTML)

    if "/uytin" in update.message.text or uytin in update.message.text:

        if "@" in update.message.text:

            username = update.message.text[8:]
            res = requests.get(
                f"{domain}/api/check-user/{username}")

            if res.text == "":
                text = f"@{username} không tồn tại trong hệ thống!"
                await context.bot.send_message(chat_id, text=text)
                return

            if res.json()['transaction'] is None:
                text = f"@{username} chưa có giao dịch nào thành công"
            else:
                text = f"@{username} đã giao dịch thành công {res.json()['transaction']} lần"

                if res.json()['reputation'] == 'yes':
                    text += " - Uy tín 💎"

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

        if "@" not in update.message.text:
            await context.bot.send_message(chat_id, text="Sai cú pháp, phải có @ trước Username!")
            return

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
        text += f"- @{item['username']} ({item['transaction']} lần)"
        if item['reputation'] == 'yes':
            text += " - Uy tín 💎\n"
        else:
            text += "\n"

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
    "5960653063:AAHyOV3a4nndUwSyXc0Vkrh8Dq87LZ3dh00").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.ALL, messageHandler))

app.run_polling()

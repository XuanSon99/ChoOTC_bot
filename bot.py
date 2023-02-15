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

    if update.message.chat.username in ["minatabar", "ChoOTCVN_support"]:

        # if "/postwithbutton" in update.message.text:
        #     text = update.message.text.split("|")

        #     reply_markup = InlineKeyboardMarkup(
        #         [[InlineKeyboardButton(
        #             text=text[2], url="https://t.me/ChoOTCVN_bot")]],
        #     )

        #     await context.bot.send_message(chat_id="-1001871429218", text=text[1], reply_markup=reply_markup, parse_mode=constants.ParseMode.HTML)

        if "/post" in update.message.text:

            text = "<b>Chọn thông báo bên dưới 🔥</b>\n<i>1. Thành viên uy tín là ai?\n2. KYC để làm gì?\n3. Affiliate - Chính sách hỗ trợ kết nối.\n4. Cảnh báo lừa đảo.\n5. Miễn trừ trách nhiệm.\n6. Uy Tín làm nên Thương hiệu.</i>"

            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='1 ☀️', callback_data='post1'),
                  InlineKeyboardButton(text='2 🌩', callback_data='post2'), ],
                 [InlineKeyboardButton(text='3 🌦', callback_data='post3'),
                  InlineKeyboardButton(text='4 🔥', callback_data='post4'), ],
                 [InlineKeyboardButton(text='5 ❄️', callback_data='post5'),
                  InlineKeyboardButton(text='6 🌤', callback_data='post6'), ]],
            )

            await context.bot.send_message(chat_id, text=text, reply_markup=reply_markup, parse_mode=constants.ParseMode.HTML)

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

    query = update.callback_query
    await query.answer()

    if query.data in ["first", "prev", "next", "last"]:

        page = update.effective_message.text[-3:]
        current_page = int(page[:1])
        last_page = int(page[-1:])

        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='|<', callback_data='first'),
              InlineKeyboardButton(text='<', callback_data='prev'),
              InlineKeyboardButton(text='>', callback_data='next'),
              InlineKeyboardButton(text='>|', callback_data='last')]],
        )

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

        return

    # choose daily post
    if query.data == "post1":
        text = "<b>Thành Viên Uy Tín Là Ai ?</b>\nLà những thành viên buôn bán thâm niên, chuyên nghiệp, có uy tín cao trong cộng đồng. Huy hiệu uy tín phải được đội ngũ bản quản lý chợ cấp.\n<b>Làm thế nào để trở thành TV uy tín ?</b>\n- Có trên 6 tháng hoạt động buôn bán tại Chợ OTC VN.\n- Giao dịch thành công tối thiểu 30 lần.\n- Được check thông tin cụ thể và phê duyệt từ 3 Admin.\n\n<i>Chat /uytin với bot @ChoOTCVN_bot để kiểm tra danh sách uy tín!</i>"
        msg = "Đã gửi 1 ☀️"

    if query.data == "post2":
        text = "<b>Xác Minh Danh Tính (KYC) Để Làm Gì?</b>\nKYC là quy trình dành cho các User muốn mua bán và giao dịch thường xuyên trên chợ:\n- KYC để đẩy nhanh tiến độ giao dịch nếu bạn là khách hàng\n- KYC để xác minh uy tín nếu bạn là Merchant\n- KYC sớm để nhận những ưu đãi từ đội ngũ Admin chợ\n\n<i>Chat ngay với bot @ChoOTCVN_bot để KYC!</i>"
        msg = "Đã gửi 2 🌩"

    if query.data == "post3":
        text = "<b>Affiliate - Chính Sách Hỗ Trợ Kết Nối</b>\nChợ OTC Việt Nam vẫn tiếp tục chạy các chương trình hỗ trợ khách hàng ngoài luồng OTC. Để nhận hoa hồng từ chương trình Affiliate, bạn hãy:\n<i>- Lập Gr chat của Merchant + khách hàng (phải có sự đồng ý thông qua Admin chợ)\n- Hỗ trợ quy trình giao dịch của khách hàng và Merchant</i>\n👉 Sau mỗi giao dịch, đội ngũ Admin sẽ check quy trình và hoàn lại cho các bạn 10% lợi nhuận.\n\n<i>Liên hệ @QuocPham_OTC để nhận thêm thông tin chi tiết!</i>"
        msg = "Đã gửi 3 🌦"

    if query.data == "post4":
        text = "<b>Cảnh Báo Lừa Đảo (Scam Warning)</b>\nCó nhiều đối tượng sử dụng tài khoản Telegram với Bio + Username tương tự đội ngũ Admin và Merchant trong chợ nhắn tin cho người dùng để thực hiện hành vi lừa đảo.\n<b>Lưu ý:</b>\n- Đội ngũ Merchant Uy tín sẽ không chủ động nhắn tin cho các bạn để yêu cầu giao dịch\n- Số tài khoản - địa chỉ ví của Merchant được Admin chợ quản lý nghiêm ngặt, tuyệt đối không giao dịch thông qua các số tài khoản - địa chỉ ví lạ\n- Các kiểu tin nhắn như “chuyển gấp; ứng trước; chuyển qua cho bạn;....” đều là hình thức Scam trá hình\n\n<i>Liên hệ @ChoOTCVN_support để được giải đáp các thắc mắc trên chợ</i>"
        msg = "Đã gửi 4 🔥"

    if query.data == "post5":
        text = "<b>Thông Báo Miễn Trừ Trách Nhiệm</b>\n- Chúng tôi sẽ không chịu trách nhiệm cho bất kỳ giao dịch ngoài luồng nào được thực hiện không thông qua Admin chợ!\n- Merchant của chợ sẽ không bao giờ chủ động nhắn tin để yêu cầu giao dịch!\n\n<i>Liên hệ @ChoOTCVN_support để được giải đáp các thắc mắc trên chợ</i>"
        msg = "Đã gửi 5 ❄️"

    if query.data == "post6":
        text = "<b>Uy Tín Làm Nên Thương Hiệu</b>\nĐộ an toàn và lợi nhuận/giao dịch của các bạn sẽ luôn được đảm bảo khi giao dịch với Thương nhân có uy tín cao trong cộng đồng. Những thương nhân an toàn sẽ được gắn huy hiệu “Uy tín” khi đăng bài mua bán.\n\n<i>Chat /uytin với bot @ChoOTCVN_bot để kiểm tra danh sách uy tín!</i>"
        msg = "Đã gửi 6 🌤"

    await context.bot.send_message(chat_id="-1001871429218", text=text, parse_mode=constants.ParseMode.HTML)
    await context.bot.send_message(chat_id, text=msg, parse_mode=constants.ParseMode.HTML)


app = ApplicationBuilder().token(
    "5960653063:AAHyOV3a4nndUwSyXc0Vkrh8Dq87LZ3dh00").build()

# app = ApplicationBuilder().token(
#     "6217705988:AAEOYp5g31rkl-iWrXAGE_mo7t0f0Oz3qIo").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.ALL, messageHandler))

app.run_polling()

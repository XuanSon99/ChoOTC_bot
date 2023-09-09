from telegram import *
from telegram.ext import *
import requests
import json
from types import SimpleNamespace
import math
import random
import time
from datetime import datetime
import pytz

kyc = "👨‍💻 Xác minh KYC"
uytin = "💎 DS Uy tín"

domain = "https://api.chootc.com"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    buttons = [[KeyboardButton(kyc), KeyboardButton(uytin)]]

    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Chào mừng bạn đến với <b>Chợ OTC VN</b>. Hãy chọn phương án bên dưới:", reply_markup=reply_markup, parse_mode=constants.ParseMode.HTML)


async def messageHandler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    username = update.effective_user.username
    chat_id = update.effective_chat.id

    # if update.message.chat.username in ["minatabar", "ChoOTCVN_support"]:

    # if "/postwithbutton" in update.message.text:
    #     text = update.message.text.split("|")

    #     reply_markup = InlineKeyboardMarkup(
    #         [[InlineKeyboardButton(
    #             text=text[2], url="https://t.me/ChoOTCVN_bot")]],
    #     )

    #     await context.bot.send_message(chat_id="-1001871429218", text=text[1], reply_markup=reply_markup, parse_mode=constants.ParseMode.HTML)
    if update.message.chat.type != "private":

        if "/uytin" in update.message.text:
            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='|<', callback_data='first'),
                  InlineKeyboardButton(text='<', callback_data='prev'),
                  InlineKeyboardButton(text='>', callback_data='next'),
                  InlineKeyboardButton(text='>|', callback_data='last')]],
            )

            await context.bot.send_message(chat_id, text=content(1), reply_markup=reply_markup, parse_mode=constants.ParseMode.HTML)

        if "uy tín" in update.message.text:

            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='VOTE UY TÍN', callback_data='vote')]],
            )

            start_time = time.time()
            seconds = abs(time.time() - start_time - 300)
            time_remaining = time.strftime("%M:%S", time.gmtime(seconds))

            text = f"<b>Biểu quyết uy tín @{username}</b>\n<i>Thời gian còn: {time_remaining}</i> ⏱"

            msg = await context.bot.send_message(chat_id, text=text, reply_markup=reply_markup, parse_mode=constants.ParseMode.HTML)

            #delete last message
            try:
                res = requests.get(f"{domain}/api/votings/@{username}")
                last_msg_id = res.json()["msg_id"]
                await context.bot.delete_message(message_id=last_msg_id, chat_id='-1001871429218')

                requests.post(f"{domain}/api/voting", {'username': f'@{username}','start_time': start_time, 'msg_id':  msg.message_id})
            except:
                requests.post(f"{domain}/api/voting", {'username': f'@{username}','start_time': start_time, 'msg_id':  msg.message_id})

        return

    if username is None:
        await context.bot.send_message(chat_id, text="Vui lòng cập nhật Username của bạn!")
        return
    
    if "/send" in update.message.text:
        text = "Thông báo chính thức từ <b>Ban Quản Lý Chợ OTC Việt Nam</b> 🇻🇳\n- Sau 1 thời gian dài chạy thử nghiệm, hoàn tất các quy chuẩn của chợ, chúng tôi đã quyết định sẽ chính thức mở chợ vào hôm nay 9/9/2023.\n- Các thành viên đã KYC trước đó sẽ được xét duyệt để đăng quảng cáo mua bán và không thao tác gì thêm.\n\n<i>Đây là thông báo dành cho những ai đã KYC trước đó!</i>"
        chat_id = update.message.text[6:]
        await context.bot.send_message(chat_id, text=text, parse_mode=constants.ParseMode.HTML)

    if kyc in update.message.text:
        link = f"https://kyc.chootc.com/#/{username}-{chat_id}"

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
    username = update.effective_user.username

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
    
    if query.data in ["vote"]:
        #get username is voted
        voting_user = update.effective_message.text.split("\n")[0].split()[-1]

        #check voting user has kyc
        info_user = requests.get(f"{domain}/api/user-info/{username}")

        if not info_user.content or info_user.json()["kyc"] != "success":
            return

        if username in voting_user:
            return
        
        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text='VOTE UY TÍN', callback_data='vote')]],
        )

        res = requests.get(f"{domain}/api/votings/{voting_user}")
        start_time = res.json()["start_time"]
        voted_list = res.json()["voted_user"]

        if time.time() - float(start_time) > 300:
            text = update.effective_message.text.split("\n")
            del text[1]
            text[0] = f"<b>Kết quả biểu quyết uy tín {voting_user}</b>"
            text[1] = f"<b>{text[1]}</b>"
            text[-1] = f"<b>{text[-1]}</b>"

            await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="\n".join(text), parse_mode=constants.ParseMode.HTML)
        else:
            # get current time
            seconds = abs(time.time() - float(start_time) - 300)
            time_remaining = time.strftime("%M:%S", time.gmtime(seconds))
            # current_time = time.strftime("%H:%M", time.localtime())
            current_time = datetime.now(tz=pytz.timezone('Asia/Ho_Chi_Minh'))
            current_hour = str(current_time)[11:16]

            #check user is admin
            response = requests.get(f"{domain}/api/isadmin/@{username}")
            if response.text:
                is_admin = "(Admin)"
            else:
                is_admin = ""

            #check user and set vote
            global voted_user

            if not voted_list:
                voted_user = f'@{username} {is_admin}'
                requests.put(f"{domain}/api/voting/{voting_user}",{'voted_user': voted_user})
            if voted_list and username not in voted_list:
                voted_user = f'{voted_list}\n@{username} {is_admin}'
                requests.put(f"{domain}/api/voting/{voting_user}",{'voted_user': voted_user})
            if voted_list and username in voted_list:
                return
            
            #export voted user list
            percent = 0
            has_admin = False
            voted_array = voted_user.split("\n")
            for index, item in enumerate(voted_array):
                if not index:
                    list_text = f"{index+1}. {item}"
                else:
                    list_text = f"{list_text}\n{index+1}. {item}"
                
                if "Admin" in item:
                    percent += 30
                    has_admin = True
                else:
                    percent += 15

            if percent < 100:
                result = f"Tỷ lệ: {percent}% | Chưa đủ uy tín để giao dịch 🔴"
            else:
                if has_admin:
                    result = f"Tỷ lệ: 100% | Đã đủ uy tín để giao dịch 🟢"
                else:
                    percent_random = random.randrange(83, 96)
                    result = f"Tỷ lệ: {percent_random}% | Chưa đủ uy tín để giao dịch 🔴"   

            text = f"<b>Biểu quyết uy tín {voting_user}</b>\n<i>Thời gian còn: {time_remaining}</i> ⏱\n<b>Danh sách đã cho uy tín:</b>\n{list_text}\n\n<b>{result}</b>"
            await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=reply_markup, parse_mode=constants.ParseMode.HTML)


app = ApplicationBuilder().token(
    "5960653063:AAHyOV3a4nndUwSyXc0Vkrh8Dq87LZ3dh00").build()

# app = ApplicationBuilder().token(
#     "6217705988:AAEOYp5g31rkl-iWrXAGE_mo7t0f0Oz3qIo").build()

app.add_handler(CommandHandler("start", start)) 
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.ALL, messageHandler))


# auto send message
async def callback_minute(context: ContextTypes.DEFAULT_TYPE):

    list = [
        "<b>Thành Viên Uy Tín Là Ai ?</b>\nLà những thành viên buôn bán thâm niên, chuyên nghiệp, có uy tín cao trong cộng đồng. Huy hiệu uy tín phải được đội ngũ bản quản lý chợ cấp.\n<b>Làm thế nào để trở thành TV uy tín ?</b>\n- Có trên 6 tháng hoạt động buôn bán tại Chợ OTC VN.\n- Giao dịch thành công tối thiểu 30 lần.\n- Được check thông tin cụ thể và phê duyệt từ 3 Admin.\n\n<i>Chat /uytin với bot @ChoOTCVN_bot để kiểm tra danh sách uy tín!</i>",

        # "<b>Xác Minh Danh Tính (KYC) Để Làm Gì?</b>\nKYC là quy trình dành cho các User muốn mua bán và giao dịch thường xuyên trên chợ:\n- KYC để đẩy nhanh tiến độ giao dịch nếu bạn là khách hàng\n- KYC để xác minh uy tín nếu bạn là Merchant\n- KYC sớm để nhận những ưu đãi từ đội ngũ Admin chợ\n\n<i>Chat ngay với bot @ChoOTCVN_bot để KYC!</i>",

        # "<b>Cảnh Báo Lừa Đảo (Scam Warning)</b>\nCó nhiều đối tượng sử dụng tài khoản Telegram với Bio + Username tương tự đội ngũ Admin và Merchant trong chợ nhắn tin cho người dùng để thực hiện hành vi lừa đảo.\n<b>Lưu ý:</b>\n- Đội ngũ Merchant Uy Tín sẽ không chủ động nhắn tin cho các bạn để yêu cầu giao dịch\n- Số tài khoản - địa chỉ ví của Merchant được Admin chợ quản lý nghiêm ngặt, tuyệt đối không giao dịch thông qua các số tài khoản - địa chỉ ví lạ\n- Các kiểu tin nhắn như “chuyển gấp; ứng trước; chuyển qua cho bạn;....” đều là hình thức Scam trá hình\n\n<i>Liên hệ @ChoOTCVN_support để được giải đáp các thắc mắc trên chợ</i>",

        # "<b>Thông Báo Miễn Trừ Trách Nhiệm</b>\nCác thành viên trong Chợ OTC Việt Nam đều có thể tự do thoả thuận và giao dịch với nhau mà không cần thông qua BQL chợ. Tuy nhiên:\n- Chúng tôi sẽ không chịu trách nhiệm cho bất kỳ giao dịch ngoài luồng nào được thực hiện không thông qua Admin chợ!\n- Thương Nhân của chợ sẽ không bao giờ chủ động nhắn tin để yêu cầu giao dịch!\n- Để đảm bảo giao dịch an toàn chúng tôi đưa ra lời khuyên nên liên hệ trực tiếp các Admin hoặc những thành viên được cấp huy hiệu “Uy Tín” trên chợ.\n\n<i>Liên hệ @ChoOTCVN_support để được giải đáp các thắc mắc trên chợ</i>",

        # "<b>Giới thiệu Chợ OTC Việt Nam</b>\nChợ OTC Việt Nam là cộng đồng giao lưu, trao đổi USDT,BTC, ETH,... các mặt hàng trực tiếp giữa tất cả <b>Khách Hàng</b> và các <b>Thương Nhân</b>, không thông qua bất cứ đơn vị tổ chức nào, không thu bất cứ khoản phí nào. Tất cả các phát sinh giao dịch đều là thỏa thuận giữa người mua và người bán.\n(Lưu ý: Chỉ các <b>Thương Nhân</b> mới được phép đăng quảng cáo trên chợ sau khi đăng ký trở thành <b>Thương Nhân</b> với BQL chợ.)\n\n<i>Liên hệ với @ChoOTCVN_support để nhận thông tin hỗ trợ</i>"
        ]
    
    try:
        res = requests.get(f"{domain}/api/setup")
        last_msg_id = res.json()[0]["value"]
        await context.bot.delete_message(message_id=last_msg_id, chat_id='-1001871429218')
        msg = await context.bot.send_message(chat_id='-1001871429218', text=random.choice(list), parse_mode=constants.ParseMode.HTML)
        requests.put(f"{domain}/api/setup/4", {'value': msg.message_id})
    except:
        msg = await context.bot.send_message(chat_id='-1001871429218', text=random.choice(list), parse_mode=constants.ParseMode.HTML)
        requests.put(f"{domain}/api/setup/4", {'value': msg.message_id})


job_queue = app.job_queue

job_minute = job_queue.run_repeating(callback_minute, interval=7200, first=10)

app.run_polling()

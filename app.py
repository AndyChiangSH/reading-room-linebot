from flask import Flask
from flask import request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError
import requests
from bs4 import BeautifulSoup
import os
import datetime
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

# load environment var
load_dotenv()

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN", ""))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET", ""))

scheduler = BackgroundScheduler({'apscheduler.timezone': 'Asia/Taipei'})
is_running = False

user_id = os.environ.get("USER_ID", "")

# 首頁
@app.route("/")
def index():
    return "Server OK!"


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    print("mtext:", mtext)

    if mtext == "#使用說明":
        reply_instruction(event)
    elif mtext == "#現在人數":
        reply_number_now(event)
    elif mtext == "#啟動機器人":
        start_robot(event)
    elif mtext == "#關閉機器人":
        stop_robot(event)

    # line_bot_api.reply_message(
    #     event.reply_token, TextSendMessage(text=event.message.text))


def reply_instruction(event):
    text = """1. 「現在人數」：機器人回傳現在自習室的人數。
2. 「啟動機器人」：啟動後，機器人將每一小時回傳自習室的人數，直到關閉機器人。
3. 「關閉機器人」：關閉後，機器人將不會再回傳自習室的人數，直到下次啟動。
4. 因為本服務架在免費平台上，運行時間是有限制的，所以希望大家上班時啟動，下班時關閉。"""

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))

def get_number():
    total_seat = int(os.environ.get("TOTAL_SEAT", 160))
    # print(total_seat)

    url = "https://space.lib.nchu.edu.tw/system/status.aspx"  # 自習室資料的網址

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    number_A = int(soup.find("td", class_="lang-8_B1A").find_next_sibling("td").text)   # A區剩餘座位
    number_B = int(soup.find("td", class_="lang-8_B1B").find_next_sibling("td").text)   # B區剩餘座位
    number_C = int(soup.find("td", class_="lang-8_B1C").find_next_sibling("td").text)   # C區剩餘座位
    total_number = total_seat - number_A - number_B - number_C # 全部座位 - A、B、C區的剩餘座位 = 使用人數

    # print(number_A)
    # print(number_B)
    # print(number_C)
    
    return total_number

def reply_number_now(event):
    total_number = get_number() # 取得人數
    print(total_number)
    
    now = datetime.datetime.now() + datetime.timedelta(hours=int(os.environ.get("TIMEZONE", 8))) # 現在時間(時區+8)
    now_format = now.strftime("%Y/%m/%d %H:%M")
    print(now_format)

    text = f"{now_format} 人數: {total_number}"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))


def push_message():
    total_number = get_number() # 取得人數
    print(total_number)

    now = datetime.datetime.now() + datetime.timedelta(hours=int(os.environ.get("TIMEZONE", 8))) # 現在時間(時區+8)
    now_format = now.strftime("%Y/%m/%d %H:%M")
    print(now_format)

    text = f"{now_format} 人數: {total_number}"
    line_bot_api.push_message(user_id, TextSendMessage(text=text))   # 推播通知


def start_robot(event):
    global scheduler, is_running
    if not is_running:   # 關閉中
        job = scheduler.add_job(push_message, 'interval', seconds=5)    # 新增工作
        scheduler.start()   # 啟動scheduler

        is_running = True
        
        text = "嗶!機器人啟動中..."
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
    else:   # 啟動中
        text = "嗶嗶!機器人已啟動!"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
    

def stop_robot(event):
    global scheduler, is_running
    if is_running:   # 啟動中
        scheduler.shutdown()    # 關閉scheduler
        scheduler = BackgroundScheduler({'apscheduler.timezone': 'Asia/Taipei'})    # 創造新的scheduler

        is_running = False

        text = "嗶!機器人關閉中..."
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
    else:
        text = "嗶嗶!機器人已關閉!"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))


if __name__ == "__main__":
    app.run(debug=True)

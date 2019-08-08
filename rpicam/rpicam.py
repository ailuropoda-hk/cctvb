from picamera import PiCamera
import socket
import telegram
import time
import os

from encrypt import *

PUBLIC_KEY_FILENAME = os.environ['PUBLIC_KEY_FILENAME']
BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = int(os.environ['CHAT_ID'])
CAPTURE_INTERVAL = int(os.environ['CAPTURE_INTERVAL'])

def internet(host="8.8.8.8", port=53, timeout=3):
  try:
    socket.setdefaulttimeout(timeout)
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
    return True
  except socket.error as ex:
    return False

camera = PiCamera()
# camera.resolution = (2592, 1944)
camera.start_preview()

public_key = importPublicKey(PUBLIC_KEY_FILENAME)
bot = None
botinfo = None

time.sleep(5)

while True:
  if internet() and botinfo is None:
    bot = telegram.Bot(token = BOT_TOKEN)
    botinfo = bot.get_me()
  if internet() and botinfo is not None:
    camera.capture('/tmp/rpicam.jpg')
    aesEncryptFile('/tmp/rpicam.jpg', '/tmp/encoded.enc', public_key)
    res = bot.send_document(chat_id=CHAT_ID, document=open('/tmp/encoded.enc', 'rb'))
    message = {
      'bot': botinfo.username,
      'chat_id': res.chat.id,
      'message_id': res.message_id,
      'file_id': res.document.file_id,
      'timestamp': res.date.timestamp()
    }
    bot.send_message(chat_id=CHAT_ID, text=message)
  time.sleep(CAPTURE_INTERVAL)
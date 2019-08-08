import telegram
from telegram.ext import Updater, MessageHandler, Filters
import time
import threading
import cv2
import imutils
import json

from encrypt import *
from utils import *

BOT_TOKEN = os.environ['SERVER_BOT_TOKEN']
INCOMING_CHAT_ID = int(os.environ['INCOMING_CHAT_ID'])
OUTGOING_CHAT_ID = int(os.environ['OUTGOING_CHAT_ID'])
PRIVATE_KEY_FILENAME = os.environ['PRIVATE_KEY_FILENAME']
RESIZED_WIDTH = 640

private_key = importPrivateKey(PRIVATE_KEY_FILENAME)
bot = telegram.Bot(token = BOT_TOKEN)
net = cv2.dnn.readNetFromDarknet('./models/yolov3-face.cfg', './models/yolov3-wider_16000.weights')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)



def download_document(file_id, bot_from, timestamp):
  global bot
  global private_key
  global net
  global RESIZED_WIDTH
  try:
    new_file = bot.get_file(file_id) 
    new_file.download(file_id + '.enc')
    aesDecryptFile(file_id + '.enc', file_id + '.jpg', private_key)
    img = cv2.imread(file_id + '.jpg')
    resized_img = imutils.resize(img, width=RESIZED_WIDTH)
    ratio = img.shape[1] / RESIZED_WIDTH
    blob = cv2.dnn.blobFromImage(resized_img, 1 / 255, (416, 416), [0, 0, 0], 1, crop=False)
    net.setInput(blob)
    layers_names = net.getLayerNames()
    outputs_names = [layers_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    outs = net.forward(outputs_names)
    faces = post_process(img, outs, 0.1, 0.4)
    cv2.imwrite(file_id + '.out.jpg', img)
    caption = json.dumps({'bot': bot_from, 'timestamp': timestamp, 'facecount': len(faces)})
    bot.send_photo(chat_id=OUTGOING_CHAT_ID, caption=caption, photo=open(file_id + '.out.jpg', 'rb'))
    if os.path.exists(file_id + '.enc'):
      os.remove(file_id + '.enc')
    if os.path.exists(file_id + '.jpg'):
      os.remove(file_id + '.jpg')
    if os.path.exists(file_id + '.out.jpg'):
      os.remove(file_id + '.out.jpg')
  except Exception as err: 
    print(err)
    if os.path.exists(file_id + '.enc'):
      os.remove(file_id + '.enc')
    if os.path.exists(file_id + '.jpg'):
      os.remove(file_id + '.jpg')
    if os.path.exists(file_id + '.out.jpg'):
      os.remove(file_id + '.out.jpg')

def new_message(update, context):
  try:
    if context.channel_post.chat.id == INCOMING_CHAT_ID:
      message = json.loads(context.channel_post.text)
      thread = threading.Thread(target = download_document, args =(message['file_id'], message['bot'], message['timestamp']))
      thread.start()
  except Exception as err: 
    print(err)

# def new_document(update, context):
#   try:
#     if context.channel_post.chat.id == INCOMING_CHAT_ID:
#       file_id = context.channel_post.document.file_id
#       timestamp = context.channel_post.date.timestamp()
#       thread = threading.Thread(target = download_document, args =(file_id, timestamp))
#       thread.start()
#   except Exception as err: 
#     print(err)

updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher

# docu_handler = MessageHandler(Filters.document, new_document)
docu_handler = MessageHandler(Filters.text, new_message)
dispatcher.add_handler(docu_handler)

updater.start_polling()
updater.idle() 



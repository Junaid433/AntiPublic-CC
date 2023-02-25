import telebot
import json
import requests
import os

bot = telebot.TeleBot('5736558781:AAEHKWXTAXlcQvVm1-iRr0CtoFktHy21JKH')

@bot.message_handler(content_types=['document'])
def handle(message):
    try:
        doc = message.document
        finfo = bot.get_file(doc.file_id)
        df = bot.download_file(finfo.file_path)
        dfs = df.decode('utf-8').split('\n')
        cards = []
        for card in dfs:
            if len(card)>16:
                card = card[:16]
            cards.append(card)
        cards = [x for x in cards if x != ""]        
        response = requests.post(
            'https://api.antipublic.cc/cards',
            json=cards
        ).json()
        lenpub = len(response["public"])
        lenpv = len(response["private"])
        lenpp = response['private_percentage']
        with open('Public.txt', 'w') as file:
            for pub in response["public"]:
                file.write(str(pub) + '\n')
        with open('Private.txt', 'w') as file:
            for pv in response["private"]:
                file.write(str(pv) + '\n')
        with open("Public.txt", "rb") as file:
            if lenpub == 0:
                pass
            else:
                bot.send_document(message.chat.id, file,reply_to_message_id=message.message_id)
        with open("Private.txt", "rb") as file:
            if lenpv == 0:
                pass
            else:
                bot.send_document(message.chat.id, file,reply_to_message_id=message.message_id)
        caption = 'Public : '+str(lenpub)+'\nPrivate : '+str(lenpv)+'\nPrivate Percentage : '+str(lenpp)
        bot.reply_to(message,caption)
        os.remove('Public.txt')
        os.remove('Private.txt')
    except Exception as e:
        res = response['detail']
        if not res:
            res = str(e)
        bot.reply_to(message, res)
bot.polling()

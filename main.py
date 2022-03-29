import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random, datetime

import os

from flask import Flask

app = Flask(__name__)


@app.route("/")
def main():
    vk_session = vk_api.VkApi(
        token='d0798041eb5ad2530312a6a6c4085d00c1fe872c8ed3db75ada34c9ee51fc5ba2116850164be113065972')

    longpoll = VkBotLongPoll(vk_session, '212234388')

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            print(event)
            print('Новое сообщение:')
            print('Для меня от:', event.obj.message['from_id'])
            print('Текст:', event.obj.message['text'])
            vk = vk_session.get_api()
            if len(set(event.obj.message['text'].lower().split()) & {'время', 'число', 'дата', 'день'}) > 0:

                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Привет, {vk.users.get(user_id=event.obj.message['from_id'])[0]['first_name']}!\n"
                                         f"Дата: {datetime.datetime.now().date()}\nВремя: {datetime.datetime.now().time().hour}:{datetime.datetime.now().time().minute}:{round(datetime.datetime.now().second)}\nДень недели: {['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'][int(datetime.date.today().weekday())]}",
                                 random_id=random.randint(0, 2 ** 64))
            elif 'секрет' in event.obj.message['text'].lower().split():
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"К сожалению вы достигли уровня максимума, передайте привет по номеру №1391",
                                 random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Привет, {vk.users.get(user_id=event.obj.message['from_id'])[0]['first_name']}!\n"
                                         f"Вы всегда можете узнать сегодняшнюю дату и время",
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

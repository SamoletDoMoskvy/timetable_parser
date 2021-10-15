import logging

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import main

vk_session = vk_api.VkApi(token='')
vk = vk_session.get_api()
group_id = vk.groups.getById()
group_id = group_id[0]['id']
longpoll = VkBotLongPoll(vk_session, group_id=group_id)
vk.groups.getLongPollServer(group_id=group_id)


def send_message(msg):
    vk.messages.send(
        key=longpoll.key,
        server=longpoll.server,
        ts=longpoll.ts,
        random_id=get_random_id(),
        message=msg,
        group_id=event.group_id,
        chat_id=event.chat_id
    )


def delete_message():
    vk.messages.delete(
        delete_for_all=1,
        group_id=event.group_id,
        peer_id=event.message.peer_id,
        conversation_message_ids=event.message.conversation_message_id
    )


for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.from_chat:
            jan_id = 237461777
            command = event.message.text.lower()
            from_id = event.message.from_id
            if event.message.from_id == jan_id:
                message = f"Либероид приложен, его сообщением было:'{event.message.text}'"
                delete_message()
                send_message(message)
            elif command == '/расписание на завтра':
                message = main.get_timetable(main.get_date(), main.TOMORROW)
                send_message(message)
            elif command == '/расписание на сегодня':
                message = main.get_timetable(main.get_date(), main.TODAY)
                send_message(message)
            elif command == '/help':
                message = '/расписание на завтра\n/расписание на сегодня'
                send_message(message)
            elif command == 'подтверди.' and event.message.from_id == 202147103:
                message = 'Подтверждаю.'
                send_message(message)
            elif command == 'молодец.':
                message = 'Спасибо!'
                send_message(message)

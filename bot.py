import datetime
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
today = datetime.datetime.today()
today = today.isoweekday() - 1
tomorrow = datetime.datetime.today()
tomorrow = tomorrow.isoweekday()
timetable = main.Manager.generate_from_umeuos()
line = '-----'


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
                day_name = timetable.days[tomorrow].day_name
                message = ""
                for item in timetable.days[tomorrow].lessons:
                    message += f"""\n\n№{item.index}
{item.title}
Аудитория: {item.room}
Время: {item.dt_from} - {item.dt_to}"""
                send_message(message)

            elif command == '/расписание на сегодня':
                day_name = timetable.days[today].day_name
                message = day_name
                for item in timetable.days[today].lessons:
                    message += f"""\n\n№{item.index}
{item.title}
Аудитория: {item.room}
Время: {item.dt_from} - {item.dt_to}"""
                send_message(message)

            elif command == '/расписание на неделю':
                message = ""
                for day in timetable.days:
                    day_name = day.day_name
                    message += line + day_name + line
                    for item in day.lessons:
                        message += f"""\n№{item.index}
{item.title}
Аудитория: {item.room}
Время: {item.dt_from} - {item.dt_to}\n\n"""
                send_message(message)

            elif command == '/help':
                message = '/расписание на завтра\n/расписание на сегодня\n/расписание на неделю'
                send_message(message)

            elif command == 'подтверди.' and event.message.from_id == 202147103:
                message = 'Подтверждаю.'
                send_message(message)

            elif command == 'молодец.':
                message = 'Спасибо!'
                send_message(message)

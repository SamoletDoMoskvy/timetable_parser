import requests, re, datetime
from bs4 import BeautifulSoup

URL = 'https://www.spbume.ru/ru/viewschedule/%D0%9E%D0%94%D0%9E-%D0%9F%D0%9809-18-1/'
DATE_PATTERN = '%d.%m.%Y'
TOMORROW = datetime.datetime.today() + datetime.timedelta(days=1)
TOMORROW = TOMORROW.replace(hour=0, minute=0, second=0, microsecond=0)
TODAY = datetime.datetime.today()
TODAY = TODAY.replace(hour=0, minute=0, second=0, microsecond=0)


def get(URL):
    request = requests.get(URL)
    html = request.text

    return BeautifulSoup(html, 'html.parser')


def get_date():
    soup = get(URL)
    week = []
    week_array = []

    for date in soup.find_all('span'):
        date = date.get_text('|')
        date = re.sub(r'[A-zА-я!@:$]+\s?', '', date).strip()
        if date == '':
            continue
        else:
            week.append(date)

    for i in week:
        i = i.split('|')
        week_array += ([[i[0], i[1]]])

    week_list = []

    for i in week_array:
        current_date1 = datetime.datetime.strptime(i[0], DATE_PATTERN)
        current_date2 = datetime.datetime.strptime(i[1], DATE_PATTERN)
        days_difference = current_date2 - datetime.timedelta(current_date1.day)
        date_list = ([current_date1 + datetime.timedelta(days=x) for x in range(days_difference.day + 1)])
        week_list.extend([date_list])

    return week_list
    # for x in range(len(week_list) - 1):
    #     try:
    #         print(week_list[x].index(TOMORROW))
    #         print(x)
    #     except:
    #         pass


# Получаем расписание на день
def get_timetable(week_list):
    for x in range(len(week_list)):
        try:
            week_list[x].index(TODAY)
            x += 1
            break
        except:
            pass

    url = f"https://www.spbume.ru/ru/viewschedule/ОДО-ПИ09-18-1/{x}/"
    timetable = [0, 1, 2, 3, 4, 5, 6, 7]
    soup = get(url)
    week_list = [0, 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

    for thead in soup.find_all('thead'):
        try:
            if week_list.index(thead.text.strip()):
                number = week_list.index(thead.text.strip())
                for tbody in soup.find_all('tbody'):
                    try:
                        if timetable.index(tbody.text.strip()):
                            pass
                    except:
                        if tbody.text.strip() == '':
                            pass
                        else:
                            timetable[number] = tbody.text.strip()
                            break
        except:
            pass

    print(timetable[TODAY.weekday() + 1])


get_timetable(get_date())

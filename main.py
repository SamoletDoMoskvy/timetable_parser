import requests, re, datetime
from bs4 import BeautifulSoup

#--Получаем страницу--#
URL = 'https://www.spbume.ru/ru/viewschedule/%D0%9E%D0%94%D0%9E-%D0%9F%D0%9809-18-1/'
def get(URL):
    weekday = datetime.datetime.today().weekday()
    request = requests.get(URL)
    html = request.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup

#--Сопостовляем текущую дату с нужной неделей--#
def get_date():
    week = []
    arr = []
    pattern = '%d.%m.%Y'
    date_list = []
    today = datetime.datetime.today() + datetime.timedelta(days=1)
    soup = get(URL)

    for date in soup.find_all('span'):
        date = date.get_text('|')
        date = re.sub(r'[A-zА-я!@:$]+\s?', '', date).strip()
        if date == '':
            continue
        else:
            week.append(date)

    for i in week:
        i = i.split('|')
        arr += ([[i[0], i[1]]])

    counter = 1

    #-Вообще, этот цикл можно выпилить, посольку почти всегда разница дней между неделями в расписании = 6, но кто знает бухгалтерию, да и почему бы не потренироваться
    for i in arr:
        current_date1 = datetime.datetime.strptime(i[0], pattern)
        current_date2 = datetime.datetime.strptime(i[1], pattern)
        days_difference = current_date2.day - current_date1.day

        if days_difference < 0:
            #--HANDMADE КоСтЫлЬ--#
            days_difference = 6

        date_list = ([current_date1 + datetime.timedelta(days = x) for x in range(days_difference)])

        for j in date_list:

            if today.date() == j.date():
                #--Возврат номера нужной нам недели--#
                return counter

        counter += 1

#--Получаем расписание на день--#
def get_timetable(date):
    URL = 'https://www.spbume.ru/ru/viewschedule/%D0%9E%D0%94%D0%9E-%D0%9F%D0%9809-18-1/{0}/'.format(date)
    print(URL)
    timetable = []
    soup = get(URL)
    for headers in soup.find_all('tbody'):
        # TODO: Реализовать алгоритм 1/0 через заполнение этого массива
        timetable.append(headers.text.strip())

    day = datetime.datetime.today().isoweekday()

    try:
        #--Здесь крутить значение индекса timetable для тестов--#
        #--Значение индекса соответствует дню недели от 1 до 7--#
        if len(timetable) < 7:
            print(timetable[day-1])
        else:
            print(timetable[day+1])
    except:
        print('Выходной')


get_timetable(get_date())

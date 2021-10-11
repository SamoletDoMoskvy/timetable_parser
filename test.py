import requests, re, datetime
from bs4 import BeautifulSoup


weekday = datetime.datetime.today().weekday()

URL = "https://www.spbume.ru/ru/viewschedule/%D0%9E%D0%94%D0%9E-%D0%9F%D0%9809-18-1/4/"

request = requests.get(URL)

html = request.text

soup = BeautifulSoup (html, 'html.parser')

timetable = []


# Парсинг имеющихся на странице дат расписания
week = []
for date in soup.find_all('span'):
    date = date.get_text('|')
    date = re.sub(r'[A-zА-я!@:$]+\s?', '', date).strip()
    if date == '':
        continue
    else:
        week.append(date)

arr = []
for i in week:
    i = i.split('|')
    arr += ([[i[0], i[1]]])

pattern = "%d.%m.%Y"
date_list = []
today = datetime.datetime.today()
counter = 1
for i in arr:
    current_date1 = datetime.datetime.strptime(i[0], pattern)
    current_date2 = datetime.datetime.strptime(i[1], pattern)
    days_difference = current_date2.day - current_date1.day
    if days_difference < 0: # Костыль
        days_difference = 6
    date_list = ([current_date1 + datetime.timedelta(days=x) for x in range(days_difference)])
    for j in date_list:
        if today.date() == j.date():
            print(counter)
    counter += 1

## Массив с датами для расписания ##
#print(arr)

#for i in week:
#    week = i.split('|')

# Парсинг самого расписания
for headers in soup.find_all('tbody'):
    timetable.append(headers.text.strip())

#print(timetable[weekday])

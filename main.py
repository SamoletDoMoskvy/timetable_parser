from bs4 import BeautifulSoup as bs
import typing
import requests
import datetime


class Lesson:
    def __init__(self, index, title, dt_from, dt_to, room):
        self.index = index
        self.title = title
        self.dt_from = dt_from
        self.dt_to = dt_to
        self.room = room


class Day:
    def __init__(self, day_index: int, day_name: str):
        self.day = day_index
        self.day_name = day_name
        self.lessons = []

    def add_lesson(self, lesson: Lesson):
        self.lessons.append(lesson)


class Week:
    def __init__(self):
        self.days: typing.List[Day] = []

    def add_day(self, day: Day) -> None:
        self.days.append(day)
        self.days = sorted(self.days, key=lambda el: el.day)


class Manager:
    weeks = []

    @classmethod
    def generate_from_umeuos(cls):
        days = {"Понедельник": 1, "Вторник": 2, "Среда": 3, "Четверг": 4, "Пятница": 5, "Суббота": 6}
        traceback = requests.get("https://www.spbume.ru/ru/viewschedule/%D0%9E%D0%94%D0%9E-%D0%9F%D0%9809-18-1/4/")
        counter = 0
        day_index = None

        if traceback.status_code == 200:
            current_day = None
            soup = bs(traceback.text, "html.parser")
            weeks = soup.find("table")
            max_index = len(weeks.find_all("th")) - 4
            week = Week()

            for itm in weeks.children:
                if itm == "\n":
                    continue

                if counter <= 1:
                    counter += 1
                    continue

                elif itm.name == "thead":
                    print(itm.text)
                    current_day = itm.text.replace("\n", "")
                    day_index = days[current_day]

                    if day_index == max_index:
                        cls.weeks.append(week)
                        week = Week()

                elif itm.name == "tbody":
                    items = itm.find_all("tr")
                    day = Day(day_index=day_index, day_name=current_day)

                    for unit in items:
                        index, unparsed_time, room, lesson = [e.text for e in unit.find_all("td")]
                        index = int(index)
                        unparsed_time = [datetime.datetime.strptime(e, "%H:%M") for e in unparsed_time[:len("08:25-09:55")].split("-")]
                        tm = [datetime.time(hour=d.hour, minute=d.minute) for d in unparsed_time]

                        lesson = Lesson(index=index, title=lesson, dt_from=tm[0], dt_to=tm[1], room=room)
                        day.add_lesson(lesson=lesson)

                    week.add_day(day)
                    print(day)

                counter += 1


if __name__ == "__main__":
    Manager.generate_from_umeuos()

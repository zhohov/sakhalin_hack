import secrets
import string
import datetime
from calendar import LocaleHTMLCalendar
from apps.tasks.models import Task


def get_password() -> str:
    length = 20
    pwd = ''
    alphabet = string.ascii_letters + string.digits + string.punctuation
    for i in range(length):
        pwd += ''.join(secrets.choice(alphabet))

    return pwd


def get_calendar() -> str:
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    cal = '<h3 class="pt-3">Календарь для</h3>' + '<table><tr><td>' \
          + set_calendar(now, year, month) + '</td><td>' + set_calendar(now, year, month + 1) + '</td></tr></table>'

    return cal


def set_calendar(now, year, month) -> str:
    cal = LocaleHTMLCalendar(locale='ru_RU.UTF-8').formatmonth(year, month)

    for i in range(1, 31):
        tasks = Task.objects.filter(date__day=i, date__month=month)
        day_tasks = ''

        if len(tasks) == 0:
            if i == now.day and month == now.month:
                cal = cal.replace(f'>{i}</td>', f'''><div class="dropdown">
                                                  <button class="btn btn-danger" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                                    {i}
                                                  </button>
                                                  <ul class="dropdown-menu">
                                                    <li><a class="dropdown-item" href="#">Выходной</a></li></ul></div></td>''')

            else:
                cal = cal.replace(f'>{i}</td>', f'''><div class="dropdown">
                                                  <button class="btn btn-light" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                                    {i}
                                                  </button>
                                                  <ul class="dropdown-menu">
                                                    <li><a class="dropdown-item" href="#">Выходной</a></li></ul></div></td>''')
            continue

        for task in tasks:
            address = task.address.first()
            if not task.is_active:
                if task.quality_assessment:
                    day_tasks += f'''<li><a class="dropdown-item" href="#">{address}</a></li>
                                            <li><a class="dropdown-item" href="#">{task.date.day}/{task.date.month}/{task.date.year}</a></a></li>
                                            <li><a href="/tasks/view_report/{task.id}/">Посмотреть отчет</a></li>
                                            <li><a href="/tasks/view_quality_assessment/{task.id}/">Посмотреть проверку</a></li><br>'''
                else:
                    day_tasks += f'''<li><a class="dropdown-item" href="#">{address}</a></li>
                                     <li><a class="dropdown-item" href="#">{task.date.day}/{task.date.month}/{task.date.year}</a></a></li>
                                     <li><a href="/tasks/view_report/{task.id}/">Посмотреть отчет</a></li>
                                     <li><a>Оценки качества пока нет</a></li><br>'''
            elif task.date.month == month:
                day_tasks += f'''<li><a class="dropdown-item" href="#">{address}</a></li>
                                <li><a class="dropdown-item" href="#">{task.date.day}/{task.date.month}/{task.date.year}</a></a></li>
                                <li><a href="/tasks/task_report/{task.id}/">Добавить отчет</a></li>
                                <li><a>Оценки качества пока нет</a></li><br>'''

        if i == now.day and tasks.first().date.month == now.month:
            day_tasks = f'''><div class="dropdown"><button class="btn btn-danger" type="button" 
            data-bs-toggle="dropdown" aria-expanded="false">{tasks.first().date.day}</button><ul class="dropdown-menu">''' + day_tasks + '</ul></div><'
        else:
            day_tasks = f'''><div class="dropdown"><button class="btn btn-secondary" type="button" 
            data-bs-toggle="dropdown" aria-expanded="false">{tasks.first().date.day}</button><ul class="dropdown-menu">''' + day_tasks + '</ul></div><'

        cal = cal.replace(f'>{tasks.first().date.day}<', day_tasks)

    return cal

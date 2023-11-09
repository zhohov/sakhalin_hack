import secrets
import string
import datetime
from calendar import LocaleHTMLCalendar


def get_password() -> str:
    length = 20
    pwd = ''
    alphabet = string.ascii_letters + string.digits + string.punctuation
    for i in range(length):
        pwd += ''.join(secrets.choice(alphabet))

    return pwd


def get_calendar(all_tasks, now, year, month) -> str:
    cal = LocaleHTMLCalendar(locale='ru_RU.UTF-8').formatmonth(year, month)

    for task in all_tasks:
        if task.date.month == month:
            address = task.address.first()
            if task.date.day == now.day and task.date.month == now.month:
                if not task.is_active:
                    if task.quality_assessment:
                        cal = cal.replace(f'>{task.date.day}<', f'''><div class="dropdown">
                                                              <button class="btn btn-danger" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                                                {task.date.day}
                                                              </button>
                                                              <ul class="dropdown-menu">
                                                                <li><a class="dropdown-item" href="#">{address}</a></li>
                                                                <li><a class="dropdown-item" href="#">{task.date.day}/{task.date.month}/{task.date.year}</a></a></li>
                                                                <li><a href="/tasks/view_report/{task.id}/">Посмотреть отчет</a></li>
                                                                <li><a href="/tasks/view_quality_assessment/{task.id}/">Посмотреть проверку</a></li>
                                                              </ul></div><''')
                    else:
                        cal = cal.replace(f'>{task.date.day}<', f'''><div class="dropdown">
                                                                                  <button class="btn btn-danger" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                                                                    {task.date.day}
                                                                                  </button>
                                                                                  <ul class="dropdown-menu">
                                                                                    <li><a class="dropdown-item" href="#">{address}</a></li>
                                                                                    <li><a class="dropdown-item" href="#">{task.date.day}/{task.date.month}/{task.date.year}</a></a></li>
                                                                                    <li><a href="/tasks/view_report/{task.id}/">Посмотреть отчет</a></li>
                                                                                    <li><a>Оценки качества пока нет</a></li>
                                                                                  </ul></div><''')
                else:
                    cal = cal.replace(f'>{task.date.day}<', f'''><div class="dropdown">
                                                                                                  <button class="btn btn-danger" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                                                                                    {task.date.day}
                                                                                                  </button>
                                                                                                  <ul class="dropdown-menu">
                                                                                                    <li><a class="dropdown-item" href="#">{address}</a></li>
                                                                                                    <li><a class="dropdown-item" href="#">{task.date.day}/{task.date.month}/{task.date.year}</a></a></li>
                                                                                                    <li><a href="/tasks/task_report/{task.id}/">Добавить отчет</a></li>
                                                                                                    <li><a>Оценки качества пока нет</a></li>
                                                                                                  </ul></div><''')
            if not task.is_active:
                if task.quality_assessment:
                    cal = cal.replace(f'>{task.date.day}<', f'''><div class="dropdown">
                                                          <button class="btn btn-secondary" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                                            {task.date.day}
                                                          </button>
                                                          <ul class="dropdown-menu">
                                                            <li><a class="dropdown-item" href="#">{address}</a></li>
                                                            <li><a class="dropdown-item" href="#">{task.date.day}/{task.date.month}/{task.date.year}</a></a></li>
                                                            <li><a href="/tasks/view_report/{task.id}/">Посмотреть отчет</a></li>
                                                            <li><a href="/tasks/view_quality_assessment/{task.id}/">Посмотреть проверку</a></li>
                                                          </ul></div><''')
                else:
                    cal = cal.replace(f'>{task.date.day}<', f'''><div class="dropdown">
                                                                              <button class="btn btn-secondary" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                                                                {task.date.day}
                                                                              </button>
                                                                              <ul class="dropdown-menu">
                                                                                <li><a class="dropdown-item" href="#">{address}</a></li>
                                                                                <li><a class="dropdown-item" href="#">{task.date.day}/{task.date.month}/{task.date.year}</a></a></li>
                                                                                <li><a href="/tasks/view_report/{task.id}/">Посмотреть отчет</a></li>
                                                                                <li><a>Оценки качества пока нет</a></li>
                                                                              </ul></div><''')
            else:
                cal = cal.replace(f'>{task.date.day}<', f'''><div class="dropdown">
                                                                                              <button class="btn btn-secondary" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                                                                                {task.date.day}
                                                                                              </button>
                                                                                              <ul class="dropdown-menu">
                                                                                                <li><a class="dropdown-item" href="#">{address}</a></li>
                                                                                                <li><a class="dropdown-item" href="#">{task.date.day}/{task.date.month}/{task.date.year}</a></a></li>
                                                                                                <li><a href="/tasks/task_report/{task.id}/">Добавить отчет</a></li>
                                                                                                <li><a>Оценки качества пока нет</a></li>
                                                                                              </ul></div><''')

    if now.month == month:
        cal = cal.replace(f'>{now.day}</td>', f'''><div class="dropdown">
                                              <button class="btn btn-danger" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                                {now.day}
                                              </button>
                                              <ul class="dropdown-menu">
                                                <li><a class="dropdown-item" href="#">Выходной</a></li></ul></div></td>''')

    for i in range(0, 31):
        cal = cal.replace(f'>{i}</td>', f'''><div class="dropdown">
                                              <button class="btn btn-light" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                                                {i}
                                              </button>
                                              <ul class="dropdown-menu">
                                                <li><a class="dropdown-item" href="#">Выходной</a></li></ul></div></td>''')

    print(cal)
    return cal

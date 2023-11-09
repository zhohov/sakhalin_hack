import datetime
import os
import random
from calendar import HTMLCalendar, LocaleHTMLCalendar
import re

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail

from apps.tasks.models import Task, CompletedTask, QualityAssessment
from apps.appeals.models import Appeal, AppealAnswer
from .models import CustomUser
from .forms import EmailLogin, OTPForm, PhoneForm, EmailPassword
from .services import get_password, get_calendar


@login_required(login_url="/users/login/")
def user_profile(request) -> render:
    try:
        user_group = request.user.groups.all().first()
        sender_appeals = Appeal.objects.all().filter(sender__id=request.user.id)
        received_appeals = Appeal.objects.all().filter(recipient__id=request.user.id)
        if user_group.name == 'Дворники':
            enddate = datetime.datetime.now(tz=datetime.timezone.utc)
            startdate = enddate - datetime.timedelta(days=7)
            tasks = Task.objects.all().filter(cleaner__id=request.user.id, date__range=[startdate, enddate])
            completed_task = CompletedTask.objects.all().filter(cleaner__id=request.user.id, marks='Выполнена')
            marks = QualityAssessment.objects.all().filter(cleaner__id=request.user.id)
            middle_mark = 0
            for mark in marks:
                middle_mark += int(mark.mark)
            if middle_mark != 0:
                middle_mark = middle_mark / completed_task.count()
            print(completed_task)
            all_tasks = Task.objects.filter(cleaner__id=request.user.id)

            now = datetime.datetime.now()
            year = now.year
            month = now.month

            cal = '<h3 class="pt-3">Календарь для</h3>' + '<table><tr><td>' + get_calendar(all_tasks, now, year, month) + '</td><td>' + get_calendar(all_tasks, now, year, month+1) + '</td></tr></table>'

            data = {
                'title': 'Личный кабинет',
                'all_tasks': all_tasks,
                'tasks': tasks,
                'appeals': sender_appeals,
                'received_appeals': received_appeals,
                'task_count': all_tasks.count(),
                'completed_task': completed_task.count(),
                'not_completed_task': all_tasks.count()-completed_task.count(),
                'middle_mark': middle_mark,
                'cal': cal,
            }
            print(all_tasks.count())
            return render(request, template_name='pages/profiles/cleaner_profile.html', context=data)

        elif user_group.name == 'Управдома':
            user_company = request.user.company.all().first()
            cleaners = CustomUser.objects.all().filter(groups__name='Дворники', company__name=user_company.name)
            data = {
                'title': 'Личный кабинет',
                'company': user_company,
                'cleaners': cleaners,
                'appeals': sender_appeals,
                'received_appeals': received_appeals,
            }
            return render(request, template_name='pages/profiles/manager_profile.html', context=data)

        elif user_group.name == 'Сотрудники ЖЭК':
            user_company = request.user.company.all().first()
            sender_appeals = Appeal.objects.all().filter(company__id=user_company.id, sender__id=None)
            received_appeals = Appeal.objects.all().filter(company__id=user_company.id).exclude(sender__id=None)
            addresses = user_company.address.all()
            cleaners = CustomUser.objects.all().filter(groups__name='Дворники', company__name=user_company.name)
            data = {
                'title': 'Личный кабинет',
                'company': user_company,
                'cleaners': cleaners,
                'addresses': addresses,
                'appeals': sender_appeals,
                'received_appeals': received_appeals,
            }
            return render(request, template_name='pages/profiles/uk_employee/uk_employee_profile.html', context=data)

    except AttributeError:
        raise render(request, template_name='pages/profiles/error.html')


def email_login(request) -> render:
    if request.method == 'POST':
        form = EmailLogin(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(email, password)
            username = CustomUser.objects.get(email=email).username
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                print(user)
                login(request, user)
                return redirect('/users/profile/')

            return redirect('/users/email_login/')

    else:
        form = EmailLogin()

    return render(request, 'registration/email_login.html', context={'title': 'Вход в аккаунт', 'form': form})


def get_email_password(request) -> render:
    if request.method == 'POST':
        form = EmailPassword(request.POST)

        if form.is_valid():
            email = form.data['email']
            user = CustomUser.objects.filter(email=email).first()

            if user is not None:
                pwd = get_password()
                user.set_password(pwd)
                user.save()
                send_mail(subject='Пароль для входа в аккаунт',
                          from_email=os.getenv('EMAIL_HOST_USER'),
                          message=f'Ваш пароль для входа в аккаунт {pwd}',
                          recipient_list=[email, ],
                          fail_silently=False
                          )

        return redirect('/users/email_login/')
    else:
        form = EmailPassword()

    return render(request, 'registration/get_email_password.html', context={'title': 'Получить пароль', 'form': form})


def phone_number_login(request) -> render:
    if request.method == 'POST':
        form = PhoneForm(request.POST)
        user = ...
        phone_number = form.data['phone_number']
        try:
            if form.is_valid:
                user = CustomUser.objects.filter(phone_number=phone_number).first()
                otp_code = random.randint(1000, 1_000_000)
                user.phone_code = otp_code
                user.save()

            return redirect('users:otp_verified', user_id=user.id)

        except:
            ...

    else:
        form = PhoneForm()

    return render(request, 'registration/phone_number_form.html', context={'title': 'Вход в аккаунт', 'form': form})


def otp_verified(request, user_id: int) -> render:
    if request.method == 'POST':
        form = OTPForm(request.POST)

        if form.is_valid:
            code = form.data['otp_code']
            user_otp = CustomUser.objects.get(pk=user_id).phone_code

            if code == user_otp:
                username = CustomUser.objects.get(pk=user_id).username
                user = authenticate(request, username=username)

                print('OK ', user)

                if user is not None:
                    login(request, user)
                    return redirect('/users/profile/')

    else:
        form = OTPForm()

    return render(request, 'registration/otp_verified_form.html', context={'title': 'Вход в аккаунт', 'form': form, 'user_id': user_id})


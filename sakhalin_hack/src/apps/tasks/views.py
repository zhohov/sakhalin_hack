import datetime
import json
from datetime import timedelta

from django.shortcuts import render, redirect
from django.core import serializers

import exif

from .forms import TaskReport, AddTask, QualityAssessmentForm
from .models import Task, CompletedTask, QualityAssessment
from apps.users.models import CustomUser, Address, Company
from django.contrib.auth.decorators import login_required

from .services.image_service import image_coordinates, get_address, verified_address


@login_required(login_url="/users/login/")
def cleaner_task_report(request, task_id: int) -> render:
    address = ...
    task = Task.objects.filter(pk=task_id).first()
    task_address = task.address.all().first()

    if request.method == 'POST':
        request.POST._mutable = True
        coord_1 = ...
        coord_2 = ...

        form = TaskReport(request.POST, request.FILES)

        try:
            file = request.FILES['photo']
            print(file)
            image = exif.Image(file)
            try:
                coord_1 = image_coordinates(image.gps_longitude, image.gps_longitude_ref)
                coord_2 = image_coordinates(image.gps_latitude, image.gps_latitude_ref)
                if coord_1 is not None:
                    form.data['coord1'] = image_coordinates(image.gps_longitude, image.gps_longitude_ref)
                    form.data['coord2'] = image_coordinates(image.gps_latitude, image.gps_latitude_ref)
                    address = get_address(coord_1, coord_2)

            except:
                print('Не удалось проверить координаты фото')

        except KeyError:
            print('Фото не загружено')

        if coord_1:
            if verified_address(address, task_address):
                if form.is_valid():
                    task_report = CompletedTask.objects.filter(task__id=task_id).first()
                    form.save()
                    task_report.verified_address = True
                    task_report.save()
                    task.is_active = False
                    task.save()
        else:
            form.save()
            task.is_active = False
            task.save()

        return redirect('/users/profile/')

    else:
        form = TaskReport()
        form.fields['task'].initial = str(task.id)
        form.fields['cleaner'].initial = str(task.cleaner.id)
        form.fields['address'].initial = str(task_address.id)
        form.fields['manager'].initial = str(task.manager.id)
        form.fields['date'].initial = str(task.date)
        form.fields['coord1'].initial = ''
        form.fields['coord1'].initial = ''

        context = {
            'title': 'Добавить отчет',
            'task': task,
            'form': form,
        }

    return render(request, 'pages/profiles/add_report.html', context=context)


@login_required(login_url="/users/login/")
def get_cleaner_tasks(request, cleaner_id: int) -> render:
    cleaner = CustomUser.objects.all().filter(pk=cleaner_id).first()
    enddate = datetime.datetime.now(tz=datetime.timezone.utc)
    startdate = enddate - timedelta(days=7)
    tasks = Task.objects.all().filter(cleaner__id=cleaner_id, date__range=[startdate, enddate])
    all_tasks = Task.objects.all().filter(cleaner__id=cleaner_id)

    completed_task = CompletedTask.objects.all().filter(cleaner__id=cleaner_id, marks='Выполнена')
    marks = QualityAssessment.objects.all().filter(cleaner__id=cleaner_id)
    middle_mark = 0
    for mark in marks:
        middle_mark += int(mark.mark)
    if middle_mark != 0:
        middle_mark = middle_mark / completed_task.count()

    data = {
        'title': 'Задачи дворника',
        'cleaner': cleaner,
        'tasks': tasks,
        'task_count': all_tasks.count(),
        'completed_task': completed_task.count(),
        'not_completed_task': all_tasks.count() - completed_task.count(),
        'middle_mark': middle_mark,
    }

    return render(request, 'pages/profiles/cleaner_info.html', context=data)


@login_required(login_url="/users/login/")
def get_all_cleaner_tasks(request, cleaner_id: int) -> render:
    cleaner = CustomUser.objects.all().filter(pk=cleaner_id).first()
    enddate = datetime.datetime.now(tz=datetime.timezone.utc)
    startdate = enddate - timedelta(days=7)
    tasks = Task.objects.all().filter(cleaner__id=cleaner_id, date__range=[startdate, enddate])
    all_tasks = Task.objects.all().filter(cleaner__id=cleaner_id)

    completed_task = CompletedTask.objects.all().filter(cleaner__id=cleaner_id, marks='Выполнена')
    marks = QualityAssessment.objects.all().filter(cleaner__id=cleaner_id)
    middle_mark = 0
    for mark in marks:
        middle_mark += int(mark.mark)
    if middle_mark != 0:
        middle_mark = middle_mark / completed_task.count()

    data = {
        'title': 'Задачи дворника',
        'cleaner': cleaner,
        'all_tasks': all_tasks,
        'task_count': all_tasks.count(),
        'completed_task': completed_task.count(),
        'not_completed_task': all_tasks.count() - completed_task.count(),
        'middle_mark': middle_mark,
    }

    return render(request, 'pages/profiles/cleaner_all_tasks_info.html', context=data)


@login_required(login_url="/users/login/")
def add_task(request, cleaner_id: int) -> render:
    if request.method == 'POST':
        request.POST._mutable = True
        form = AddTask(request.POST)
        print(form.data)

        if form.is_valid():
            print(form.data)
            form.save()

        return redirect('/users/profile/')
    else:
        cleaner = CustomUser.objects.all().filter(pk=cleaner_id).first()
        company = cleaner.company.first()

        form = AddTask()
        form.fields['cleaner'].initial = str(cleaner_id)
        form.fields['manager'].initial = str(request.user.id)
        form.fields['address'].queryset = Address.objects.filter(company__id=f'{company.id}')

        context = {
            'title': 'Добавить задачу',
            'cleaner': cleaner,
            'form': form,
        }

    return render(request, 'pages/profiles/add_task.html', context=context)


@login_required(login_url="/users/login/")
def view_report(request, task_id: int) -> render:
    task = Task.objects.filter(pk=task_id).first()
    report = CompletedTask.objects.filter(task__id=task_id).first()

    context = {
        'title': 'Просмотр отчета',
        'report': report,
        'task': task,
    }

    return render(request, 'pages/profiles/view_report.html', context=context)


@login_required(login_url="/users/login/")
def create_quality_assessment(request, task_id: int) -> render:
    if request.method == 'POST':
        task = Task.objects.filter(pk=task_id).first()
        form = QualityAssessmentForm(request.POST, request.FILES)
        print(form.data)

        if form.is_valid():
            form.save()
            task.quality_assessment = True
            task.save()

        return redirect('/users/profile/')

    else:
        task = Task.objects.filter(pk=task_id).first()
        address = task.address.all().first()
        task_report = CompletedTask.objects.filter(task__id=task_id).first()

        form = QualityAssessmentForm()
        form.fields['cleaner'].initial = task.cleaner.id
        form.fields['manager'].initial = task.manager.id
        form.fields['task'].initial = task.id
        form.fields['task_report'].initial = task_report.id
        form.fields['address'].initial = address.id

        context = {
            'title': 'Проверка качества',
            'form': form,
            'task': task,
        }

    return render(request, 'pages/profiles/create_quality_assessment.html', context=context)


@login_required(login_url="/users/login/")
def view_quality_assessment(request, task_id: int) -> render:
    task = Task.objects.filter(pk=task_id).first()
    task_report = CompletedTask.objects.filter(task__id=task_id).first()
    quality_assessment = QualityAssessment.objects.filter(task__id=task_id).first()
    context = {
        'title': 'Просмотр оценки качества',
        'task': task,
        'task_report': task_report,
        'quality_assessment': quality_assessment
    }

    return render(request, 'pages/profiles/view_quality_assessment.html', context=context)


@login_required(login_url="/users/login/")
def get_address_info(request, address_id) -> render:
    address = Address.objects.filter(pk=address_id).first()
    all_tasks = Task.objects.all().filter(address__id=address_id)
    completed_task = CompletedTask.objects.all().filter(address__id=address_id, marks='Выполнена')
    marks = QualityAssessment.objects.all().filter(address__id=address_id)
    middle_mark = 0
    for mark in marks:
        middle_mark += int(mark.mark)
    if middle_mark != 0:
        middle_mark = middle_mark / completed_task.count()

    context = {
        'title': 'Информация по адресу',
        'address': address,
        'all_tasks': all_tasks,
        'task_count': all_tasks.count(),
        'completed_task': completed_task.count(),
        'not_completed_task': all_tasks.count() - completed_task.count(),
        'middle_mark': middle_mark,
    }

    return render(request, 'pages/profiles/uk_employee/address_info.html', context=context)


@login_required(login_url="/users/login/")
def get_general_report(request) -> render:
    all_addresses = Address.objects.all()
    companies = Company.objects.all()
    companies_json = serializers.serialize('json', Company.objects.all())
    cleaners = CustomUser.objects.filter(groups__name='Дворники')
    completed_tasks = CompletedTask.objects.all()
    quality_assessment = QualityAssessment.objects.all()

    middle_mark = 0
    for mark in quality_assessment:
        middle_mark += int(mark.mark)
    if middle_mark != 0:
        middle_mark = middle_mark / quality_assessment.count()

    companies_rating: dict = {}

    for company in companies:
        rating = 0
        k = 0
        address_quality_assessment = ...
        addresses = company.address.all()
        for address in addresses:
            address_quality_assessment = QualityAssessment.objects.filter(address__id=address.id)
            for mark in address_quality_assessment:
                rating += int(mark.mark)
                k += 1
        if address_quality_assessment.count() != 0:
            rating = rating / address_quality_assessment.count()

        companies_rating[company.name] = rating

    address_task_count = []
    for address in all_addresses:
        address_task = {}
        tasks = CompletedTask.objects.filter(address__id=address.id)
        address_task['name'] = f'{address}'
        address_task['coord1'] = address.coord1
        address_task['coord2'] = address.coord2
        address_task['tasks'] = tasks.count()
        address_task_count.append(address_task)

    print(address_task_count)

    for quality in quality_assessment:
        report = CompletedTask.objects.filter(task__id=quality.task.id).first()
        print(report.photo)

    context = {
        'companies': companies,
        'companies_count': companies.count(),
        'completed_tasks_count': completed_tasks.count(),
        'cleaners_count': cleaners.count(),
        'middle_mark': middle_mark,
        'companies_rating': json.loads(json.dumps(companies_rating)),
        'companies_json': json.loads(json.dumps(companies_json)),
        'address_task_count': json.loads(json.dumps(address_task_count)),
    }
    return render(request, 'pages/general_report.html', context=context)

import datetime
from datetime import timedelta

from django.shortcuts import render, redirect
import exif

from .forms import TaskReport, AddTask, QualityAssessmentForm
from .models import Task, CompletedTask, QualityAssessment
from apps.users.models import CustomUser, Address
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
        'cleaner': cleaner,
        'all_tasks': all_tasks,
        'tasks': tasks,
        'task_count': all_tasks.count(),
        'completed_task': completed_task.count(),
        'not_completed_task': all_tasks.count() - completed_task.count(),
        'middle_mark': middle_mark,
    }

    return render(request, 'pages/profiles/cleaner_info.html', context=data)


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

        form = AddTask()
        form.fields['cleaner'].initial = str(cleaner_id)
        form.fields['manager'].initial = str(request.user.id)

        context = {
            'cleaner': cleaner,
            'form': form,
        }

    return render(request, 'pages/profiles/add_task.html', context=context)


@login_required(login_url="/users/login/")
def view_report(request, task_id: int) -> render:
    task = Task.objects.filter(pk=task_id).first()
    report = CompletedTask.objects.filter(task__id=task_id).first()

    context = {
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
        'address': address,
        'all_tasks': all_tasks,
        'task_count': all_tasks.count(),
        'completed_task': completed_task.count(),
        'not_completed_task': all_tasks.count() - completed_task.count(),
        'middle_mark': middle_mark,
    }

    return render(request, 'pages/profiles/uk_employee/address_info.html', context=context)

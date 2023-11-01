from django.shortcuts import render, redirect
import exif

from .forms import TaskReport, AddTask
from .models import Task, CompletedTask
from apps.users.models import CustomUser
from django.contrib.auth.decorators import login_required

from .services.image_service import image_coordinates


def get_tasks(request):
    tasks = Task.objects.all()
    managers = CustomUser.objects.all().filter(groups__name='Управляющие')
    cleaners = CustomUser.objects.all().filter(groups__name='Дворники')
    user = CustomUser.objects.filter(pk=request.user.id).first()

    try:
        user_group = user.groups.all().first()
    except AttributeError:
        print('Groups not found')

    data = {
        'tasks': tasks,
        'managers': managers,
        'cleaners': cleaners,
        'user': user,
    }

    if user_group.name == 'Дворники':
        return render(request, 'pages/cleaner_profile.html', context=data)

    elif user_group.name == 'Управляющие':
        return render(request, 'pages/manager_profile.html', context=data)

    return render(request, 'pages/base.html', context=data)


@login_required(login_url="/users/login/")
def cleaner_task_report(request, task_id: int) -> render:
    task = Task.objects.filter(pk=task_id).first()
    address = task.address.all().first()

    if request.method == 'POST':
        request.POST._mutable = True

        form = TaskReport(request.POST, request.FILES)

        file = request.FILES['photo']

        image = exif.Image(file)
        print(image_coordinates(image.gps_latitude, image.gps_latitude_ref))
        print(image_coordinates(image.gps_longitude, image.gps_longitude_ref))
        print(form.data)

        if form.is_valid():
            print(form.data)
            form.save()
            task.is_active = False
            task.save()

        return redirect('/users/profile/')

    else:
        form = TaskReport()
        form.fields['task'].initial = str(task.id)
        form.fields['cleaner'].initial = str(task.cleaner.id)
        form.fields['address'].initial = str(address.id)
        form.fields['manager'].initial = str(task.manager.id)

        context = {
            'task': task,
            'form': form,
        }

    return render(request, 'pages/add_report.html', context=context)


@login_required()
def get_cleaner_tasks(request, cleaner_id: int) -> render:
    cleaner = CustomUser.objects.all().filter(pk=cleaner_id).first()
    tasks = Task.objects.all().filter(cleaner__id=cleaner_id)

    data = {
        'cleaner': cleaner,
        'tasks': tasks,
    }

    return render(request, 'pages/profiles/cleaner_info.html', context=data)


@login_required()
def add_task(request, cleaner_id: int) -> render:
    if request.method == 'POST':
        request.POST._mutable = True
        form = AddTask(request.POST)

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

    return render(request, 'pages/add_task.html', context=context)


@login_required()
def view_report(request, task_id: int) -> render:
    report = CompletedTask.objects.filter(task__id=task_id).first()
    context = {
        'report': report,
    }

    return render(request, 'pages/view_report.html', context=context)


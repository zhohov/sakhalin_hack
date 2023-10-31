import datetime

from django.shortcuts import render, redirect
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import exif

from .forms import TaskReport
from .models import Task
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
        print(user_group.name)
        return render(request, 'pages/base.html', context=data)

    return render(request, 'pages/base.html', context=data)


@login_required(login_url="/users/login/")
def cleaner_task_report(request, task_id: int | None) -> render:
    task = Task.objects.filter(pk=task_id).first()
    address = task.address.all().first()

    if request.method == 'POST':
        request.POST._mutable = True

        form = TaskReport(request.POST, request.FILES)

        file = request.FILES['photo']

        image = exif.Image(file)
        print(image_coordinates(image.gps_latitude, image.gps_latitude_ref))
        print(image_coordinates(image.gps_longitude, image.gps_longitude_ref))

        address = task.address.all().first()

        form.data['task'] = str(task.id)
        form.data['cleaner'] = str(task.cleaner.id)
        form.data['address'] = str(address.id)
        print(form.data)

        if form.is_valid():
            print(form.data)
            form.save()

        return redirect('/users/profile/')


    else:
        form = TaskReport()
        form.fields['task'].initial = str(task.id)
        form.fields['cleaner'].initial = str(task.cleaner.id)
        form.fields['address'].initial = str(address.id)
        context = {
            'task': task,
            'form': form,
        }

    return render(request, 'pages/add_report.html', context=context)

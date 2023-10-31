from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.tasks.models import Task


@login_required(login_url="/users/login/")
def user_profile(request) -> render:
    try:
        user_group = request.user.groups.all().first()
        tasks = Task.objects.all().filter(cleaner__id=request.user.id)
        data = {
            'tasks': tasks
        }

    except AttributeError:
        raise render(request, template_name='pages/profiles/error.html')

    if user_group.name == 'Дворники':
        return render(request, template_name='pages/profiles/cleaner_profile.html', context=data)

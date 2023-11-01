from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.tasks.models import Task
from .models import CustomUser


@login_required(login_url="/users/login/")
def user_profile(request) -> render:
    try:
        user_group = request.user.groups.all().first()
        if user_group.name == 'Дворники':
            tasks = Task.objects.all().filter(cleaner__id=request.user.id)
            data = {
                'tasks': tasks
            }
            return render(request, template_name='pages/profiles/cleaner_profile.html', context=data)

        elif user_group.name == 'Управляющие':
            user_company = request.user.company.all().first()
            cleaners = CustomUser.objects.all().filter(groups__name='Дворники', company__name=user_company.name)
            data = {
                'company': user_company,
                'cleaners': cleaners,
            }
            print(data)
            return render(request, template_name='pages/profiles/manager_profile.html', context=data)

    except AttributeError:
        raise render(request, template_name='pages/profiles/error.html')

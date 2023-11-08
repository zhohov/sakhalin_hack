from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import UserAppealForm, UKAppealForm, UserAppealAnswerForm, UKAppealAnswerForm
from .models import Appeal, AppealAnswer
from apps.users.models import CustomUser


@login_required(login_url="/users/login/")
def create_appeal(request):
    request_user = CustomUser.objects.filter(pk=request.user.id).first()
    user_group = request_user.groups.first()
    company = request_user.company.first()

    if request.method == 'POST':
        request.POST._mutable = True
        if user_group.name == 'Сотрудники ЖЭК':
            form = UKAppealForm(request.POST)

            if form.is_valid():
                form.save()

        else:
            form = UserAppealForm(request.POST)

            if form.is_valid():
                form.save()

        return redirect('/users/profile/')

    else:
        if user_group.name == 'Сотрудники ЖЭК':
            form = UKAppealForm()
            form.fields['company'].initial = str(company.id)
            form.fields['recipient'].queryset = CustomUser\
                .objects.filter(company=company.id).exclude(groups=user_group.id)

            context = {
                'form': form,
            }

        else:
            form = UserAppealForm()
            form.fields['sender'].initial = str(request.user.id)
            form.fields['company'].initial = str(company.id)
            context = {
                'form': form,
            }

        return render(request, 'pages/appeals/create_appeal.html', context=context)


@login_required(login_url="/users/login/")
def create_appeal_answer(request, appeal_id: int):
    request_user = CustomUser.objects.filter(pk=request.user.id).first()
    user_group = request_user.groups.first()
    appeal = Appeal.objects.filter(pk=appeal_id).first()

    if request.method == 'POST':
        request.POST._mutable = True
        if user_group.name == 'Сотрудник ЖЭК':
            form = UKAppealAnswerForm(request.POST)

        else:
            form = UserAppealAnswerForm(request.POST)

        if form.is_valid():
            print(form.data)
            appeal.is_active = False
            form.save()
            appeal.save()

        return redirect('/users/profile/')

    else:
        if user_group.name == 'Сотрудники ЖЭК':
            form = UKAppealAnswerForm()

            form.fields['appeal'].initial = str(appeal.id)
            form.fields['sender'].initial = str(appeal.sender.id)
            form.fields['company'].initial = str(appeal.company.id)

            context = {
                'form': form,
                'appeal': appeal,
            }

        else:
            form = UserAppealAnswerForm()

            form.fields['appeal'].initial = str(appeal.id)
            form.fields['recipient'].initial = str(appeal.recipient.id)
            form.fields['company'].initial = str(appeal.recipient.id)

            context = {
                'form': form,
                'appeal': appeal,
            }

    return render(request, 'pages/appeals/create_appeal_answer.html', context=context)


@login_required()
def view_appeal_answer(request, appeal_id: int) -> render:
    appeal = Appeal.objects.filter(pk=appeal_id).first()
    answer = AppealAnswer.objects.filter(appeal__id=appeal_id).first()
    context = {
        'appeal': appeal,
        'answer': answer,
    }

    return render(request, 'pages/appeals/view_appeal_answer.html', context=context)

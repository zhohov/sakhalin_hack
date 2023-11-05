from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import AppealForm, AppealAnswerForm
from .models import Appeal, AppealAnswer


@login_required(login_url="/users/login/")
def create_appeal(request):
    if request.method == 'POST':
        request.POST._mutable = True
        form = AppealForm(request.POST)

        if form.is_valid():
            print(form.data)
            form.save()

        return redirect('/users/profile/')

    else:
        form = AppealForm()
        form.fields['sender'].initial = str(request.user.id)
        context = {
            'form': form,

        }

    return render(request, 'pages/appeals/create_appeal.html', context=context)


@login_required(login_url="/users/login/")
def create_appeal_answer(request, appeal_id: int):
    appeal = Appeal.objects.filter(pk=appeal_id).first()
    if request.method == 'POST':
        request.POST._mutable = True
        form = AppealAnswerForm(request.POST)

        if form.is_valid():
            print(form.data)
            appeal.is_active = False
            form.save()
            appeal.save()

        return redirect('/users/profile/')

    else:
        form = AppealAnswerForm()

        form.fields['appeal'].initial = str(appeal.id)
        form.fields['sender'].initial = str(appeal.sender.id)
        form.fields['recipient'].initial = str(appeal.recipient.id)

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

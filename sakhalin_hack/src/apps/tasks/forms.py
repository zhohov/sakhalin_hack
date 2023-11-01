from django.forms import ModelForm, widgets
from .models import Task, CompletedTask


class AddTask(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'date': widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class TaskReport(ModelForm):
    class Meta:
        model = CompletedTask
        fields = '__all__'
        widgets = {
            'date': widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

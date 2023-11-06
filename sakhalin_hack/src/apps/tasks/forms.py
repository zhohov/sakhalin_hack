from django.forms import ModelForm, widgets, HiddenInput
from .models import Task, CompletedTask, QualityAssessment


class AddTask(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'date': widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
            'cleaner': widgets.HiddenInput(),
            'manager': widgets.HiddenInput(),
            'is_active': widgets.HiddenInput(),
            'quality_assessment': widgets.HiddenInput(),
        }


class TaskReport(ModelForm):
    class Meta:
        model = CompletedTask
        fields = '__all__'
        widgets = {
            'date': widgets.HiddenInput(),
            'task': widgets.HiddenInput(),
            'cleaner': widgets.HiddenInput(),
            'manager': widgets.HiddenInput(),
            'verified_address': widgets.HiddenInput(),
            'coord1': widgets.HiddenInput(),
            'coord2': widgets.HiddenInput(),
            'is_active': widgets.HiddenInput(),
            'address': widgets.HiddenInput(),
        }


class QualityAssessmentForm(ModelForm):
    class Meta:
        model = QualityAssessment
        fields = '__all__'
        widgets = {
            'date': widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
            'cleaner': widgets.HiddenInput(),
            'manager': widgets.HiddenInput(),
            'task': widgets.HiddenInput(),
            'task_report': widgets.HiddenInput(),
            'address': widgets.HiddenInput(),
        }

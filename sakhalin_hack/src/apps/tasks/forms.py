from django.forms import ModelForm, widgets
from .models import CompletedTask


class TaskReport(ModelForm):
    class Meta:
        model = CompletedTask
        fields = '__all__'
        widgets = {
            'date': widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

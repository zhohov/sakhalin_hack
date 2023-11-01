from django.forms import ModelForm, widgets

from .models import Appeal, AppealAnswer


class AppealForm(ModelForm):
    class Meta:
        model = Appeal
        fields = '__all__'
        widgets = {
            'date': widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class AppealAnswerForm(ModelForm):
    class Meta:
        model = AppealAnswer
        fields = '__all__'
        widgets = {
            'date': widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

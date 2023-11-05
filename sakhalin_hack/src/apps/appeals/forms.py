from django.forms import ModelForm, widgets, forms

from .models import Appeal, AppealAnswer


class AppealForm(ModelForm):
    class Meta:
        model = Appeal
        fields = '__all__'
        widgets = {
            'date': widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
            'sender': widgets.HiddenInput(),
            'is_active': widgets.HiddenInput()
        }


class AppealAnswerForm(ModelForm):
    class Meta:
        model = AppealAnswer
        fields = '__all__'
        widgets = {
            'date': widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
            'appeal': widgets.HiddenInput(),
            'sender': widgets.HiddenInput(),
            'recipient': widgets.HiddenInput()
        }

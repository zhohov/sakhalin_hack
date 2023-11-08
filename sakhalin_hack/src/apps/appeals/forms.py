from django.forms import ModelForm, widgets, forms

from .models import Appeal, AppealAnswer


class UserAppealForm(ModelForm):
    class Meta:
        model = Appeal
        fields = '__all__'
        widgets = {
            'sender': widgets.HiddenInput(),
            'is_active': widgets.HiddenInput(),
            'recipient': widgets.HiddenInput(),
            'company': widgets.HiddenInput(),
        }


class UKAppealForm(ModelForm):
    class Meta:
        model = Appeal
        fields = '__all__'
        widgets = {
            'sender': widgets.HiddenInput(),
            'is_active': widgets.HiddenInput(),
            'company': widgets.HiddenInput(),
        }


class UserAppealAnswerForm(ModelForm):
    class Meta:
        model = AppealAnswer
        fields = '__all__'
        widgets = {
            'appeal': widgets.HiddenInput(),
            'sender': widgets.HiddenInput(),
            'recipient': widgets.HiddenInput(),
            'company': widgets.HiddenInput(),
        }


class UKAppealAnswerForm(ModelForm):
    class Meta:
        model = AppealAnswer
        fields = '__all__'
        widgets = {
            'date': widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
            'appeal': widgets.HiddenInput(),
            'sender': widgets.HiddenInput(),
            'recipient': widgets.HiddenInput(),
            'company': widgets.HiddenInput(),
        }

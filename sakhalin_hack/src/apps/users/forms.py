from django import forms


class EmailLogin(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class PhoneForm(forms.Form):
    phone_number = forms.CharField()


class OTPForm(forms.Form):
    otp_code = forms.CharField()

import re

from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.layout import Layout, Field
from django.forms import ModelForm
from django import forms
from pyotp import totp
from .models import User


def phone_number_validation(phone_number):
    patter_number = re.compile("^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$")
    msg = None
    if not re.match(patter_number, str(phone_number)):
        msg = "Phone number must be in Indian Format +91 "\
              "Eg : 977587666,0 9754845789,0-9778545896,+91 9456211568, " \
              "     91 9857842356,919578965389,03595-259506,03592 245902"
    # else :
    #     if not verify_phone_number(phone_number):
    #         msg = "Phone number is valid but doesnot exist "
    return msg


class UserSignUp(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2',
                  'phone_number', 'gender', 'profile_photo']

    def __init__(self, *args, **kwargs):
        super(UserSignUp, self).__init__(*args, **kwargs)
        helper = self.helper = FormHelper()

        # Moving field labels into placeholders
        layout = helper.layout = Layout()
        for field_name, field in self.fields.items():
            layout.append(Field(field_name, placeholder=field.label))
        helper.form_show_labels = False

    def clean(self):
        cleaned_data = super(UserSignUp, self).clean()

        email = cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            self.add_error('email', "this email already exist")

        msg_returned = phone_number_validation(cleaned_data.get("phone_number"))
        if msg_returned:
            self.add_error('phone_number', msg_returned)

        return cleaned_data


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'phone_number', 'gender', 'profile_photo']

    def clean(self):
        cleaned_data = super(UserUpdateForm, self).clean()

        msg_returned = phone_number_validation(cleaned_data.get("phone_number"))
        if msg_returned:
            self.add_error('phone_number', msg_returned)

        return cleaned_data


class PhoneNumber(forms.Form):
    otp = forms.IntegerField(help_text="Enter the otp")

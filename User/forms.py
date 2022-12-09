from django.db import models
from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.forms.widgets import SelectDateWidget
from Tontine.admin import UserCreationForm
from django import forms


'''class DateSelectorWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        days = [(day, day) for day in range(1, 32)]
        months = [(month, month) for month in range(1, 13)]
        years = [(year, year) for year in [2018, 2019, 2020]]
        widgets = [
            forms.Select(attrs=attrs, choices=days),
            forms.Select(attrs=attrs, choices=months),
            forms.Select(attrs=attrs, choices=years),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, date):
            return [value.day, value.month, value.year]
        elif isinstance(value, str):
            year, month, day = value.split('-')
            return [day, month, year]
        return [None, None, None]

    def value_from_datadict(self, data, files, name):
        day, month, year = super().value_from_datadict(data, files, name)
        # DateField expects a single string that it can parse into a date.
        return '{}-{}-{}'.format(year, month, day)

'''


class FormUser(ModelForm):

    class Meta:
        model = UserCreationForm
        #fields = '__all__'
        fields = ['username', 'surname', 'address', 'email', 'telephone',
                  'date_of_birth', 'profession', 'password', 'password1']
        # fields = ['username','first_name','last_name','email','password','password1']

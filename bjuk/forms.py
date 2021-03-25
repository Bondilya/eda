from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.forms import ModelMultipleChoiceField

from .models import *


class AddFoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = '__all__'
        widgets = {'author': forms.HiddenInput}


class AddRacionForm(forms.ModelForm):
    food = forms.ModelChoiceField(queryset=Food.objects.all(), label='Блюда', widget=forms.widgets.Select())
    gramm = forms.FloatField(widget=forms.widgets.NumberInput(), label='Грамм')

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super(AddRacionForm, self).__init__(*args, **kwargs)
        self.fields['food'].queryset = self.fields['food'].queryset.filter(author = current_user)
        self.fields['meal'].queryset = self.fields['meal'].queryset.filter(author = current_user)

    class Meta:
        model = Racion
        fields = '__all__'
        widgets = {'author': forms.HiddenInput}


class ChangeRacionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super(ChangeRacionForm, self).__init__(*args, **kwargs)
        self.fields['meal'].queryset = self.fields['meal'].queryset.filter(author = current_user)
        self.fields['food'].queryset = self.fields['food'].queryset.filter(author = current_user)

    class Meta:
        model = Racion
        fields = ('food', 'gramm', 'meal')
        widgets = {'author': forms.HiddenInput}


class AddMealForm(forms.ModelForm):
    time = forms.TimeField(label='Время приема', help_text='*не обязательно', required=False, widget=forms.widgets.TimeInput())
    class Meta:
        model = Meal
        fields = ('name', 'time')
        widgets = {'author': forms.HiddenInput}


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput,
                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль (повторно)', widget=forms.PasswordInput,
                help_text='Введите тот же самый пароль еще раз для проверки')

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError('Введенные пароли не совпадают',
                                  code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        if commit:
            user.save()
        user_registrated.send(RegisterUserForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2')

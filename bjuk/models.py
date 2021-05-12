from django.db import models
from django.core import validators
from django.contrib.auth.models import User
from django.dispatch import Signal

import uuid
from .utilities import *


class Food(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    bel = models.FloatField(validators = [validators.MinValueValidator(0.1)], verbose_name='Белки')
    jir = models.FloatField(validators = [validators.MinValueValidator(0.1)], verbose_name='Жиры')
    ugl = models.FloatField(validators = [validators.MinValueValidator(0.1)], verbose_name='Углеводы')
    cal = models.FloatField(validators = [validators.MinValueValidator(0.1)], verbose_name='Калории')
    author = models.ForeignKey(User, on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'Еда'
        verbose_name_plural = 'Еда'

    def __str__(self):
        return self.title

class Meal(models.Model):
    name = models.CharField(max_length=65, verbose_name='Название приема пищи', blank = False)
    time = models.TimeField(verbose_name='Время приема', blank = True, null = True)
    foods = models.ManyToManyField(Food, through='Racion', through_fields=('meal', 'food'), verbose_name = 'Блюда')
    author = models.ForeignKey(User, on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'Прием пищи'
        verbose_name_plural = 'Приемы пищи'

    def __str__(self):
        return self.name

class Racion(models.Model):
    meal = models.ForeignKey(Meal, on_delete = models.CASCADE, verbose_name = 'Прием пищи')
    food = models.ForeignKey(Food, on_delete = models.CASCADE, verbose_name = 'Блюдо')
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    gramm = models.FloatField(validators = [validators.MinValueValidator(0.1)], verbose_name='Грамм')
    def bel(self):
        b = (self.gramm/100)*self.food.bel
        return b
    def jir(self):
        j = (self.gramm/100)*self.food.jir
        return j
    def ugl(self):
        u = (self.gramm/100)*self.food.ugl
        return u
    def cal(self):
        c = (self.gramm/100)*self.food.cal
        return c

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'


user_registrated = Signal(providing_args=['instance'])

def user_registrated_dispathcer(sender, **kwargs):
    send_activation_notification(kwargs['instance'])
user_registrated.connect(user_registrated_dispathcer)#привязка обработчика к сигналу с помощью метода connect()

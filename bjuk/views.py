from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core import serializers
# from django.template import TemplateDoesNotExist
# from django.template.loader import get_template
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
# from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView
# from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView
# from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
# from django.views.generic.base import TemplateView
# from django.core.signing import BadSignature
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import *
from .utilities import create_user_id
from datetime import timedelta
from django.db.models import Q
from django.contrib.auth.models import Group
import json
from django.forms.models import model_to_dict


@login_required()
def index(request):
    foods = Food.objects.filter(author = request.user.pk)
    meals = Meal.objects.filter(author = request.user.pk)
    racions = Racion.objects.filter(author = request.user.pk)
    sum_bel=0;sum_jir=0;sum_ugl=0;sum_cal=0
    for racion in racions:
        b = (racion.gramm/100.0)*racion.food.bel
        j = (racion.gramm/100.0)*racion.food.jir
        u = (racion.gramm/100.0)*racion.food.ugl
        c = (racion.gramm/100.0)*racion.food.cal
        sum_bel+=b;sum_jir+=j;sum_ugl+=u;sum_cal+=c
    if 'username' in request.session and not request.user.groups.filter(name='guests'):
        return redirect('data')
    context = {'foods':foods, 'meals':meals, 'racions':racions, 'sum_bel':sum_bel, 'sum_jir':sum_jir, 'sum_ugl':sum_ugl, 'sum_cal':sum_cal}
    return render(request, 'bjuk/index.html',context)


def demo_login(request):
    if 'username' in request.session:
        guest = User.objects.get(username=request.session['username'])
        login(request, guest, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('index')
    else:
        q = Q(username__startswith = 'Guest') & Q(groups = 1)
        if User.objects.filter(q):
            last = User.objects.filter(q).last()
            id = create_user_id(last.username)
            guest = User.objects.create_user(username='Guest' + str(id), password='password'+ str(id))
            guest.groups.add(1)
        else:
            guest = User.objects.create_user(username='Guest1', password='password1')
            guest.groups.add(1)
        login(request, guest, backend='django.contrib.auth.backend.ModelBackend')
        return redirect('index')


def test_session(request):
    if 'demo_logged' in request.session:
        return HttpResponse(request.session['username'])
    else:
        return HttpResponse(None)


def logout_view(request):
    if request.user.groups.filter(name='guests'):
        username = request.user.username
        logout(request)
        request.session['username'] = username
    else:
        logout(request)
    return redirect('account_login')


def data(request):
    return render(request, 'bjuk/data_transfer.html', {'name':request.session['username']})

def data_transfer(request):
    if 'username' in request.session:
        u = User.objects.get(username=request.session['username'])
        Racion.objects.filter(author = u).update(author = request.user)
        Meal.objects.filter(author = u).update(author=request.user)
        Food.objects.filter(author = u).update(author=request.user)
        u.delete()
        del request.session['username']
        messages.add_message(request, messages.SUCCESS, '???????????? ????????????????????')
    return redirect('index')


def data_delete(request):
    if 'username' in request.session:
        u = User.objects.get(username=request.session['username'])
        u.delete()
        del request.session['username']
    return redirect('index')


'''**************************************??????***********************************************'''
class ChangeFood(UpdateView, LoginRequiredMixin):
    model = Food
    form_class = AddFoodForm
    template_name = 'bjuk/change_food.html'
    success_url = '/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class DeleteFood(DeleteView, LoginRequiredMixin):
    model = Food
    success_url = '/'
    template_name = 'bjuk/delete_food.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


@login_required
def AddFood(request):
    if request.method == 'POST':
        form = AddFoodForm(request.POST)
        if form.is_valid():
            food = form.save()
            messages.add_message(request, messages.SUCCESS, '?????????? ??????????????????')
            return redirect('index')
    else:
        form = AddFoodForm(initial={'author': request.user.pk})
    context = {'form': form,}
    return render(request, 'bjuk/add_food.html', context)

'''**************************************???????????? ????????***********************************************'''
@login_required
def AddMeal(request):
    if request.method == 'POST':
        form = AddMealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit = False)
            meal.author = request.user
            meal.save()
            messages.add_message(request, messages.SUCCESS, '?????????? ???????? ????????????????')
            return redirect('index')
    else:
        form = AddMealForm(initial={'author': request.user})
    context = {'form': form,}
    return render(request, 'bjuk/add_meal.html', context)


class ChangeMeal(UpdateView, LoginRequiredMixin):
    model = Meal
    form_class = AddMealForm
    template_name = 'bjuk/change_meal.html'
    success_url = '/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class DeleteMeal(DeleteView, LoginRequiredMixin):
    model = Meal
    success_url = '/'
    template_name = 'bjuk/delete_meal.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

'''**************************************???????????? ???????? + ??????***********************************************'''
@login_required
def AddRacion(request):
    if request.method == 'POST':
        form = AddRacionForm(request.POST, current_user = request.user, initial = {'author' : request.user})
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            form = AddRacionForm()
            context = {'form':form}
            return render(request,'bjuk/add_racion.html', context)
    else:
        form = AddRacionForm(current_user = request.user, initial={'author': request.user})
        context = {'form':form}
        return render(request,'bjuk/add_racion.html', context)


@login_required
def ChangeRacion(request, pk):
    racion = get_object_or_404(Racion, pk=pk)
    if request.method == 'POST':
        form = ChangeRacionForm(request.POST, current_user = request.user, instance = racion)
        if form.is_valid():
            racion = form.save()
            messages.add_message(request, messages.SUCCESS, '?????????? ????????????????????')
            return redirect('index')
    else:
        form = ChangeRacionForm(current_user = request.user, instance = racion)
    context = {'form': form, 'racion' : racion}
    return render(request, 'bjuk/change_racion.html', context)


@login_required
def DeleteRacion(request, pk):
    racion = get_object_or_404(Racion, pk=pk)
    if request.method == 'POST':
        racion.delete()
        messages.add_message(request, messages.SUCCESS, '?????????? ??????????????')
        return redirect('index')
    else:
        context = {'racion': racion}
        return render(request, 'bjuk/delete_racion.html', context)


'''***********************************************????????????????????????****************************************************************************'''
'''
class BJULoginView(LoginView):
    template_name = 'main/login.html'
    success_url = reverse_lazy('index')


class BJULogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'main/logout.html'


class BJUPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('profile')
    success_message = '???????????? ???????????????????????? ??????????????'


class RegisterUserView(CreateView):
    model = User
    template_name = 'main/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('register_done')


class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(User, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.save()
    return render(request, template)


class BJUPasswordResetView(PasswordResetView):
    template_name = 'main/password_reset.html'
    subject_template_name = 'email/reset_letter_subject.txt'
    email_template_name = 'email/reset_letter_body.txt'
    success_url = reverse_lazy('password_reset_done')


class BJUPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'main/password_reset_done.html'


class BJUPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'main/password_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class BJUPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'main/password_complete.html'
'''

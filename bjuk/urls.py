from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='index'),

    path('add_food/', AddFood, name='add_food'),
    path('delete_food/<int:pk>/', DeleteFood.as_view(), name='delete_food'),
    path('change_food/<int:pk>/', ChangeFood.as_view(), name='change_food'),

    path('add_meal/', AddMeal, name='add_meal'),
    path('delete_meal/<int:pk>/', DeleteMeal.as_view(), name='delete_meal'),
    path('change_meal/<int:pk>/', ChangeMeal.as_view(), name='change_meal'),

    path('add_racion/', AddRacion, name='add_racion'),
    path('delete_racion/<int:pk>/', DeleteRacion, name='delete_racion'),
    path('change_racion/<int:pk>/', ChangeRacion, name='change_racion'),

    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/login/', BJULoginView.as_view(), name='login'),

    path('accounts/password/reset/done/', BJUPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/password/reset/', BJUPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password/confirm/complete/', BJUPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('accounts/password/confirm/<uidb64>/<token>/', BJUPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('accounts/password/change/', BJUPasswordChangeView.as_view(), name='password_change'),
    path('accounts/logout/', BJULogoutView.as_view(), name='logout'),

    path('social/', include('social_django.urls', namespace='social')),
]

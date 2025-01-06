from django.urls import path
from .views import *
from .views import ServicesListView, MastersListView

urlpatterns = [
    path('', index, name='home'),
    path('services/', ServicesListView.as_view(), name='services_list'),
    path('masters/', MastersListView.as_view(), name='masters'),
    path('appointment/', Appointment, name='appointment'),
    path('history/', history_appointment, name='history_appointment'),
    path('success_appointment/', success_appointment, name='success_appointment'),
    path('login/', loginPage, name='login'),
    path('masters_login/', masterslogPage, name='masters_login'),
    path('masters_register/', mastersregPage, name='masters_register'),
    path('masters_profile/', mastersPage, name='masters_profile'),
    path('future_appointment/', future_appointment, name='future_appointment'),
    path('history_past_appointment/', history_past_appointment, name='history_past_appointment'),
    path('register/', registerPage, name='register'),
    path('logout/', doLogout, name='logout'),
    path('profile/', profilePage, name='profile'),
    path('about/', about, name='about'),
    path('feedback/',feedback, name='feedback'),
]

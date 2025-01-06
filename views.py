from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from django.views.generic import ListView

def index(request):
    return render(request, 'salon_app/base.html')

class ServicesListView(ListView):
    model = Service
    context_object_name = 'services'
    template_name = 'salon_app/services_list.html'

class MastersListView(ListView):
    model = Master
    context_object_name = 'masters'
    template_name = 'salon_app/masters.html'

@login_required
def Appointment(request):
    masters = Master.objects.all()
    services = Service.objects.all()
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            master = form.cleaned_data['master']
            service = form.cleaned_data['service']
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']

            if check_availability(master, service, date, time):
                appointment = Appointment.objects.create(
                    user=request.user,
                    master=master,
                    service=service,
                    date=date,
                    time=time
                )
                appointment.save()
                return redirect('salon_app/success_appointment.html')
            else:
                form.add_error(None, 'К сожалению, выбранное время занято. Попробуйте выбрать другую дату или время.')
    else:
        form = AppointmentForm()
    all_time = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00']

    yesterday = datetime.today()
    min_day_value = yesterday.strftime("%Y-%m-%d")
    context = {'form': form, 'masters': masters, 'services': services,'min_day_value': min_day_value, 'all_time': all_time}
    return render(request, 'salon_app/appointment.html', context)


def check_availability(master, service, date, time):
    appointments = Appointment.objects.filter(
        master=master,
        service=service,
    ).filter(date=date).filter(time=time)

    if appointments.exists():
        return False
    return True

def history_appointment(request):
    return render(request, 'salon_app/history.html')

def success_appointment(request):
    if request.POST:
        user = request.POST['user']
        master = request.POST['service']
        service = request.POST['service']
        date = request.POST['date']
        time = request.POST['time']
        element = Appointment(
                    user=user,
                    master=master,
                    service=service,
                    date=date,
                    time=time)
        element.save()
    return render(request, 'salon_app/success_appointment.html')

def about(request):
    return render(request, 'salon_app/about.html')

def feedback(request):
    return render(request, 'salon_app/feedback.html')

def doLogout(request):
    logout(request)
    return render(request, 'salon_app/base.html')

def future_appointment(request):
    return render(request, 'salon_app/future_appointment.html')

def history_past_appointment(request):
    return render(request, 'salon_app/history_past_appointment.html')

def loginPage(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                form.add_error(None, 'Неверные данные!')
    return render(request, 'salon_app/login.html', {'form': form})

def registerPage(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    return render(request, 'salon_app/register.html', {'form': form})

def profilePage(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'salon_app/profile.html', {'user': request.user})


def mastersPage(request):
    if not request.master.is_authenticated:
        return redirect('masters_login')
    return render(request, 'salon_app/masters_profile.html', {'master': request.master})

def masterslogPage(request):
    form = MastersLoginForm()
    if request.method == 'POST':
        form = MastersLoginForm(request.POST)
        if form.is_valid():
            master = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if master is not None:
                login(request, master)
                return redirect('masters_profile')
            else:
                form.add_error(None, 'Неверные данные!')
    return render(request, 'salon_app/masters_login.html', {'form': form})
def mastersregPage(request):
    form = MastersRegisterForm()
    if request.method == 'POST':
        form = MastersRegisterForm(request.POST)
        if form.is_valid():
            master = form.save(commit=False)
            master.set_password(form.cleaned_data['password'])
            master.save()
            return redirect('masters_login')
    return render(request, 'salon_app/masters_register.html', {'form': form})


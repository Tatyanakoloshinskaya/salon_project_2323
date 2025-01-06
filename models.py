from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db.models import *
from django.conf import settings


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()

    def __str__(self):
        return self.name


class Feedback(models.Model):
    feedback_dt = models.DateTimeField(auto_now=True)
    feedback_name = models.CharField(max_length=100, verbose_name='Имя')
    feedback_phone = models.CharField(max_length=100, verbose_name='Номер телефона')

    def __str__(self):
        return f"{self.feedback_dt} - {self.feedback_name} - {self.feedback_phone}"


class CustomUserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, username, fio, experience, phone, password, password_confirm, **extra_fields):

        if not username:
            raise ValueError(_('The given username must be set'))
        if not fio:
            raise ValueError(_('The given fio must be set'))
        if not experience:
            raise ValueError(_('The given experience must be set'))
        if not phone:
            raise ValueError(_('The given phone must be set'))

        user = self.model(username=username, fio=fio, experience=experience, phone=phone,  password=password, password_confirm=password_confirm, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class Master(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    fio = models.CharField(max_length=150)
    experience = models.IntegerField()
    phone = models.CharField(max_length=11)
    password = models.CharField(max_length=51)
    password_confirm = models.CharField(max_length=51)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['fio', 'experience', 'phone', 'password', 'password_confirm']

    class Meta:
        verbose_name = _('master')
        verbose_name_plural = _('masters')

    def __str__(self):
        return f"{self.username}, {self.fio}, {self.experience}, {self.phone}, {self.password}, {self.password_confirm}"


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    master = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.user} - {self.master} - {self.service} - {self.date} - {self.time}"





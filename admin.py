from django.contrib import admin
from .models import *

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('username', 'fio', 'experience', 'phone')



@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback_dt', 'feedback_name', 'feedback_phone')

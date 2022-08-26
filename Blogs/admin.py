from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'date_created']

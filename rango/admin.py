# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib import admin
from rango.models import Category, Page
# Register your models here.
from models import UserProfile


class pageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

class catAdmin(admin.ModelAdmin):
    list_display=('name','views','likes')


admin.site.register(Category, catAdmin)
admin.site.register(Page,pageAdmin)
admin.site.register(UserProfile)
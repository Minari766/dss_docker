from django.contrib import admin
from django import forms
from .models import Post, Area, Attraction, Category, Like


admin.site.register(Post)
admin.site.register(Area)
admin.site.register(Attraction)
admin.site.register(Category)
admin.site.register(Like)


#
# Register your models here.

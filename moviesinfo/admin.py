from django.contrib import admin

# Register your models here.
from moviesinfo.models import Movies, Platform, Review

admin.site.register(Movies)
admin.site.register(Platform)
admin.site.register(Review)
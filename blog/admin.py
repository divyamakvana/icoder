from django.contrib import admin
from .models import Blog, BlogComment

admin.site.register((Blog, BlogComment))


from django.contrib import admin

from .models import Category
from .models import Article

admin.site.register(Category)
admin.site.register(Article)
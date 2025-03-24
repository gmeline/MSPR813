from django.contrib import admin

from .models import Category
from .models import Article
from .models import GeneratedImage

admin.site.register(Category)
admin.site.register(Article)
admin.site.register(GeneratedImage)
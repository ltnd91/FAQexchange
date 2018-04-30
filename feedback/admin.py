from django.contrib import admin

# Register your models here.

from .models import Answer
from .models import Comment

admin.site.register(Answer)
admin.site.register(Comment)

from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Post)
admin.site.register(models.Comment)
admin.site.register(models.UserProfile)
admin.site.register(models.Notification)
admin.site.register(models.Tag)

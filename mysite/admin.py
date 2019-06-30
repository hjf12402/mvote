from django.contrib import admin
from . import models

# Register your models here.
class PollAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'enabled']
    ordering = ('-created_at',)

class PollItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'poll', 'vote']
    ordering = ('poll',)

admin.site.register(models.Profile)
admin.site.register(models.Poll, PollAdmin)
admin.site.register(models.PollItem, PollItemAdmin)
from django.contrib import admin
from .models import Reminder

# Register your models here.

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'user',
        'application',
        'reminder_type',
        'due_date',
        'is_completed',
        'is_sent',
    )

    list_filter = (
        'reminder_type',
        'notification_channel',
        'is_completed',
        'is_sent',
        'due_date',
    )

    search_fields = (
        'title',
        'user__username',
        'application__job_title',
        'application__company_name',
    )

    ordering = ('due_date',)
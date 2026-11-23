
from django.contrib import admin
from .models import JobApplication, ApplicationHistory


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):

    list_display = (
        'job_title',
        'company_name',
        'user',
        'status',
        'date_applied',
        'deadline',
    )

    list_filter = (
        'status',
        'employment_type',
        'date_applied',
    )

    search_fields = (
        'job_title',
        'company_name',
        'user__username',
    )

    ordering = ('-created_at',)

@admin.register(ApplicationHistory)
class ApplicationHistoryAdmin(admin.ModelAdmin):

    list_display = (
        'application',
        'old_status',
        'new_status',
        'changed_at',
    )

    list_filter = ('new_status', 'changed_at')
    search_fields = ('application__job_title', 'application__company_name')
    ordering = ('-changed_at',) 
from django.db import models
from django.conf import settings
from applications.models import JobApplication
# Create your models here.

class Reminder(models.Model):
    class ReminderType(models.TextChoices):
        FOLLOW_UP = 'follow_up', 'Follow-up'
        INTERVIEW = 'interview', 'Interview'
        ASSESSMENT = 'assessment', 'Assessment'
        DEADLINE = 'deadline', 'Application Deadline'
        OTHER = 'other', 'Other'

    class NotificationChannel(models.TextChoices):
        IN_APP = 'in_app', 'In-app'
        EMAIL = 'email', 'Email'
        BOTH = 'both', 'In-app and Email'

      # User relationship
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reminders'
    )

       # Related job application (optional)
    application = models.ForeignKey(
        JobApplication,
        on_delete=models.CASCADE,
        related_name='reminders',
        null=True,
        blank=True
    )

    # Reminder model strucure
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    reminder_type = models.CharField(
        max_length=20,
        choices=ReminderType.choices,
        default=ReminderType.OTHER
    )
    notification_channel = models.CharField(
        max_length=10,
        choices=NotificationChannel.choices,
        default=NotificationChannel.IN_APP
    )
    is_completed = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['due_date']
        verbose_name = 'Reminder'
        verbose_name_plural = 'Reminders'

    def __str__(self):
        return f"{self.title} - {self.user.username}"

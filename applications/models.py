from django.db import models
from django.conf import settings


class JobApplication(models.Model):

    # Application status choices
    class Status(models.TextChoices):
        SAVED = 'saved', 'Saved'
        APPLIED = 'applied', 'Applied'
        SHORTLISTED = 'shortlisted', 'Shortlisted'
        INTERVIEW = 'interview', 'Interview'
        ASSESSMENT = 'assessment', 'Assessment'
        OFFER = 'offer', 'Offer'
        REJECTED = 'rejected', 'Rejected'
        WITHDRAWN = 'withdrawn', 'Withdrawn'

    # Employment type choices
    class EmploymentType(models.TextChoices):
        FULL_TIME = 'full_time', 'Full-time'
        PART_TIME = 'part_time', 'Part-time'
        CONTRACT = 'contract', 'Contract'
        INTERNSHIP = 'internship', 'Internship'
        TEMPORARY = 'temporary', 'Temporary'

    # User relationship
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='job_applications'
    )

    # Job information
    company_name = models.CharField(max_length=150)
    job_title = models.CharField(max_length=150)
    location = models.CharField(max_length=150, blank=True)
    employment_type = models.CharField(
        max_length=20,
        choices=EmploymentType.choices,
        blank=True
    )
    job_source = models.CharField(max_length=100, blank=True)
    job_url = models.URLField(
        blank=True,
        help_text="Paste the link to the original job advert (optional)."
    )
    job_image = models.ImageField(
        upload_to='job_images/',
        blank=True,
        null=True,
        help_text="upload a screenshot or image of job advert (optional)."

    )
    salary = models.CharField(max_length=100, blank=True)
    date_applied = models.DateField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SAVED
    )
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Job Application'
        verbose_name_plural = 'Job Applications'

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"
    
    # Application History
    
class ApplicationHistory(models.Model):

    application = models.ForeignKey(
        JobApplication,
        on_delete=models.CASCADE,
        related_name='history'
    )

    old_status = models.CharField(
        max_length=20,
        choices=JobApplication.Status.choices,
        blank=True
    )

    new_status = models.CharField(
        max_length=20,
        choices=JobApplication.Status.choices
    )

    changed_at = models.DateTimeField(auto_now_add=True)

    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-changed_at']
        verbose_name = 'Application History'
        verbose_name_plural = 'Application Histories'

    def __str__(self):
        return (
            f"{self.application.job_title}: "
            f"{self.old_status or 'Initial status'} → {self.new_status}"
        )
from django import forms
from .models import JobApplication


class JobApplicationForm(forms.ModelForm):

    class Meta:
        model = JobApplication

        fields = [
            'company_name',
            'job_title',
            'location',
            'employment_type',
            'job_source',
            'job_url',
            'job_image',
            'salary',
            'date_applied',
            'deadline',
            'status',
            'description',
            'notes',
        ]

        widgets = {
            'date_applied': forms.DateInput(attrs={'type': 'date'}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
            })

        # Use Bootstrap's select styling for dropdown fields
        for field_name in ['employment_type', 'job_source', 'status']:
            self.fields[field_name].widget.attrs['class'] = 'form-select'
    def clean_job_image(self):
        image = self.cleaned_data.get('job_image')

        if image:
            # Limit image uploads to 5 MB
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    'Image size cannot exceed 5 MB.'
                )

            # Check whether the file is an image
            if not image.content_type.startswith('image/'):
                raise forms.ValidationError(
                    'Please upload a valid image file.'
                )

        return image

    def clean(self):
        cleaned_data = super().clean()

        date_applied = cleaned_data.get('date_applied')
        deadline = cleaned_data.get('deadline')

        if date_applied and deadline:
            if deadline < date_applied:
                self.add_error(
                    'deadline',
                    'The application deadline cannot be before the date applied.'
                )

        return cleaned_data        
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import JobApplication, ApplicationHistory
from .forms import JobApplicationForm
# Create your views here..

@login_required
def application_list(request):
    applications = JobApplication.objects.filter(
        user=request.user)
    # Search by company, job title or location
    search_query = request.GET.get('q', '').strip()

    if search_query:
        applications = applications.filter(
            Q(company_name__icontains=search_query) |
            Q(job_title__icontains=search_query) |
            Q(location__icontains=search_query)
        )
        # Get the actual choices defined on the model fields
    status_choices = JobApplication._meta.get_field('status').choices

    employment_choices = JobApplication._meta.get_field(
        'employment_type'
    ).choices

    valid_statuses = dict(status_choices)
    valid_employment_types = dict(employment_choices)

    # Filter by status
    status_filter = request.GET.get('status', '')

    if status_filter in valid_statuses:
        applications = applications.filter(status=status_filter)

    # Filter by employment type
    employment_filter = request.GET.get('employment_type', '')

    if employment_filter in valid_employment_types:
        applications = applications.filter(
            employment_type=employment_filter
        )
     # Sort applications newest first
    applications = applications.order_by('-created_at')

    # Pagination: 6 applications per page
    paginator = Paginator(applications, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'applications': page_obj.object_list,
        'search_query': search_query,
        'status_filter': status_filter,
        'employment_filter': employment_filter,
        'status_choices': status_choices,
        'employment_choices': employment_choices,
    }

    return render(
        request, 
        'applications/application_list.html', 
        {'applications': applications})



def application_detail(request, pk):
    application = get_object_or_404(
        JobApplication,
        pk=pk,
        user=request.user)
    history =application.history.all().order_by('changed_at')

    status_labels = dict(
        JobApplication._meta.get_field('status').choices
    )
    return render( request, 'applications/application_detail.html',{
        'application': application,
        'history':history,
        'status_labels' : status_labels
    })
@login_required
def application_create(request):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            
             # Record the initial application status
            ApplicationHistory.objects.create(

                application=application,
                old_status='',
                new_status=application.status,
                notes='Application created.'
            )

            messages.success(request, 'Application added successfully.')
            return redirect('application_detail', pk=application.pk)

    else:
        form = JobApplicationForm()

    return render(request, 'applications/application_form.html', {
        'form': form,
        'page_title': 'Add Job Application'
    })

@login_required
def application_update(request, pk):
    application = get_object_or_404(
        JobApplication,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':
        old_status = application.status

        form = JobApplicationForm(
            request.POST,
            request.FILES,
            instance=application
        )

        if form.is_valid():
            updated_application = form.save()

            # Record history only when the status changes
            if old_status != updated_application.status:
                ApplicationHistory.objects.create(
                    application=application,
                    old_status=old_status,
                    new_status=updated_application.status
                )
            messages.success(request, 'Application updated successfully.')
            return redirect('application_detail', pk=application.pk)

    else:
        form = JobApplicationForm(instance=application)

    return render(request, 'applications/application_form.html', {
        'form': form,
        'application': application,
        'page_title': 'Edit Job Application'
    })


@login_required
def application_delete(request, pk):
    application = get_object_or_404(
        JobApplication,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':
        application.delete()

        messages.success(request, 'Application deleted successfully.')
        return redirect('application_list')

    return render(request, 'applications/application_confirm_delete.html', {
        'application': application
    })


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import DBCData
from projects.models import Project
from .parsers import parse_dbc

@login_required
def dbc_detail(request, username, title):
    if request.user.username != username:
        return HttpResponseForbidden()

    project = get_object_or_404(Project, title=title, owner=request.user)
    dbc_data = getattr(project, 'dbc_data', None)

    return render(request, 'dbc_handler/dbc_detail.html', {
        'project': project,
        'dbc_data': dbc_data,
        'username': username,
        'active_tab': 'dbc'
    })

@login_required
def upload_dbc(request, username, title):
    if request.user.username != username:
        return HttpResponseForbidden()

    project = get_object_or_404(Project, title=title, owner=request.user)

    if request.method == 'POST' and request.FILES.get('dbc_file'):
        dbc_file = request.FILES['dbc_file']
        parsed_data = parse_dbc(dbc_file)

        DBCData.objects.update_or_create(
            project=project,
            defaults={
                'title': dbc_file.name,
                'parsed_data': parsed_data,
                'uploaded_by': request.user
            }
        )

        return redirect('dbc:detail', username=username, title=title)

    return render(request, 'dbc_handler/dbc_upload.html', {
        'project': project,
        'username': username,
        'active_tab': 'dbc'
    })


# Create your views here.

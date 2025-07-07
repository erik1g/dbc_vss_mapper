from .models import VSSData
from .parsers import parse_vss_file
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from projects.models import Project
from django.http import HttpResponseForbidden

@login_required
def vss_upload(request, username, title):
    if request.user.username != username:
        return HttpResponseForbidden("Nicht erlaubt!")

    project = get_object_or_404(Project, title=title, owner=request.user)

    try:
        existing_data = project.vss_data
    except VSSData.DoesNotExist:
        existing_data = None

    if request.method == 'POST' and request.FILES.get('vss_file'):
        vss_file = request.FILES['vss_file']
        
        try:
            parsed_data = parse_vss_file(vss_file)
        except ValueError as e:
            return render(request, 'vss_handler/vss_upload.html', {
                'project': project,
                'username': username,
                'error': str(e),
                'existing_data': existing_data,
            })

        if existing_data:
            existing_data.title = vss_file.name
            existing_data.data = parsed_data.get('full_data', {})
            existing_data.signals = parsed_data.get('signals', [])
            existing_data.uploaded_by = request.user
            existing_data.save()
        else:
            VSSData.objects.create(
                project=project,
                title=vss_file.name,
                data=parsed_data.get('full_data', {}),
                signals=parsed_data.get('signals', []),
                uploaded_by=request.user
            )

        return redirect('vss:detail', username=username, title=title)

    return render(request, 'vss_handler/vss_upload.html', {
        'project': project,
        'username': username,
        'existing_data': existing_data,
    })


@login_required
def vss_detail(request, username, title):
    if request.user.username != username:
        return HttpResponseForbidden("Nicht erlaubt!")
    
    project = get_object_or_404(Project, title=title, owner=request.user)
    try:
        vss_data = project.vss_data
    except VSSData.DoesNotExist:
        vss_data = None
    return render(request, 'vss_handler/vss_detail.html', {
        'project': project,
        'username': username,
        'vss_data': vss_data,
        'active_tab': 'vss'
    })

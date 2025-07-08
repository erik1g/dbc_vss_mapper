from .models import VSSData, VSSSignal
from .parsers import parse_vss_file
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from projects.models import Project
from django.http import HttpResponseForbidden
from django.db import transaction

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

        signals_data = parsed_data.get('signals', [])
        full_data = parsed_data.get('full_data', {})

        with transaction.atomic():
            if existing_data:
                # Update bestehendes VSSData
                existing_data.title = vss_file.name
                existing_data.data = full_data
                existing_data.uploaded_by = request.user
                existing_data.save()

                # Alte Signals löschen
                existing_data.signals.all().delete()

            else:
                # Neues VSSData
                existing_data = VSSData.objects.create(
                    project=project,
                    title=vss_file.name,
                    data=full_data,
                    uploaded_by=request.user
                )

            # Neue Signals anlegen
            signal_objs = []
            for s in signals_data:
                signal_objs.append(VSSSignal(
                    vss_data=existing_data,
                    name=s.get('name', ''),
                    api_name=s.get('apiName', ''),
                    type=s.get('type', ''),
                    datatype=s.get('datatype'),
                    unit=s.get('unit'),
                    description=s.get('description'),
                    api_id=s.get('api_id'),
                    api_uuid=s.get('api_uuid'),
                    parent_api_name=s.get('parent_api_name'),
                    metadata=s.get('metadata')
                ))
            VSSSignal.objects.bulk_create(signal_objs)

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
        vss_signals = vss_data.vss_signals.all()
    except VSSData.DoesNotExist:
        vss_data = None
        vss_signals = []

    return render(request, 'vss_handler/vss_detail.html', {
        'project': project,
        'username': username,
        'vss_data': vss_data,
        'vss_signals': vss_signals,
        'active_tab': 'vss'
    })


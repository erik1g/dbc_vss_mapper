from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from projects.models import Project
from django.http import HttpResponseForbidden
from .models import VssDbcMappingData
import json
from vss_handler.models import VSSData
from dbc_handler.models import DBCData

@login_required
def vss_dbc_mapping_create(request, username, title):  
    if request.user.username != username:
        return HttpResponseForbidden("Nicht erlaubt!")

    project = get_object_or_404(Project, title=title, owner=request.user)

    if request.method == 'POST':
        # Titel aus dem Formular holen
        mapping_title = request.POST.get('title') or None

        # Neues Mapping-Objekt anlegen
        VssDbcMappingData.objects.create(
            project=project,
            title=mapping_title,
            mapping_data={},  # leeres Dict als Start
            created_by=request.user
        )

        return redirect('mapping:detail', username=username, title=title)

    return render(request, 'mapper/mapper_create.html', {
        'project': project,
        'username': username,
    })


@login_required
def vss_dbc_mapping_detail(request, username, title):
    if request.user.username != username:
        return HttpResponseForbidden("Nicht erlaubt!")

    project = get_object_or_404(Project, title=title, owner=request.user)

    # Das neueste Mapping holen (oder None)
    vss_dbc_mapping = project.vss_dbc_mapping.order_by('-created_at').first()
    vss_data = project.vss_data or {}
    dbc_data = project.dbc_data or {}

    return render(request, 'mapper/mapper_detail.html', {
        'project': project,
        'username': username,
        'dbc_data': dbc_data,
        'dbc_data_json': json.dumps(dbc_data.parsed_data or {}),
        'vss_data': vss_data,
        'vss_data_json': json.dumps(vss_data.data or {}),
        'vss_dbc_mapping': vss_dbc_mapping,
        'active_tab': 'mapping'
    })
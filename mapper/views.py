from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from projects.models import Project
from django.http import HttpResponseForbidden
from .models import VssDbcMappingData
import json
from vss_handler.models import VSSData , VSSSignal
from dbc_handler.models import DBCData , DBCMessage ,DBCSignal
from .models import VssDbcMappingEntry, VssDbcMappingTransform
from django.http import JsonResponse

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
    vss_dbc_mapping = project.vss_dbc_mappings.order_by('-created_at').first()

    mapping_entries = (
        vss_dbc_mapping.entries
        .select_related('vss_signal', 'dbc_signal', 'dbc_signal__message')
        if vss_dbc_mapping else []
    )

    return render(request, 'mapper/mapper_detail.html', {
        'project': project,
        'username': username,
        'vss_dbc_mapping': vss_dbc_mapping,
        'mapping_entries': mapping_entries,
        'active_tab': 'mapping'
    })

@login_required
def add_vss_dbc_mapping_entry(request, username, title):
    if request.user.username != username:
        return HttpResponseForbidden("Nicht erlaubt!")

    project = get_object_or_404(Project, title=title, owner=request.user)
    vss_dbc_mapping = VssDbcMappingData.objects.filter(project=project).first()
    vss_data = getattr(project, 'vss_data', None)
    dbc_data = getattr(project, 'dbc_data', None)

    vss_signals = vss_data.vss_signals.all() if vss_data else []
    dbc_signals = DBCSignal.objects.filter(message__dbc_data=dbc_data) if dbc_data else []

    # -> filtere schon verwendete VSS-Signale
    if vss_dbc_mapping:
        used_vss_ids = VssDbcMappingEntry.objects.filter(mapping_data=vss_dbc_mapping).values_list('vss_signal_id', flat=True)
        available_vss_signals = vss_signals.exclude(id__in=used_vss_ids)
    else:
        available_vss_signals = vss_signals

    # -----------------------------------
    # Handle GET → Render Formular
    # -----------------------------------
    if request.method == 'GET':
        vss_signal_id = request.GET.get('vss_signal')
        dbc_signal_id = request.GET.get('dbc_signal')       
        default_dbc2vss = True
        default_vss2dbc = True
        disable_vss2dbc = False
        selected_vss_signal_id =  None
        selected_dbc_signal_id =  None
        mapping_choices = []

        if vss_signal_id:
            try:
                selected_vss_signal = VSSSignal.objects.get(id=vss_signal_id)
                selected_vss_signal_id = selected_vss_signal.id
                if selected_vss_signal.type == 'sensor':
                    default_vss2dbc = False
                    disable_vss2dbc = True
            except VSSSignal.DoesNotExist:
                selected_vss_signal = None
                selected_vss_signal_id = None
        
            if dbc_signal_id:
                try:
                    selected_dbc_signal = dbc_signals.get(id=dbc_signal_id)
                    selected_dbc_signal_id = selected_dbc_signal.id

                    if selected_dbc_signal.choices and isinstance(selected_dbc_signal.choices, list):
                        mapping_choices = [
                            {"from_value": c["label"], "key": c["value"]}
                            for c in selected_dbc_signal.choices
                            if "label" in c and "value" in c
                        ]

                except DBCSignal.DoesNotExist:
                    selected_dbc_signal_id = None

        return render(request, 'mapper/mapper_add_entry.html', {
            'vss_signals': available_vss_signals,
            'dbc_signals': dbc_signals,
            'project': project,
            'username': username,
            'mapping_choices': mapping_choices,
            'selected_vss_signal_id': selected_vss_signal_id,
            'selected_dbc_signal_id': selected_dbc_signal_id,
            'default_dbc2vss': default_dbc2vss,
            'default_vss2dbc': default_vss2dbc,
            'disable_vss2dbc': disable_vss2dbc,
        })

    # -----------------------------------
    # Handle POST → Speichern
    # -----------------------------------
    if request.method == 'POST':
        if not vss_dbc_mapping:
            return render(request, 'mapper/mapper_add_entry.html', {
                'error': "Kein Mapping-Dokument vorhanden. Bitte zuerst eine Mapping-Datei anlegen.",
                'vss_signals': available_vss_signals,
                'dbc_signals': dbc_signals,
                'project': project,
                'username': username
            })

        vss_signal_id = request.POST.get('vss_signal')
        dbc_signal_id = request.POST.get('dbc_signal')

        if not vss_signal_id or not dbc_signal_id:
            return render(request, 'mapper/mapper_add_entry.html', {
                'error': "Bitte beide Signale auswählen.",
                'vss_signals': available_vss_signals,
                'dbc_signals': dbc_signals,
                'project': project,
                'username': username
            })

        try:
            vss_signal = VSSSignal.objects.get(id=vss_signal_id)
            dbc_signal = DBCSignal.objects.get(id=dbc_signal_id)
        except (VSSSignal.DoesNotExist, DBCSignal.DoesNotExist):
            return render(request, 'mapper/mapper_add_entry.html', {
                'error': "Ungültige Signal-IDs.",
                'vss_signals': available_vss_signals,
                'dbc_signals': dbc_signals,
                'project': project,
                'username': username
            })

        # Prüfen ob VSS-Signal schon verwendet
        if VssDbcMappingEntry.objects.filter(mapping_data=vss_dbc_mapping, vss_signal=vss_signal).exists():
            return render(request, 'mapper/mapper_add_entry.html', {
                'error': "Dieses VSS-Signal ist bereits gemappt.",
                'vss_signals': available_vss_signals,
                'dbc_signals': dbc_signals,
                'project': project,
                'username': username
            })

        # Entry speichern
        entry = VssDbcMappingEntry.objects.create(
            mapping_data=vss_dbc_mapping,
            vss_signal=vss_signal,
            dbc_signal=dbc_signal
        )


        VssDbcMappingTransform.objects.create(
            mapping_entry=entry,
            direction='dbc2vss',
            interval_ms=request.POST.get('dbc2vss_interval') or None,
            math=request.POST.get('dbc2vss_math') or None,
            mapping=request.POST.get('dbc2vss_mapping') or None,
        )

        VssDbcMappingTransform.objects.create(
            mapping_entry=entry,
            direction='vss2dbc',
            interval_ms=request.POST.get('vss2dbc_interval') or None,
            math=request.POST.get('vss2dbc_math') or None,
            mapping=request.POST.get('vss2dbc_mapping') or None,
        )

    return redirect('mapping:detail', username=username, title=title)
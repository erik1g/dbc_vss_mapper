from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import DBCData, DBCMessage, DBCSignal
from projects.models import Project
from .parsers import parse_dbc
from django.db import transaction

@login_required
def dbc_detail(request, username, title):
    if request.user.username != username:
        return HttpResponseForbidden()

    project = get_object_or_404(Project, title=title, owner=request.user)
    dbc_data = getattr(project, 'dbc_data', None)

    messages = dbc_data.messages.all() if dbc_data else []

    return render(request, 'dbc_handler/dbc_detail.html', {
        'project': project,
        'dbc_data': dbc_data,
        'messages': messages,
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

        messages_data = parsed_data.get('messages', [])
        full_data = parsed_data

        with transaction.atomic():
            dbc_data, created = DBCData.objects.get_or_create(
                project=project,
                defaults={
                    'title': dbc_file.name,
                    'parsed_data': full_data,
                    'uploaded_by': request.user
                }
            )

            if not created:
                dbc_data.title = dbc_file.name
                dbc_data.parsed_data = full_data
                dbc_data.uploaded_by = request.user
                dbc_data.save()

                # ALLES löschen
                dbc_data.messages.all().delete()

            # JETZT Messages und ihre Signals sauber neu anlegen
            for msg in messages_data:
                message_obj = DBCMessage.objects.create(
                    dbc_data=dbc_data,
                    name=msg.get('message_name'),
                    frame_id=msg.get('frame_id'),
                    length=msg.get('length'),
                    senders=msg.get('senders'),
                    comment=msg.get('comment')
                )

                signal_objs = []
                for s in msg.get('signals', []):
                    signal_objs.append(DBCSignal(
                        message=message_obj,
                        name=s.get('signal_name', ''),
                        unit=s.get('unit', ''),
                        start_bit=s.get('start_bit'),
                        length=s.get('length'),
                        byte_order=s.get('byte_order'),
                        is_signed=s.get('is_signed', False),
                        scale=s.get('scale'),
                        offset=s.get('offset'),
                        minimum=s.get('min'),
                        maximum=s.get('max'),
                        choices=s.get('choices'),
                        metadata=s.get('metadata')
                    ))
                DBCSignal.objects.bulk_create(signal_objs)

        return redirect('dbc:detail', username=username, title=title)

    return render(request, 'dbc_handler/dbc_upload.html', {
        'project': project,
        'username': username,
        'active_tab': 'dbc'
    })


# Create your views here.

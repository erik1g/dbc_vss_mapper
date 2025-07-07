from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm
from django.http import HttpResponseForbidden

@login_required
def project_list(request, username):
    if request.user.username != username:
        return HttpResponseForbidden("Nicht erlaubt!")

    projects = request.user.projects.all()
    return render(request, 'projects/project_list.html', {
        'projects': projects,
        'username': username,
    })


@login_required
def create_project(request , username):
    if request.user.username != username:
        return HttpResponseForbidden("Nicht erlaubt!")
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('project_list', username=username)
    else:
        form = ProjectForm()
    return render(request, 'projects/project_create.html', {
        'form': form,
        'username': username
    })

@login_required
def project_detail(request, username, title):
    if request.user.username != username:
        return HttpResponseForbidden("Nicht erlaubt!")
    
    project = get_object_or_404(Project, title = title, owner=request.user)
    return render(request, 'projects/project_detail.html', {
        'project': project,
        'username': username,
        'active_tab': 'info'
    })


# Create your views here.

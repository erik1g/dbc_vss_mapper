from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('create/', views.create_project, name='create_project'),
    path('<str:title>/', views.project_detail, name='project_detail'),

    # VSS-Handler wird eingebunden
    path('<str:title>/vss/', include(('vss_handler.urls', 'vss_handler'), namespace='vss')),

    # DBC-Handler wird eingebunden
    path('<str:title>/dbc/', include(('dbc_handler.urls', 'dbc_handler'), namespace='dbc')),

        # DBC-Handler wird eingebunden
    path('<str:title>/mapping/', include(('mapper.urls', 'mapper'), namespace='mapping')),
]


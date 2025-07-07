from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', login_required(views.logout_view), name='logout'),
]

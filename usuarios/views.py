from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'

@login_required
def bienvenida(request):
    return redirect('dashboard:dashboard_home')

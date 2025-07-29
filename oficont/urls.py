from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from usuarios.views import CustomLoginView
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

def home_redirect(request):
    """Redirige siempre al login primero"""
    return redirect('login')

def dashboard_redirect(request):
    """Redirige al dashboard solo si está autenticado"""
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard_home')
    else:
        return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_redirect, name='home'),  # Redirige según autenticación
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dashboard/', include('dashboard.urls')),  # Dashboard del sistema contable
    path('logout/', LogoutView.as_view(next_page='login', http_method_names=['get', 'post']), name='logout'),

    # Rutas de restablecimiento de contraseña
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

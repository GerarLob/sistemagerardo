from django.contrib import admin
from django.urls import path
from usuarios.views import CustomLoginView, bienvenida
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', CustomLoginView.as_view(), name='login'),  # CAMBIADO: ahora la raíz va al login
    path('bienvenida/', bienvenida, name='bienvenida'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Rutas de restablecimiento de contraseña
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

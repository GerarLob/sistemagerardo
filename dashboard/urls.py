from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Dashboard principal
    path('', views.dashboard_home, name='dashboard_home'),
    
    # Gestión de clientes
    path('clientes/', views.clientes_lista, name='clientes_lista'),
    path('clientes/nuevo/', views.cliente_crear, name='cliente_crear'),
    path('clientes/<int:cliente_id>/', views.cliente_detalle, name='cliente_detalle'),
    path('clientes/<int:cliente_id>/editar/', views.cliente_editar, name='cliente_editar'),
    
    # Gestión de transacciones
    path('transacciones/', views.transacciones_lista, name='transacciones_lista'),
    path('transacciones/nueva/', views.transaccion_crear, name='transaccion_crear'),
    path('transacciones/<int:transaccion_id>/editar/', views.transaccion_editar, name='transaccion_editar'),
    
    # Reportes
    path('reportes/', views.reportes_lista, name='reportes_lista'),
    path('reportes/generar/', views.reporte_generar, name='reporte_generar'),
    
    # Configuración del sistema
    path('configuracion/', views.configuracion_sistema, name='configuracion_sistema'),
] 
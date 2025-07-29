from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from .models import Cliente, Transaccion, CategoriaContable, ReporteContable, ConfiguracionSistema
from .forms import ClienteForm, TransaccionForm, CategoriaContableForm

@login_required
def dashboard_home(request):
    """Vista principal del dashboard"""
    # Obtener estadísticas generales
    total_clientes = Cliente.objects.filter(activo=True).count()
    total_transacciones = Transaccion.objects.count()
    
    # Transacciones del mes actual
    mes_actual = timezone.now().month
    ano_actual = timezone.now().year
    transacciones_mes = Transaccion.objects.filter(
        fecha_transaccion__month=mes_actual,
        fecha_transaccion__year=ano_actual
    )
    
    ingresos_mes = transacciones_mes.filter(tipo_transaccion='ingreso').aggregate(
        total=Sum('monto'))['total'] or Decimal('0.00')
    gastos_mes = transacciones_mes.filter(tipo_transaccion='gasto').aggregate(
        total=Sum('monto'))['total'] or Decimal('0.00')
    
    # Transacciones recientes
    transacciones_recientes = Transaccion.objects.select_related('cliente', 'categoria').order_by('-fecha_registro')[:5]
    
    # Clientes recientes
    clientes_recientes = Cliente.objects.filter(activo=True).order_by('-fecha_registro')[:5]
    
    # Gráfico de transacciones por categoría (últimos 30 días)
    fecha_limite = timezone.now().date() - timedelta(days=30)
    transacciones_30_dias = Transaccion.objects.filter(fecha_transaccion__gte=fecha_limite)
    
    context = {
        'total_clientes': total_clientes,
        'total_transacciones': total_transacciones,
        'ingresos_mes': ingresos_mes,
        'gastos_mes': gastos_mes,
        'balance_mes': ingresos_mes - gastos_mes,
        'transacciones_recientes': transacciones_recientes,
        'clientes_recientes': clientes_recientes,
        'mes_actual': mes_actual,
        'ano_actual': ano_actual,
    }
    
    return render(request, 'dashboard/dashboard_home.html', context)

@login_required
def clientes_lista(request):
    """Lista de clientes"""
    clientes = Cliente.objects.all().order_by('nombre')
    return render(request, 'dashboard/clientes_lista.html', {'clientes': clientes})

@login_required
def cliente_detalle(request, cliente_id):
    """Detalle de un cliente específico"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    transacciones = Transaccion.objects.filter(cliente=cliente).order_by('-fecha_transaccion')
    
    # Estadísticas del cliente
    total_ingresos = transacciones.filter(tipo_transaccion='ingreso').aggregate(
        total=Sum('monto'))['total'] or Decimal('0.00')
    total_gastos = transacciones.filter(tipo_transaccion='gasto').aggregate(
        total=Sum('monto'))['total'] or Decimal('0.00')
    
    context = {
        'cliente': cliente,
        'transacciones': transacciones,
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos,
        'balance': total_ingresos - total_gastos,
    }
    
    return render(request, 'dashboard/cliente_detalle.html', context)

@login_required
def cliente_crear(request):
    """Crear nuevo cliente"""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado exitosamente.')
            return redirect('dashboard:clientes_lista')
    else:
        form = ClienteForm()
    
    return render(request, 'dashboard/cliente_form.html', {'form': form, 'titulo': 'Nuevo Cliente'})

@login_required
def cliente_editar(request, cliente_id):
    """Editar cliente existente"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado exitosamente.')
            return redirect('dashboard:cliente_detalle', cliente_id=cliente.id)
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'dashboard/cliente_form.html', {
        'form': form, 
        'titulo': f'Editar Cliente: {cliente.nombre}'
    })

@login_required
def transacciones_lista(request):
    """Lista de transacciones"""
    transacciones = Transaccion.objects.select_related('cliente', 'categoria').order_by('-fecha_transaccion')
    
    # Filtros
    cliente_id = request.GET.get('cliente')
    tipo_transaccion = request.GET.get('tipo')
    estado = request.GET.get('estado')
    
    if cliente_id:
        transacciones = transacciones.filter(cliente_id=cliente_id)
    if tipo_transaccion:
        transacciones = transacciones.filter(tipo_transaccion=tipo_transaccion)
    if estado:
        transacciones = transacciones.filter(estado=estado)
    
    clientes = Cliente.objects.filter(activo=True)
    
    context = {
        'transacciones': transacciones,
        'clientes': clientes,
        'filtros': {
            'cliente_id': cliente_id,
            'tipo_transaccion': tipo_transaccion,
            'estado': estado,
        }
    }
    
    return render(request, 'dashboard/transacciones_lista.html', context)

@login_required
def transaccion_crear(request):
    """Crear nueva transacción"""
    if request.method == 'POST':
        form = TransaccionForm(request.POST, request.FILES)
        if form.is_valid():
            transaccion = form.save(commit=False)
            transaccion.registrado_por = request.user
            transaccion.save()
            messages.success(request, 'Transacción registrada exitosamente.')
            return redirect('dashboard:transacciones_lista')
    else:
        form = TransaccionForm()
    
    return render(request, 'dashboard/transaccion_form.html', {
        'form': form, 
        'titulo': 'Nueva Transacción'
    })

@login_required
def transaccion_editar(request, transaccion_id):
    """Editar transacción existente"""
    transaccion = get_object_or_404(Transaccion, id=transaccion_id)
    if request.method == 'POST':
        form = TransaccionForm(request.POST, request.FILES, instance=transaccion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transacción actualizada exitosamente.')
            return redirect('dashboard:transacciones_lista')
    else:
        form = TransaccionForm(instance=transaccion)
    
    return render(request, 'dashboard/transaccion_form.html', {
        'form': form, 
        'titulo': f'Editar Transacción: {transaccion.cliente.nombre}'
    })

@login_required
def reportes_lista(request):
    """Lista de reportes generados"""
    reportes = ReporteContable.objects.select_related('cliente').order_by('-fecha_generado')
    return render(request, 'dashboard/reportes_lista.html', {'reportes': reportes})

@login_required
def reporte_generar(request):
    """Generar nuevo reporte"""
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        tipo_reporte = request.POST.get('tipo_reporte')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        
        if cliente_id and tipo_reporte and fecha_inicio and fecha_fin:
            cliente = get_object_or_404(Cliente, id=cliente_id)
            reporte = ReporteContable.objects.create(
                cliente=cliente,
                tipo_reporte=tipo_reporte,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                generado_por=request.user
            )
            messages.success(request, 'Reporte generado exitosamente.')
            return redirect('dashboard:reportes_lista')
        else:
            messages.error(request, 'Por favor complete todos los campos.')
    
    clientes = Cliente.objects.filter(activo=True)
    return render(request, 'dashboard/reporte_generar.html', {'clientes': clientes})

@login_required
def configuracion_sistema(request):
    """Configuración del sistema"""
    config, created = ConfiguracionSistema.objects.get_or_create(id=1)
    
    if request.method == 'POST':
        config.nombre_oficina = request.POST.get('nombre_oficina', config.nombre_oficina)
        config.direccion_oficina = request.POST.get('direccion_oficina', config.direccion_oficina)
        config.telefono_oficina = request.POST.get('telefono_oficina', config.telefono_oficina)
        config.email_oficina = request.POST.get('email_oficina', config.email_oficina)
        config.save()
        messages.success(request, 'Configuración actualizada exitosamente.')
        return redirect('dashboard:configuracion_sistema')
    
    return render(request, 'dashboard/configuracion_sistema.html', {'config': config})

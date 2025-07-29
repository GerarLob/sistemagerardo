from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal

class Cliente(models.Model):
    """Modelo para gestionar clientes de la oficina contable"""
    TIPO_CLIENTE_CHOICES = [
        ('individual', 'Persona Individual'),
        ('empresa', 'Empresa'),
        ('organizacion', 'Organización'),
    ]
    
    nombre = models.CharField(max_length=200, verbose_name="Nombre/Razón Social")
    tipo_cliente = models.CharField(max_length=20, choices=TIPO_CLIENTE_CHOICES, default='individual')
    nit = models.CharField(max_length=20, unique=True, verbose_name="NIT")
    direccion = models.TextField(verbose_name="Dirección")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    email = models.EmailField(verbose_name="Correo Electrónico")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True, verbose_name="Cliente Activo")
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.nit}"

class CategoriaContable(models.Model):
    """Categorías contables para organizar transacciones"""
    nombre = models.CharField(max_length=100, verbose_name="Nombre de Categoría")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    tipo = models.CharField(max_length=20, choices=[
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
        ('activo', 'Activo'),
        ('pasivo', 'Pasivo'),
    ], verbose_name="Tipo de Categoría")
    
    class Meta:
        verbose_name = "Categoría Contable"
        verbose_name_plural = "Categorías Contables"
    
    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

class Transaccion(models.Model):
    """Modelo para registrar transacciones contables"""
    TIPO_TRANSACCION_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
        ('transferencia', 'Transferencia'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
        ('completado', 'Completado'),
    ]
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    categoria = models.ForeignKey(CategoriaContable, on_delete=models.CASCADE, verbose_name="Categoría")
    tipo_transaccion = models.CharField(max_length=20, choices=TIPO_TRANSACCION_CHOICES, verbose_name="Tipo de Transacción")
    monto = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Monto (Q)")
    descripcion = models.TextField(verbose_name="Descripción")
    fecha_transaccion = models.DateField(verbose_name="Fecha de Transacción")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    comprobante = models.FileField(upload_to='comprobantes/', blank=True, null=True, verbose_name="Comprobante")
    registrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Registrado por")
    
    class Meta:
        verbose_name = "Transacción"
        verbose_name_plural = "Transacciones"
        ordering = ['-fecha_transaccion']
    
    def __str__(self):
        return f"{self.cliente.nombre} - {self.monto}Q - {self.fecha_transaccion}"

class ReporteContable(models.Model):
    """Modelo para generar reportes contables"""
    TIPO_REPORTE_CHOICES = [
        ('balance_general', 'Balance General'),
        ('estado_resultados', 'Estado de Resultados'),
        ('flujo_efectivo', 'Flujo de Efectivo'),
        ('libro_diario', 'Libro Diario'),
        ('libro_mayor', 'Libro Mayor'),
    ]
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    tipo_reporte = models.CharField(max_length=30, choices=TIPO_REPORTE_CHOICES, verbose_name="Tipo de Reporte")
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de Fin")
    fecha_generado = models.DateTimeField(auto_now_add=True)
    generado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Generado por")
    archivo_pdf = models.FileField(upload_to='reportes/', blank=True, null=True, verbose_name="Archivo PDF")
    
    class Meta:
        verbose_name = "Reporte Contable"
        verbose_name_plural = "Reportes Contables"
        ordering = ['-fecha_generado']
    
    def __str__(self):
        return f"{self.cliente.nombre} - {self.get_tipo_reporte_display()} - {self.fecha_generado.strftime('%d/%m/%Y')}"

class ConfiguracionSistema(models.Model):
    """Configuraciones generales del sistema contable"""
    nombre_oficina = models.CharField(max_length=200, default="OFICONT - Oficina Contable", verbose_name="Nombre de la Oficina")
    direccion_oficina = models.TextField(default="Guatemala", verbose_name="Dirección de la Oficina")
    telefono_oficina = models.CharField(max_length=20, default="", verbose_name="Teléfono de la Oficina")
    email_oficina = models.EmailField(default="", verbose_name="Email de la Oficina")
    moneda = models.CharField(max_length=10, default="Q", verbose_name="Moneda")
    formato_fecha = models.CharField(max_length=20, default="DD/MM/YYYY", verbose_name="Formato de Fecha")
    
    class Meta:
        verbose_name = "Configuración del Sistema"
        verbose_name_plural = "Configuraciones del Sistema"
    
    def __str__(self):
        return f"Configuración - {self.nombre_oficina}"

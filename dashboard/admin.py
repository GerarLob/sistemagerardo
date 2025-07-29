from django.contrib import admin
from .models import Cliente, CategoriaContable, Transaccion, ReporteContable, ConfiguracionSistema

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo_cliente', 'nit', 'telefono', 'email', 'activo', 'fecha_registro']
    list_filter = ['tipo_cliente', 'activo', 'fecha_registro']
    search_fields = ['nombre', 'nit', 'email']
    list_editable = ['activo']
    date_hierarchy = 'fecha_registro'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'tipo_cliente', 'nit')
        }),
        ('Información de Contacto', {
            'fields': ('direccion', 'telefono', 'email')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )

@admin.register(CategoriaContable)
class CategoriaContableAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'descripcion']
    list_filter = ['tipo']
    search_fields = ['nombre', 'descripcion']

@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'tipo_transaccion', 'monto', 'categoria', 'fecha_transaccion', 'estado', 'registrado_por']
    list_filter = ['tipo_transaccion', 'estado', 'fecha_transaccion', 'categoria']
    search_fields = ['cliente__nombre', 'descripcion']
    date_hierarchy = 'fecha_transaccion'
    readonly_fields = ['fecha_registro', 'registrado_por']
    
    fieldsets = (
        ('Información de la Transacción', {
            'fields': ('cliente', 'categoria', 'tipo_transaccion', 'monto', 'descripcion')
        }),
        ('Fechas', {
            'fields': ('fecha_transaccion', 'fecha_registro')
        }),
        ('Estado y Archivos', {
            'fields': ('estado', 'comprobante')
        }),
        ('Registro', {
            'fields': ('registrado_por',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es una nueva transacción
            obj.registrado_por = request.user
        super().save_model(request, obj, form, change)

@admin.register(ReporteContable)
class ReporteContableAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'tipo_reporte', 'fecha_inicio', 'fecha_fin', 'fecha_generado', 'generado_por']
    list_filter = ['tipo_reporte', 'fecha_generado']
    search_fields = ['cliente__nombre']
    date_hierarchy = 'fecha_generado'
    readonly_fields = ['fecha_generado', 'generado_por']
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo reporte
            obj.generado_por = request.user
        super().save_model(request, obj, form, change)

@admin.register(ConfiguracionSistema)
class ConfiguracionSistemaAdmin(admin.ModelAdmin):
    list_display = ['nombre_oficina', 'telefono_oficina', 'email_oficina', 'moneda']
    
    def has_add_permission(self, request):
        # Solo permitir una configuración
        return not ConfiguracionSistema.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # No permitir eliminar la configuración
        return False

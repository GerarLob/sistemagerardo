from django import forms
from .models import Cliente, Transaccion, CategoriaContable

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'tipo_cliente', 'nit', 'direccion', 'telefono', 'email', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre o Razón Social'}),
            'tipo_cliente': forms.Select(attrs={'class': 'form-select'}),
            'nit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'NIT'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Dirección completa'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre': 'Nombre/Razón Social',
            'tipo_cliente': 'Tipo de Cliente',
            'nit': 'NIT',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'email': 'Correo Electrónico',
            'activo': 'Cliente Activo',
        }

class CategoriaContableForm(forms.ModelForm):
    class Meta:
        model = CategoriaContable
        fields = ['nombre', 'descripcion', 'tipo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción de la categoría'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'nombre': 'Nombre de Categoría',
            'descripcion': 'Descripción',
            'tipo': 'Tipo de Categoría',
        }

class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['cliente', 'categoria', 'tipo_transaccion', 'monto', 'descripcion', 'fecha_transaccion', 'estado', 'comprobante']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'tipo_transaccion': forms.Select(attrs={'class': 'form-select'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'placeholder': '0.00'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción de la transacción'}),
            'fecha_transaccion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'comprobante': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'cliente': 'Cliente',
            'categoria': 'Categoría Contable',
            'tipo_transaccion': 'Tipo de Transacción',
            'monto': 'Monto (Q)',
            'descripcion': 'Descripción',
            'fecha_transaccion': 'Fecha de Transacción',
            'estado': 'Estado',
            'comprobante': 'Comprobante',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo clientes activos
        self.fields['cliente'].queryset = Cliente.objects.filter(activo=True)
        
        # Filtrar categorías por tipo de transacción si se especifica
        if 'tipo_transaccion' in self.data:
            tipo_transaccion = self.data.get('tipo_transaccion')
            if tipo_transaccion in ['ingreso', 'gasto']:
                self.fields['categoria'].queryset = CategoriaContable.objects.filter(tipo=tipo_transaccion)
        elif self.instance.pk and self.instance.tipo_transaccion:
            self.fields['categoria'].queryset = CategoriaContable.objects.filter(tipo=self.instance.tipo_transaccion)

class ReporteForm(forms.Form):
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.filter(activo=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Cliente'
    )
    tipo_reporte = forms.ChoiceField(
        choices=[
            ('balance_general', 'Balance General'),
            ('estado_resultados', 'Estado de Resultados'),
            ('flujo_efectivo', 'Flujo de Efectivo'),
            ('libro_diario', 'Libro Diario'),
            ('libro_mayor', 'Libro Mayor'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Tipo de Reporte'
    )
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Fecha de Inicio'
    )
    fecha_fin = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Fecha de Fin'
    )

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            raise forms.ValidationError("La fecha de inicio no puede ser posterior a la fecha de fin.")
        
        return cleaned_data 
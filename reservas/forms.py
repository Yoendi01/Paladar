from django import forms
from django.utils import timezone
from .models import Reserva


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = [
            'nombre', 'email', 'telefono', 'fecha', 'hora',
            'personas', 'comentarios', 'metodo_contacto'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Tu nombre completo'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'tucorreo@ejemplo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+53 5555 5555'
            }),
            'fecha': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'hora': forms.Select(attrs={'class': 'form-input'}),
            'personas': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': 1,
                'max': 30,
                'placeholder': '2'
            }),
            'comentarios': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                'placeholder': 'Alergias, ocasión especial, preferencias...'
            }),
            'metodo_contacto': forms.RadioSelect(attrs={'class': 'radio-group'}),
        }
        labels = {
            'metodo_contacto': '¿Cómo quieres que te confirmemos?',
            'comentarios': 'Comentarios (opcional)',
        }

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha < timezone.now().date():
            raise forms.ValidationError('No puedes reservar para una fecha pasada.')
        return fecha

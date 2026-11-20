from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date


class Reserva(models.Model):
    HORARIOS = [
        ('12:00', '12:00 PM'),
        ('12:30', '12:30 PM'),
        ('13:00', '1:00 PM'),
        ('13:30', '1:30 PM'),
        ('14:00', '2:00 PM'),
        ('18:00', '6:00 PM'),
        ('18:30', '6:30 PM'),
        ('19:00', '7:00 PM'),
        ('19:30', '7:30 PM'),
        ('20:00', '8:00 PM'),
        ('20:30', '8:30 PM'),
        ('21:00', '9:00 PM'),
    ]

    OPCIONES_CONTACTO = [
        ('whatsapp', 'WhatsApp'),
        ('email', 'Correo Electrónico'),
    ]

    nombre = models.CharField(max_length=120)
    email = models.EmailField()
    telefono = models.CharField(max_length=30)
    fecha = models.DateField()
    hora = models.CharField(max_length=5, choices=HORARIOS)
    personas = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(30)]
    )
    comentarios = models.TextField(blank=True)
    metodo_contacto = models.CharField(
        max_length=10, choices=OPCIONES_CONTACTO, default='whatsapp'
    )
    creada_en = models.DateTimeField(auto_now_add=True)
    confirmada = models.BooleanField(default=False)

    class Meta:
        ordering = ['-creada_en']
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f"{self.nombre} - {self.fecha} {self.hora} ({self.personas}p)"

from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Reserva


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'hora', 'personas', 'metodo_contacto', 'confirmada')
    list_filter = ('fecha', 'metodo_contacto', 'confirmada')
    search_fields = ('nombre', 'email', 'telefono')
    list_editable = ('confirmada',)
    date_hierarchy = 'fecha'

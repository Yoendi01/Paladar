from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from urllib.parse import quote
from .forms import ReservaForm
from .models import Reserva


def landing(request):
    """Landing page principal del paladar."""
    return render(request, 'reservas/landing.html')


def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save()

            # ========== ENVÍO POR EMAIL ==========
            if reserva.metodo_contacto == 'email':
                _enviar_email_reserva(request, reserva)

            # ========== WHATSAPP ==========
            if reserva.metodo_contacto == 'whatsapp':
                request.session['wa_link'] = _generar_link_whatsapp(reserva)
                request.session['wa_nombre'] = reserva.nombre

            request.session['reserva_id'] = reserva.id
            return redirect('reserva_exitosa')
    else:
        form = ReservaForm()

    return render(request, 'reservas/reserva_form.html', {
        'form': form,
        'paladar_nombre': settings.PALADAR_NOMBRE,
    })


def reserva_exitosa(request):
    reserva_id = request.session.get('reserva_id')
    if not reserva_id:
        return redirect('landing')

    reserva = get_object_or_404(Reserva, pk=reserva_id)
    wa_link = request.session.get('wa_link')

    return render(request, 'reservas/reserva_exitosa.html', {
        'reserva': reserva,
        'wa_link': wa_link,
        'paladar_nombre': settings.PALADAR_NOMBRE,
        'paladar_whatsapp': settings.PALADAR_WHATSAPP,
        'paladar_email': settings.PALADAR_EMAIL,
    })


def mis_reservas(request):
    """Consulta de reservas por email o teléfono."""
    reservas = []
    busqueda = ''
    if request.method == 'POST':
        busqueda = request.POST.get('busqueda', '').strip()
        if busqueda:
            reservas = Reserva.objects.filter(
                email__iexact=busqueda
            ) | Reserva.objects.filter(
                telefono__icontains=busqueda
            )
            reservas = reservas.order_by('-creada_en')

    return render(request, 'reservas/mis_reservas.html', {
        'reservas': reservas,
        'busqueda': busqueda,
        'paladar_nombre': settings.PALADAR_NOMBRE,
    })


# ==================== HELPERS ====================

def _generar_link_whatsapp(reserva):
    """Genera el link de WhatsApp con el mensaje pre-llenado."""
    texto = (
        f"¡Hola {settings.PALADAR_NOMBRE}! 👋\n\n"
        f"Quiero confirmar mi reserva:\n\n"
        f"👤 Nombre: {reserva.nombre}\n"
        f"📅 Fecha: {reserva.fecha.strftime('%d/%m/%Y')}\n"
        f"🕐 Hora: {reserva.hora}\n"
        f"👥 Personas: {reserva.personas}\n"
        f"📧 Email: {reserva.email}\n"
        f"📞 Teléfono: {reserva.telefono}\n"
    )
    if reserva.comentarios:
        texto += f"📝 Comentarios: {reserva.comentarios}\n"
    texto += "\n¡Gracias! 🙏"

    return f"https://wa.me/{settings.PALADAR_WHATSAPP}?text={quote(texto)}"


def _enviar_email_reserva(request, reserva):
    """Envía el correo al paladar y al cliente."""
    asunto_paladar = f"🍽️ Nueva Reserva - {reserva.nombre}"
    mensaje_paladar = (
        f"Nueva reserva recibida:\n\n"
        f"Nombre: {reserva.nombre}\n"
        f"Email: {reserva.email}\n"
        f"Teléfono: {reserva.telefono}\n"
        f"Fecha: {reserva.fecha.strftime('%d/%m/%Y')}\n"
        f"Hora: {reserva.hora}\n"
        f"Personas: {reserva.personas}\n"
        f"Comentarios: {reserva.comentarios or 'Ninguno'}\n"
    )

    send_mail(
        asunto_paladar,
        mensaje_paladar,
        settings.PALADAR_EMAIL,
        [settings.PALADAR_EMAIL],
        fail_silently=True,
    )

    asunto_cliente = f"✅ Reserva recibida en {settings.PALADAR_NOMBRE}"
    mensaje_cliente = (
        f"Hola {reserva.nombre},\n\n"
        f"Hemos recibido tu solicitud de reserva. ¡Te esperamos!\n\n"
        f"📅 Fecha: {reserva.fecha.strftime('%d/%m/%Y')}\n"
        f"🕐 Hora: {reserva.hora}\n"
        f"👥 Personas: {reserva.personas}\n\n"
        f"Te confirmaremos a la brevedad.\n\n"
        f"{settings.PALADAR_NOMBRE}\n"
        f"{settings.PALADAR_DIRECCION}\n"
        f"Tel: {settings.PALADAR_TELEFONO}"
    )

    send_mail(
        asunto_cliente,
        mensaje_cliente,
        settings.PALADAR_EMAIL,
        [reserva.email],
        fail_silently=True,
    )

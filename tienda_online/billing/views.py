from django.shortcuts import render
from .utils import PDFBillGenerator, HTMLBillGenerator
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.http import FileResponse, HttpResponse
from .models import Bill
from django.contrib import messages
from django.conf import settings
import os


def view_bill(request):
    bill_data = {'amount': 150}

    generator = PDFBillGenerator() if request.GET.get(
        'format') == 'pdf' else HTMLBillGenerator()

    return generator.generate_bill(bill_data)


def download_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    file_path = bill.pdf_file.path
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=f'bill_{bill_id}.pdf')
    else:
        return HttpResponse("Error: No se encontró el archivo", status=404)


def send_bill_email(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    email = EmailMessage(
        subject='Factura de Compra TechVanguard',
        body='Gracias por su compra. Encuentra adjunta la factura de tu compra reciente.',
        from_email=settings.EMAIL_HOST_USER,
        to=[bill.customer_email],
    )
    if os.path.exists(bill.pdf_file.path):
        email.attach_file(bill.pdf_file.path)
        email.send()
        messages.success(
            request, 'Hemos enviado un correo electronico con su factura')
        return HttpResponse("Correo enviado correctamente")
    else:
        return HttpResponse("Error al enviar el correo", status=500)

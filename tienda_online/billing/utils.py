from django.conf import settings
from .interfaces import BillGenerator
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.core.files.base import ContentFile
from .models import Bill
import os
import io


class PDFBillGenerator(BillGenerator):
    def generate_bill(self, data):
        filename = f'bill_{data["customer_email"]}.pdf'
        file_path = os.path.join(settings.MEDIA_ROOT, 'bills', filename)

        # response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = f'attachment; filename="bill.pdf"'

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        p.setFont("Helvetica-Bold", 16)
        p.drawString(72, height - 72, "Factura de Compra - TechVanguard")
        p.setFont("Helvetica", 12)
        p.drawString(72, height - 104, f"Cliente: {data['customer_name']}")
        p.drawString(72, height - 124,
                     f"Correo Electrónico: {data['customer_email']}")

        y_position = height - 144
        p.drawString(72, y_position, "Productos Comprados:")
        p.setFont("Helvetica", 10)
        total = 0

        for item in data['items']:
            y_position -= 20
            product_details = f"{item['id']} - {item['name']} - Precio: ${item['price']}"
            p.drawString(100, y_position, product_details)
            total += item['price']

        y_position -= 40
        p.setFont("Helvetica-Bold", 12)
        p.drawString(72, y_position, f"Total Pagado: ${data['total_amount']}")

        p.showPage()
        p.save()
        # return response

        buffer.seek(0)
        file_content = ContentFile(buffer.read())
        buffer.close()
        # Guardar el pdf en el model
        bill = Bill(
            customer_name=data['customer_name'],
            customer_email=data['customer_email'],
        )

        # Guardar el archivo PDF en el campo del archivo
        bill.pdf_file.save(filename, file_content)
        bill.save()

        return bill.pdf_file.url, bill.id

    def download_bill(self, bill_id):
        return self.generate_bill({'amount': 100})


class HTMLBillGenerator(BillGenerator):
    def generate_bill(self, data):
        return f"<html><body><h1>bill for ${data['amount']}</h1></body></html>"

    def download_bill(self, bill_id):
        return self.generate_bill({'amount': 100})

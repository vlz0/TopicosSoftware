from .interfaces import BillGenerator
from reportlab.pdfgen import canvas
from django.http import HttpResponse
import os

class PDFBillGenerator(BillGenerator):
    def generate_bill(self, data):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="bill_{data.id}.pdf"'

        p = canvas.Canvas(response)
        p.drawString(100, 800, "Factura de tu reciente compra")
        p.drawString(100, 735, f"ID de compra: {data.id}")
        p.drawString(100, 780, f"Total: ${data['price']}")
        p.showPage()
        p.save()
        return response

    def download_bill(self, bill_id):
        return self.generate_bill({'price': 100})

class HTMLBillGenerator(BillGenerator):
    def generate_bill(self, data):
        return f"<html><body><h1>bill for ${data['price']}</h1></body></html>"

    def download_bill(self, bill_id):
        return self.generate_bill({'price': 100})

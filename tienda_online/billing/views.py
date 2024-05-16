from django.shortcuts import render
from .utils import PDFBillGenerator, HTMLBillGenerator


def bill_view(request):
    bill_data = {'amount': 150}

    generator = PDFBillGenerator() if request.GET.get(
        'format') == 'pdf' else HTMLBillGenerator()

    return generator.generate_bill(bill_data)

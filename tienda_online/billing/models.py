from django.db import models

class Bill(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    pdf_file = models.FileField(upload_to='bills/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Factura de {self.customer_email} - {self.created_at}"
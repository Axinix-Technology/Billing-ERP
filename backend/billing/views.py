from django.db.models import Q
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order
from .pdf import generate_invoice_pdf_bytes


class OrderInvoicePDFView(APIView):
    """
    Binary PDF streaming endpoint for order invoices.
    Justified custom endpoint outside /api/populate/ because it streams binary application/pdf.
    """
    permission_classes = [AllowAny]

    def get(self, request, identifier):
        if identifier.isdigit():
            order = Order.objects.filter(Q(pk=int(identifier)) | Q(bill_number=identifier), status=1).first()
        else:
            order = Order.objects.filter(bill_number=identifier, status=1).first()

        if not order:
            return Response(
                {"success": False, "message": "Order invoice could not be found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        pdf_bytes = generate_invoice_pdf_bytes(order)
        response = HttpResponse(pdf_bytes, content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="Invoice_{order.bill_number}.pdf"'
        return response


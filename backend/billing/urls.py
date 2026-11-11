from django.urls import path
from .views import OrderInvoicePDFView

urlpatterns = [
    path('<str:identifier>/pdf', OrderInvoicePDFView.as_view(), name='order-invoice-pdf-no-slash'),
    path('<str:identifier>/pdf/', OrderInvoicePDFView.as_view(), name='order-invoice-pdf'),
]


from django.urls import path
from .views import SalesReportPDFView

urlpatterns = [
    path('pdf', SalesReportPDFView.as_view(), name='sales-report-pdf-no-slash'),
    path('pdf/', SalesReportPDFView.as_view(), name='sales-report-pdf'),
]


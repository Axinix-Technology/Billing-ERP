import datetime
from django.db.models import Avg, Count, Q, Sum
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from billing.models import Order
from .pdf import generate_sales_report_pdf_bytes


class SalesReportPDFView(APIView):
    """
    Binary PDF streaming endpoint for date-ranged sales reports.
    Justified custom endpoint outside /api/populate/ because it streams binary application/pdf.
    Respects active date range, payment method filter, and search query.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not getattr(request.user, "is_superadmin", False):
            return Response(
                {
                    "success": False,
                    "message": "Sales report export is restricted to store administrators.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        today = timezone.localdate()
        default_start = (today - datetime.timedelta(days=30)).isoformat()
        default_end = today.isoformat()

        start_str = (request.query_params.get("startDate") or default_start).strip()
        end_str = (request.query_params.get("endDate") or default_end).strip()
        search_term = (request.query_params.get("search") or "").strip()
        payment_filter = (request.query_params.get("payment_method") or "").strip().lower()

        try:
            start_date = datetime.date.fromisoformat(start_str)
            end_date = datetime.date.fromisoformat(end_str)
        except ValueError:
            return Response(
                {
                    "success": False,
                    "message": "Invalid date format. Please select valid start and end dates (YYYY-MM-DD).",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        qs = Order.objects.filter(
            status=1,
            created_at__date__gte=start_date,
            created_at__date__lte=end_date,
        )

        if payment_filter and payment_filter != "all":
            qs = qs.filter(payment_method=payment_filter)

        if search_term:
            qs = qs.filter(
                Q(bill_number__icontains=search_term)
                | Q(customer_name__icontains=search_term)
                | Q(customer_phone__icontains=search_term)
            )

        agg = qs.aggregate(
            total_revenue=Sum("grand_total"),
            total_orders=Count("id"),
            avg_order_value=Avg("grand_total"),
        )

        stats = {
            "total_revenue": float(agg["total_revenue"] or 0),
            "total_orders": int(agg["total_orders"] or 0),
            "avg_order_value": float(agg["avg_order_value"] or 0),
        }

        orders = list(qs.order_by("-id"))
        pdf_bytes = generate_sales_report_pdf_bytes(
            stats=stats,
            orders=orders,
            start_date=start_str,
            end_date=end_str,
            search_term=search_term,
            payment_filter=payment_filter,
        )

        response = HttpResponse(pdf_bytes, content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="Sales_Report_{start_str}_to_{end_str}.pdf"'
        return response


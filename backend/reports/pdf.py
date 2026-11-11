import io
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_sales_report_pdf_bytes(stats, orders, start_date, end_date, search_term="", payment_filter=""):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    generated_at = timezone.localtime(timezone.now()).strftime("%d %b %Y, %I:%M:%S %p")

    # Header Banner
    c.setFillColor(colors.HexColor("#4A2511"))
    c.rect(0, height - 95, width, 95, fill=1, stroke=0)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(40, height - 42, "CHAI POINT & BAKERY - SALES REPORT")

    c.setFont("Helvetica", 9.5)
    c.drawString(40, height - 64, f"Selected Period: {start_date} to {end_date}")
    c.drawRightString(width - 40, height - 64, f"Printed On: {generated_at}")

    # Context Metadata Bar (Rule 4: Date range, active filters, active search)
    y = height - 115
    c.setFillColor(colors.HexColor("#374151"))
    c.setFont("Helvetica", 9)
    filter_parts = [f"Date Range: {start_date} to {end_date}"]
    if payment_filter:
        filter_parts.append(f"Payment Method: {payment_filter.upper()}")
    if search_term:
        filter_parts.append(f"Search Query: '{search_term}'")
    c.drawString(40, y, "Active Criteria: " + "  |  ".join(filter_parts))

    # Summary KPI Box
    y -= 45
    c.setFillColor(colors.HexColor("#FEF3C7"))
    c.rect(40, y, width - 80, 36, fill=1, stroke=0)

    c.setFillColor(colors.HexColor("#4A2511"))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(55, y + 14, f"Total Orders: {stats['total_orders']}")
    c.drawString(215, y + 14, f"Total Revenue: Rs. {stats['total_revenue']:.2f}")
    c.drawString(405, y + 14, f"Avg Ticket: Rs. {stats['avg_order_value']:.2f}")

    # Table Header
    y -= 35
    c.setFillColor(colors.HexColor("#F3F4F6"))
    c.rect(40, y, width - 80, 22, fill=1, stroke=0)

    c.setFillColor(colors.HexColor("#1F2937"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(48, y + 7, "Bill Number")
    c.drawString(165, y + 7, "Customer")
    c.drawString(295, y + 7, "Date")
    c.drawString(400, y + 7, "Payment")
    c.drawRightString(width - 48, y + 7, "Total (Rs.)")

    # Table Rows
    y -= 18
    c.setFont("Helvetica", 8.5)
    c.setFillColor(colors.HexColor("#374151"))

    if not orders:
        c.drawString(48, y, "No matching orders found for the selected criteria.")
    else:
        for order in orders:
            if y < 60:
                c.showPage()
                y = height - 60
                c.setFont("Helvetica", 8.5)
                c.setFillColor(colors.HexColor("#374151"))

            dt = timezone.localtime(order.created_at).strftime("%d-%m-%Y %H:%M") if order.created_at else "-"
            c.drawString(48, y, str(order.bill_number))
            c.drawString(165, y, str(order.customer_name or "Walk-in")[:24])
            c.drawString(295, y, dt)
            c.drawString(400, y, str(order.payment_method or "cash").upper())
            c.drawRightString(width - 48, y, f"Rs. {float(order.grand_total):.2f}")

            y -= 6
            c.setStrokeColor(colors.HexColor("#E5E7EB"))
            c.setLineWidth(0.4)
            c.line(40, y, width - 40, y)
            y -= 14

    c.showPage()
    c.save()

    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


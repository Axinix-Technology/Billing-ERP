import io
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


def generate_invoice_pdf_bytes(order):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Header Banner (#4A2511 Dark Teak Theme)
    c.setFillColor(colors.HexColor("#4A2511"))
    c.rect(0, height - 100, width, 100, fill=1, stroke=0)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(40, height - 45, "CHAI POINT & BAKERY")

    c.setFont("Helvetica", 10)
    c.drawString(40, height - 65, "Authentic Artisanal Tea & Delights")
    c.drawRightString(width - 40, height - 45, "Tax Invoice / Cash Receipt")

    # Metadata
    y = height - 130
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y, "Invoice No:")
    c.setFont("Helvetica", 10)
    c.drawString(115, y, str(order.bill_number))

    created_local = timezone.localtime(order.created_at) if order.created_at else timezone.localtime(timezone.now())
    c.setFont("Helvetica-Bold", 10)
    c.drawString(330, y, "Date & Time:")
    c.setFont("Helvetica", 10)
    c.drawString(410, y, created_local.strftime("%d %b %Y, %I:%M %p"))

    y -= 18
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y, "Customer:")
    c.setFont("Helvetica", 10)
    c.drawString(115, y, str(order.customer_name or "Walk-in Customer"))

    c.setFont("Helvetica-Bold", 10)
    c.drawString(330, y, "Payment Mode:")
    c.setFont("Helvetica", 10)
    c.drawString(410, y, str(order.payment_method or "CASH").upper())

    if order.customer_phone:
        y -= 18
        c.setFont("Helvetica-Bold", 10)
        c.drawString(40, y, "Phone:")
        c.setFont("Helvetica", 10)
        c.drawString(115, y, str(order.customer_phone))

    # Divider Line
    y -= 20
    c.setStrokeColor(colors.HexColor("#D97706"))
    c.setLineWidth(1.5)
    c.line(40, y, width - 40, y)

    # Table Header
    y -= 30
    c.setFillColor(colors.HexColor("#F3F4F6"))
    c.rect(40, y, width - 80, 24, fill=1, stroke=0)

    c.setFillColor(colors.HexColor("#1F2937"))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y + 7, "S.No")
    c.drawString(95, y + 7, "Item Description")
    c.drawRightString(375, y + 7, "Price")
    c.drawRightString(425, y + 7, "Qty")
    c.drawRightString(width - 50, y + 7, "Amount (Rs.)")

    # Table Rows
    y -= 22
    c.setFont("Helvetica", 9.5)
    c.setFillColor(colors.HexColor("#374151"))

    items = order.items.filter(status=1)
    for idx, item in enumerate(items, start=1):
        if y < 120:
            c.showPage()
            y = height - 60

        desc = item.product_name
        if item.customization:
            desc += f" ({item.customization})"

        c.drawString(50, y, str(idx))
        c.drawString(95, y, desc[:45])
        c.drawRightString(375, y, f"Rs. {float(item.unit_price):.2f}")
        c.drawRightString(425, y, str(item.quantity))
        c.drawRightString(width - 50, y, f"Rs. {float(item.total_price):.2f}")

        y -= 8
        c.setStrokeColor(colors.HexColor("#E5E7EB"))
        c.setLineWidth(0.5)
        c.line(40, y, width - 40, y)
        y -= 16

    # Totals Summary
    y -= 12
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawRightString(440, y, "Subtotal:")
    c.drawRightString(width - 50, y, f"Rs. {float(order.subtotal):.2f}")

    if float(order.discount_amount) > 0:
        y -= 16
        c.drawRightString(440, y, "Discount:")
        c.drawRightString(width - 50, y, f"-Rs. {float(order.discount_amount):.2f}")

    y -= 16
    c.drawRightString(440, y, "Tax (GST):")
    c.drawRightString(width - 50, y, f"Rs. {float(order.tax_amount):.2f}")

    y -= 10
    c.setStrokeColor(colors.HexColor("#4A2511"))
    c.setLineWidth(1)
    c.line(330, y, width - 40, y)

    y -= 18
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor("#4A2511"))
    c.drawRightString(440, y, "Grand Total:")
    c.drawRightString(width - 50, y, f"Rs. {float(order.grand_total):.2f}")

    # Footer
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.HexColor("#6B7280"))
    c.drawCentredString(width / 2, 50, "Thank you for visiting Chai Point & Bakery! Have a refreshing day.")

    c.showPage()
    c.save()

    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes


# Method & Symbol Index: Reports & Analytics

| Symbol | Type | File Path | Lines | Responsibility | Related Symbols |
|---|---|---|---|---|---|
| `OrderService.execute_report` | Service Method | `backend/billing/services.py` | 132-199 | Computes aggregate KPIs, today revenue, payment breakdown, and top items via `POST /api/populate/report/order` | `Order`, `OrderItem` |
| `SalesReportPDFView` | APIView | `backend/reports/views.py` | 14-79 | Binary PDF stream endpoint (`GET /api/reports/pdf`) respecting active date range, search, and filters | `generate_sales_report_pdf_bytes` |
| `generate_sales_report_pdf_bytes` | Utility Function | `backend/reports/pdf.py` | 8-97 | Builds PDF sales report displaying print timestamp, date range, active criteria, and order list | `SalesReportPDFView` |
| `ReportsPage` | React Page Component | `frontend/src/pages/ReportsPage.jsx` | 1-280 | Analytics dashboard screen displaying KPIs and date-range PDF exporter | `OrderService.execute_report` |

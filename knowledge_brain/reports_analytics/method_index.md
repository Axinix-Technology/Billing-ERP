# Method & Symbol Index: Reports & Analytics

| Symbol | Type | File Path | Lines | Responsibility | Related Symbols |
|---|---|---|---|---|---|
| `get_dashboard_stats` | APIView / Function | `backend/reports/views.py` | Verify by symbol search | Computes aggregate KPIs, today revenue, payment breakdown, and top items | `Order`, `OrderItem` |
| `export_sales_report_pdf` | APIView / Function | `backend/reports/views.py` | Verify by symbol search | Generates tabular date-ranged sales report PDF | `generate_report_pdf` |
| `generate_report_pdf` | Utility Function | `backend/reports/pdf.py` | Verify by symbol search | Builds PDF canvas and document structure using ReportLab | `export_sales_report_pdf` |
| `ReportsPage` | React Page Component | `frontend/src/pages/ReportsPage.jsx` | 1-280 | Analytics dashboard screen displaying KPIs and date-range PDF exporter | `api.getDashboardStats` |

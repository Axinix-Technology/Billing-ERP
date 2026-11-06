# End-to-End Data Flow: Reports & Analytics

## 1. Flow 1: Dashboard Analytics Aggregation

- **Trigger:** Admin navigates to `/reports`.
- **Starting Screen:** `frontend/src/pages/ReportsPage.jsx`
- **Frontend Logic:**
  - Invokes `api.getDashboardStats()` on mount.
- **API Request:**
  - `GET /api/reports/dashboard`
  - Headers: `Authorization: Bearer <token>`
- **Backend View / Handler:**
  - `backend/reports/views.py:get_dashboard_stats`
  - Validates `request.user.role.is_superadmin`.
  - Performs aggregations:
    - Overall: `SUM(grand_total)`, `COUNT(id)`, `AVG(grand_total)` from `Order`.
    - Today: `SUM(grand_total)`, `COUNT(id)` where `created_at__date == today`.
    - Payments: `values('payment_method').annotate(count=Count('id'), total=Sum('grand_total'))`.
    - Top Products: `values('product_name').annotate(total_qty=Sum('quantity'), total_sales=Sum('total_price')).order_by('-total_qty')[:5]`.
- **Response Shape:**
  - Status `200 OK`:
    ```json
    {
      "success": true,
      "stats": {
        "total_revenue": "125000.00",
        "total_orders": 350,
        "avg_order_value": "357.14",
        "today_revenue": "4200.00",
        "today_orders": 24,
        "paymentBreakdown": [...],
        "topProducts": [...],
        "recentOrders": [...]
      }
    }
    ```
- **State Update & Resulting Screen:**
  - Populates metric bars, charts, and summary tables on `ReportsPage.jsx`.

---

## 2. Flow 2: Sales Summary PDF Export

- **Trigger:** Admin clicks "Export PDF" with date range inputs.
- **API Request:** `GET /api/reports/pdf?startDate=2026-11-01&endDate=2026-11-06`
- **Backend Logic:** Aggregates orders between `startDate` and `endDate`, builds tabular summary using ReportLab, and streams binary `application/pdf`.

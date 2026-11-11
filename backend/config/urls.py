from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def health_check(request):
    return JsonResponse({
        "status": "OK",
        "message": "Billing ERP Backend API (Axinix Core) is operational",
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health', health_check, name='api-health-no-slash'),
    path('api/health/', health_check, name='api-health'),
    path('api/auth/', include('users.urls')),
    path('api/populate/', include(('populate_core.urls', 'populate'), namespace='populate')),
    path('api/orders/', include('billing.urls')),
    path('api/reports/', include('reports.urls')),
]


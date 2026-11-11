from django.urls import path
from .views import LoginView, ProfileView, LogoutView

urlpatterns = [
    path('login', LoginView.as_view(), name='auth-login-no-slash'),
    path('login/', LoginView.as_view(), name='auth-login'),
    path('me', ProfileView.as_view(), name='auth-me-no-slash'),
    path('me/', ProfileView.as_view(), name='auth-me'),
    path('logout', LogoutView.as_view(), name='auth-logout-no-slash'),
    path('logout/', LogoutView.as_view(), name='auth-logout'),
]


from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from auth.views import CustomLoginView, RefreshTokenView, RegisterView


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/token/', CustomLoginView.as_view()),
    path('api/register/', RegisterView.as_view()),
    path('api/token/refresh/', RefreshTokenView.as_view()),
    
    path('api/', include('feedback.urls')),
]

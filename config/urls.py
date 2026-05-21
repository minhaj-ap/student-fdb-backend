from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from auth.views import AutoLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/token/', AutoLoginView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/register/', include('users.urls')),
    
    path('api/', include('feedback.urls')),
]

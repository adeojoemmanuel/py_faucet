from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin2/', admin.site.urls),
    path('', include('faucet.urls')),  # Include app URLs at root
]
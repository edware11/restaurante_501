"""
config/urls.py — URLs raíz del proyecto Restaurante Pasta La Vista
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # ── Django Admin (superusuario) ──────────────────────
    path('admin/', admin.site.urls),

    # ── App gestion (todas las demás rutas) ──────────────
    path('', include('gestion.urls')),
]

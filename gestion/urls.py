from django.urls import path
from . import views

urlpatterns = [

    # ── Dashboard ──────────────────────────────────────────
    path('', views.inicio, name='inicio'),

    # ── Autenticación ──────────────────────────────────────
    path('login/',    views.login_view,   name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/',   views.logout_view,   name='logout'),

    # ── Clientes ───────────────────────────────────────────
    path('clientes/',                      views.clientes_lista,   name='clientes'),
    path('clientes/nuevo/',                views.cliente_crear,    name='cliente_crear'),
    path('clientes/<int:pk>/editar/',      views.cliente_editar,   name='cliente_editar'),
    path('clientes/<int:pk>/eliminar/',    views.cliente_eliminar, name='cliente_eliminar'),

    # ── Empleados ──────────────────────────────────────────
    path('empleados/',                     views.empleados_lista,   name='empleados'),
    path('empleados/nuevo/',               views.empleado_crear,    name='empleado_crear'),
    path('empleados/<int:pk>/editar/',     views.empleado_editar,   name='empleado_editar'),
    path('empleados/<int:pk>/eliminar/',   views.empleado_eliminar, name='empleado_eliminar'),

    # ── Mesas ──────────────────────────────────────────────
    path('mesas/',                         views.mesas_lista,   name='mesas'),
    path('mesas/nueva/',                   views.mesa_crear,    name='mesa_crear'),
    path('mesas/<int:pk>/editar/',         views.mesa_editar,   name='mesa_editar'),
    path('mesas/<int:pk>/eliminar/',       views.mesa_eliminar, name='mesa_eliminar'),

    # ── Platos ─────────────────────────────────────────────
    path('platos/',                        views.platos_lista,   name='platos'),
    path('platos/nuevo/',                  views.plato_crear,    name='plato_crear'),
    path('platos/<int:pk>/editar/',        views.plato_editar,   name='plato_editar'),
    path('platos/<int:pk>/eliminar/',      views.plato_eliminar, name='plato_eliminar'),

    # ── Órdenes ────────────────────────────────────────────
    path('ordenes/',                       views.ordenes_lista,   name='ordenes'),
    path('ordenes/nueva/',                 views.orden_crear,     name='orden_crear'),
    path('ordenes/<int:pk>/editar/',       views.orden_editar,    name='orden_editar'),
    path('ordenes/<int:pk>/eliminar/',     views.orden_eliminar,  name='orden_eliminar'),

    # ── Facturas ───────────────────────────────────────────
    path('facturas/',                      views.facturas_lista, name='facturas'),
]

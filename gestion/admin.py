from django.contrib import admin
from .models import Cliente, Empleado, Mesa, Plato, Orden, DetalleOrden, Factura

admin.site.site_header  = '🍝 Pasta La Vista — Administración'
admin.site.site_title   = 'Admin Restaurante'
admin.site.index_title  = 'Panel de Control'


class DetalleOrdenInline(admin.TabularInline):
    model  = DetalleOrden
    extra  = 1
    fields = ('plato_id', 'cantidad', 'precio_unitario')


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'telefono', 'correo')
    search_fields = ('nombre', 'correo')
    ordering      = ('nombre',)


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'cargo', 'telefono', 'correo')
    search_fields = ('nombre', 'cargo')
    list_filter   = ('cargo',)
    ordering      = ('nombre',)


@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('numero_mesa', 'capacidad', 'estado_mesa')
    list_filter  = ('estado_mesa',)
    ordering     = ('numero_mesa',)


@admin.register(Plato)
class PlatoAdmin(admin.ModelAdmin):
    list_display  = ('nombre_plato', 'categoria', 'precio', 'disponible')
    search_fields = ('nombre_plato', 'categoria')
    list_filter   = ('categoria', 'disponible')
    ordering      = ('nombre_plato',)


@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ('pk', 'mesa_id', 'empleado_id', 'cliente_id', 'fecha_hora', 'estado_orden')
    list_filter  = ('estado_orden',)
    ordering     = ('-fecha_hora',)
    inlines      = [DetalleOrdenInline]


@admin.register(DetalleOrden)
class DetalleOrdenAdmin(admin.ModelAdmin):
    list_display = ('pk', 'orden_id', 'plato_id', 'cantidad', 'precio_unitario')


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'orden_id', 'fecha_factura', 'total_factura', 'metodo_pago')
    ordering     = ('-fecha_factura',)
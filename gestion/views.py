from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .models import Cliente, Empleado, Mesa, Plato, Orden, Factura, DetalleOrden
from .decorators import rol_requerido


# ============================================================
# AUTENTICACIÓN
# ============================================================

def login_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.username}!')
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'gestion/login.html')


def registro_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        username  = request.POST.get('username')
        email     = request.POST.get('email', '')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Ese nombre de usuario ya está en uso.')
        elif len(password1) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
        else:
            User.objects.create_user(username=username, email=email, password=password1)
            messages.success(request, 'Cuenta creada. Ahora puedes iniciar sesión.')
            return redirect('login')
    return render(request, 'gestion/registro.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'Sesión cerrada.')
    return redirect('login')


# ============================================================
# DASHBOARD
# ============================================================

@login_required
def inicio(request):
    context = {
        'total_clientes':  Cliente.objects.count(),
        'total_empleados': Empleado.objects.count(),
        'total_mesas':     Mesa.objects.count(),
        'total_platos':    Plato.objects.count(),
        'total_ordenes':   Orden.objects.count(),
        'total_facturas':  Factura.objects.count(),
    }
    return render(request, 'gestion/inicio.html', context)


# ============================================================
# CLIENTES
# ============================================================

@rol_requerido('admin', 'mesero')
def clientes_lista(request):
    clientes = Cliente.objects.all().order_by('nombre')
    return render(request, 'gestion/clientes_lista.html', {'clientes': clientes})

@rol_requerido('admin', 'mesero')
def cliente_crear(request):
    if request.method == 'POST':
        Cliente.objects.create(
            nombre   = request.POST['nombre'],
            telefono = request.POST.get('telefono', ''),
            correo   = request.POST.get('correo', '') or None,
        )
        messages.success(request, 'Cliente creado correctamente.')
        return redirect('clientes')
    return render(request, 'gestion/cliente_form.html')

@rol_requerido('admin')
def cliente_editar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.nombre   = request.POST['nombre']
        cliente.telefono = request.POST.get('telefono', '')
        cliente.correo   = request.POST.get('correo', '') or None
        cliente.save()
        messages.success(request, 'Cliente actualizado.')
        return redirect('clientes')
    return render(request, 'gestion/cliente_form.html', {'objeto': cliente})

@rol_requerido('admin')
def cliente_eliminar(request, pk):
    get_object_or_404(Cliente, pk=pk).delete()
    messages.success(request, 'Cliente eliminado.')
    return redirect('clientes')


# ============================================================
# EMPLEADOS — solo admin
# ============================================================

@rol_requerido('admin')
def empleados_lista(request):
    empleados = Empleado.objects.all().order_by('nombre')
    return render(request, 'gestion/empleados_lista.html', {'empleados': empleados})

@rol_requerido('admin')
def empleado_crear(request):
    if request.method == 'POST':
        Empleado.objects.create(
            nombre   = request.POST['nombre'],
            cargo    = request.POST.get('cargo', ''),
            telefono = request.POST.get('telefono', ''),
            correo   = request.POST.get('correo', '') or None,
        )
        messages.success(request, 'Empleado creado.')
        return redirect('empleados')
    return render(request, 'gestion/empleado_form.html')

@rol_requerido('admin')
def empleado_editar(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == 'POST':
        empleado.nombre   = request.POST['nombre']
        empleado.cargo    = request.POST.get('cargo', '')
        empleado.telefono = request.POST.get('telefono', '')
        empleado.correo   = request.POST.get('correo', '') or None
        empleado.save()
        messages.success(request, 'Empleado actualizado.')
        return redirect('empleados')
    return render(request, 'gestion/empleado_form.html', {'objeto': empleado})

@rol_requerido('admin')
def empleado_eliminar(request, pk):
    get_object_or_404(Empleado, pk=pk).delete()
    messages.success(request, 'Empleado eliminado.')
    return redirect('empleados')


# ============================================================
# MESAS
# ============================================================

@rol_requerido('admin', 'mesero')
def mesas_lista(request):
    mesas = Mesa.objects.all().order_by('numero_mesa')
    return render(request, 'gestion/mesas_lista.html', {'mesas': mesas})

@rol_requerido('admin')
def mesa_crear(request):
    if request.method == 'POST':
        Mesa.objects.create(
            numero_mesa = request.POST['numero_mesa'],
            capacidad   = request.POST.get('capacidad', 4),
            estado_mesa = request.POST.get('estado', 'disponible'),
        )
        messages.success(request, 'Mesa creada.')
        return redirect('mesas')
    return render(request, 'gestion/mesa_form.html')

@rol_requerido('admin')
def mesa_editar(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    if request.method == 'POST':
        mesa.numero_mesa = request.POST['numero_mesa']
        mesa.capacidad   = request.POST.get('capacidad', 4)
        mesa.estado_mesa = request.POST.get('estado', 'disponible')
        mesa.save()
        messages.success(request, 'Mesa actualizada.')
        return redirect('mesas')
    return render(request, 'gestion/mesa_form.html', {'objeto': mesa})

@rol_requerido('admin')
def mesa_eliminar(request, pk):
    get_object_or_404(Mesa, pk=pk).delete()
    messages.success(request, 'Mesa eliminada.')
    return redirect('mesas')

@rol_requerido('admin', 'mesero')
def mesa_cambiar_estado(request, pk):
    mesa = get_object_or_404(Mesa, pk=pk)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in ['disponible', 'ocupada', 'reservada']:
            mesa.estado_mesa = nuevo_estado
            mesa.save()
            messages.success(request, f'Mesa {mesa.numero_mesa} marcada como {nuevo_estado}.')
    return redirect('mesas')


# ============================================================
# PLATOS
# ============================================================

@rol_requerido('admin', 'mesero', 'caja')
def platos_lista(request):
    platos = Plato.objects.all().order_by('nombre_plato')
    platos_facturados = set(
        DetalleOrden.objects.filter(
            orden_id__factura__isnull=False
        ).values_list('plato_id_id', flat=True)
    )
    return render(request, 'gestion/platos_lista.html', {
        'platos': platos,
        'platos_facturados': platos_facturados,
    })

@rol_requerido('admin', 'mesero')
def plato_crear(request):
    if request.method == 'POST':
        Plato.objects.create(
            nombre_plato = request.POST['nombre'],
            descripcion  = request.POST.get('descripcion', ''),
            precio       = request.POST['precio'],
            categoria    = request.POST.get('categoria', ''),
            disponible   = True,
        )
        messages.success(request, 'Plato creado.')
        return redirect('platos')
    return render(request, 'gestion/plato_form.html')

@rol_requerido('admin', 'mesero')
def plato_editar(request, pk):
    plato = get_object_or_404(Plato, pk=pk)
    if request.method == 'POST':
        plato.nombre_plato = request.POST['nombre']
        plato.descripcion  = request.POST.get('descripcion', '')
        plato.precio       = request.POST['precio']
        plato.categoria    = request.POST.get('categoria', '')
        plato.save()
        messages.success(request, 'Plato actualizado.')
        return redirect('platos')
    return render(request, 'gestion/plato_form.html', {'objeto': plato})

@rol_requerido('admin', 'mesero')
def plato_eliminar(request, pk):
    get_object_or_404(Plato, pk=pk).delete()
    messages.success(request, 'Plato eliminado.')
    return redirect('platos')


# ============================================================
# ÓRDENES
# ============================================================

@rol_requerido('admin', 'mesero')
def ordenes_lista(request):
    ordenes = Orden.objects.select_related(
        'mesa_id', 'empleado_id', 'cliente_id'
    ).all().order_by('-fecha_hora')
    return render(request, 'gestion/ordenes_lista.html', {'ordenes': ordenes})


def _procesar_detalles(request, orden):
    """Helper compartido: lee los platos del POST, crea DetalleOrden y retorna el total."""
    platos_texto = request.POST.getlist('plato_texto[]')
    cantidades   = request.POST.getlist('cantidad[]')
    terminos     = request.POST.getlist('termino[]')
    alergias_l   = request.POST.getlist('alergias[]')
    notas_l      = request.POST.getlist('notas[]')

    total = 0
    for i, nombre_plato in enumerate(platos_texto):
        if not nombre_plato.strip():
            continue

        plato = Plato.objects.filter(nombre_plato=nombre_plato.strip()).first()
        if not plato:
            continue

        precio   = plato.precio
        cantidad = int(cantidades[i]) if i < len(cantidades) else 1
        subtotal = precio * cantidad
        total   += subtotal

        DetalleOrden.objects.create(
            orden_id        = orden,
            plato_id        = plato,
            cantidad        = cantidad,
            precio_unitario = precio,
            subtotal        = subtotal,
            termino         = terminos[i]   if i < len(terminos)   else '',
            alergias        = alergias_l[i] if i < len(alergias_l) else '',
            notas           = notas_l[i]    if i < len(notas_l)    else '',
        )

    return total


@rol_requerido('admin', 'mesero')
def orden_crear(request):
    if request.method == 'POST':
        mesa     = get_object_or_404(Mesa, pk=request.POST['id_mesa'])
        empleado = get_object_or_404(Empleado, pk=request.POST['id_empleado'])
        cliente  = get_object_or_404(Cliente, pk=request.POST['id_cliente']) if request.POST.get('id_cliente') else None

        orden = Orden.objects.create(
            mesa_id      = mesa,
            empleado_id  = empleado,
            cliente_id   = cliente,
            estado_orden = 'pendiente',
            total        = 0,
        )

        mesa.estado_mesa = 'ocupada'
        mesa.save()

        orden.total = _procesar_detalles(request, orden)
        orden.save()

        messages.success(request, f'Orden #{orden.pk} creada. Mesero: {empleado.nombre}. Mesa {mesa.numero_mesa} marcada como ocupada.')
        return redirect('ordenes')

    mesas     = Mesa.objects.filter(estado_mesa='disponible').order_by('numero_mesa')
    clientes  = Cliente.objects.all().order_by('nombre')
    platos    = Plato.objects.filter(disponible=True).order_by('nombre_plato')
    empleados = Empleado.objects.all().order_by('nombre')
    return render(request, 'gestion/orden_form.html', {
        'mesas':     mesas,
        'clientes':  clientes,
        'platos':    platos,
        'empleados': empleados,
    })


@rol_requerido('admin', 'mesero')
def orden_editar(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    if request.method == 'POST':
        mesa     = get_object_or_404(Mesa, pk=request.POST['id_mesa'])
        empleado = get_object_or_404(Empleado, pk=request.POST['id_empleado'])
        cliente  = get_object_or_404(Cliente, pk=request.POST['id_cliente']) if request.POST.get('id_cliente') else None

        orden.mesa_id      = mesa
        orden.empleado_id  = empleado
        orden.cliente_id   = cliente
        orden.estado_orden = request.POST.get('estado', orden.estado_orden)
        orden.save()

        orden.detalles.all().delete()

        orden.total = _procesar_detalles(request, orden)
        orden.save()

        messages.success(request, f'Orden #{orden.pk} actualizada.')
        return redirect('ordenes')

    context = {
        'objeto':    orden,
        'detalles':  orden.detalles.all(),
        'mesas':     Mesa.objects.filter(estado_mesa='disponible').order_by('numero_mesa'),
        'clientes':  Cliente.objects.all().order_by('nombre'),
        'platos':    Plato.objects.filter(disponible=True).order_by('nombre_plato'),
        'empleados': Empleado.objects.all().order_by('nombre'),
    }
    return render(request, 'gestion/orden_form.html', context)


@rol_requerido('admin', 'mesero')
def orden_eliminar(request, pk):
    get_object_or_404(Orden, pk=pk).delete()
    messages.success(request, 'Orden eliminada.')
    return redirect('ordenes')


# ============================================================
# FACTURAS — admin y caja
# ============================================================

@rol_requerido('admin', 'caja')
def facturas_lista(request):
    facturas = Factura.objects.select_related('orden_id').all().order_by('-fecha_factura')
    ordenes_pendientes = Orden.objects.filter(
        factura__isnull=True
    ).exclude(
        estado_orden='cancelada'
    ).select_related('mesa_id', 'cliente_id').order_by('-fecha_hora')
    return render(request, 'gestion/facturas_lista.html', {
        'facturas': facturas,
        'ordenes_pendientes': ordenes_pendientes,
    })


@rol_requerido('admin', 'caja')
def factura_generar(request, orden_pk):
    orden = get_object_or_404(Orden, pk=orden_pk)

    if hasattr(orden, 'factura'):
        messages.warning(request, f'La orden #{orden.pk} ya tiene factura generada.')
        return redirect('facturas')

    if request.method == 'POST':
        metodo_pago   = request.POST.get('metodo_pago', 'efectivo')
        subtotal      = orden.total
        impuesto      = subtotal * 19 / 100
        total_factura = subtotal + impuesto

        Factura.objects.create(
            orden_id      = orden,
            metodo_pago   = metodo_pago,
            subtotal      = subtotal,
            impuesto      = impuesto,
            total_factura = total_factura,
        )

        orden.mesa_id.estado_mesa = 'disponible'
        orden.mesa_id.save()

        orden.estado_orden = 'entregada'
        orden.save()

        messages.success(request, f'Factura generada para la orden #{orden.pk}.')
        return redirect('facturas')

    detalles = orden.detalles.select_related('plato_id').all()
    return render(request, 'gestion/factura_form.html', {
        'orden': orden,
        'detalles': detalles,
    })


def error_403(request, exception):
    return render(request, 'gestion/403.html', status=403)
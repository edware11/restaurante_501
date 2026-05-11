from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Cliente, Empleado, Mesa, Plato, Orden, Factura


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
# CLIENTES — CRUD
# ============================================================

def clientes_lista(request):
    clientes = Cliente.objects.all().order_by('nombre')
    return render(request, 'gestion/clientes_lista.html', {'clientes': clientes})


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


def cliente_eliminar(request, pk):
    get_object_or_404(Cliente, pk=pk).delete()
    messages.success(request, 'Cliente eliminado.')
    return redirect('clientes')


# ============================================================
# EMPLEADOS — CRUD
# ============================================================

def empleados_lista(request):
    empleados = Empleado.objects.all().order_by('nombre')
    return render(request, 'gestion/empleados_lista.html', {'empleados': empleados})


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


def empleado_eliminar(request, pk):
    get_object_or_404(Empleado, pk=pk).delete()
    messages.success(request, 'Empleado eliminado.')
    return redirect('empleados')


# ============================================================
# MESAS — CRUD
# ============================================================

def mesas_lista(request):
    mesas = Mesa.objects.all().order_by('numero_mesa')
    return render(request, 'gestion/mesas_lista.html', {'mesas': mesas})


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


def mesa_eliminar(request, pk):
    get_object_or_404(Mesa, pk=pk).delete()
    messages.success(request, 'Mesa eliminada.')
    return redirect('mesas')


# ============================================================
# PLATOS — CRUD
# ============================================================

def platos_lista(request):
    platos = Plato.objects.all().order_by('nombre_plato')
    return render(request, 'gestion/platos_lista.html', {'platos': platos})


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


def plato_eliminar(request, pk):
    get_object_or_404(Plato, pk=pk).delete()
    messages.success(request, 'Plato eliminado.')
    return redirect('platos')


# ============================================================
# ÓRDENES — CRUD
# ============================================================

def ordenes_lista(request):
    ordenes = Orden.objects.select_related(
        'mesa_id', 'empleado_id', 'cliente_id'
    ).all().order_by('-fecha_hora')
    return render(request, 'gestion/ordenes_lista.html', {'ordenes': ordenes})


def orden_crear(request):
    if request.method == 'POST':
        Orden.objects.create(
            mesa_id     = get_object_or_404(Mesa,     pk=request.POST['id_mesa']),
            empleado_id = get_object_or_404(Empleado, pk=request.POST['id_empleado']),
            cliente_id  = get_object_or_404(Cliente,  pk=request.POST['id_cliente']) if request.POST.get('id_cliente') else None,
            estado_orden = request.POST.get('estado', 'pendiente'),
            total        = 0,
        )
        messages.success(request, 'Orden creada correctamente.')
        return redirect('ordenes')
    context = {
        'mesas':     Mesa.objects.all().order_by('numero_mesa'),
        'empleados': Empleado.objects.all().order_by('nombre'),
        'clientes':  Cliente.objects.all().order_by('nombre'),
    }
    return render(request, 'gestion/orden_form.html', context)


def orden_editar(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    if request.method == 'POST':
        orden.mesa_id     = get_object_or_404(Mesa,     pk=request.POST['id_mesa'])
        orden.empleado_id = get_object_or_404(Empleado, pk=request.POST['id_empleado'])
        orden.cliente_id  = get_object_or_404(Cliente,  pk=request.POST['id_cliente']) if request.POST.get('id_cliente') else None
        orden.estado_orden = request.POST.get('estado', orden.estado_orden)
        orden.save()
        messages.success(request, 'Orden actualizada.')
        return redirect('ordenes')
    context = {
        'objeto':    orden,
        'mesas':     Mesa.objects.all().order_by('numero_mesa'),
        'empleados': Empleado.objects.all().order_by('nombre'),
        'clientes':  Cliente.objects.all().order_by('nombre'),
    }
    return render(request, 'gestion/orden_form.html', context)


def orden_eliminar(request, pk):
    get_object_or_404(Orden, pk=pk).delete()
    messages.success(request, 'Orden eliminada.')
    return redirect('ordenes')


# ============================================================
# FACTURAS
# ============================================================

def facturas_lista(request):
    facturas = Factura.objects.all().order_by('-fecha_factura')
    return render(request, 'gestion/facturas_lista.html', {'facturas': facturas})
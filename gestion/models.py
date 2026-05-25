from django.db import models


class Cliente(models.Model):
    nombre   = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    correo   = models.EmailField(unique=True, blank=True, null=True)

    class Meta:
        db_table = 'Cliente'

    def __str__(self):
        return self.nombre


class Empleado(models.Model):
    CARGOS = [
        ('Mesero',        'Mesero'),
        ('Mesera',        'Mesera'),
        ('Cajero',        'Cajero'),
        ('Cajera',        'Cajera'),
        ('Administrador', 'Administrador'),
    ]
    nombre   = models.CharField(max_length=100)
    cargo    = models.CharField(max_length=50, choices=CARGOS)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    correo   = models.EmailField(unique=True, blank=True, null=True)

    class Meta:
        db_table = 'Empleado'

    def __str__(self):
        return f'{self.nombre} — {self.cargo}'


class Mesa(models.Model):
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('ocupada',    'Ocupada'),
        ('reservada',  'Reservada'),
    ]
    numero_mesa = models.IntegerField(unique=True)
    capacidad   = models.IntegerField(default=4)
    estado_mesa = models.CharField(max_length=20, choices=ESTADOS, default='disponible')

    class Meta:
        db_table = 'Mesa'

    def __str__(self):
        return f'Mesa {self.numero_mesa} ({self.estado_mesa})'


class Plato(models.Model):
    nombre_plato = models.CharField(max_length=100)
    descripcion  = models.TextField(blank=True, null=True)
    precio       = models.DecimalField(max_digits=10, decimal_places=2)
    categoria    = models.CharField(max_length=50, blank=True, null=True)
    disponible   = models.BooleanField(default=True)

    class Meta:
        db_table = 'Plato'

    def __str__(self):
        return f'{self.nombre_plato} — ${self.precio}'


class Orden(models.Model):
    ESTADOS = [
        ('pendiente',  'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('lista',      'Lista'),
        ('entregada',  'Entregada'),
        ('cancelada',  'Cancelada'),
    ]
    fecha_hora   = models.DateTimeField(auto_now_add=True)
    estado_orden = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    total        = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cliente_id   = models.ForeignKey('Cliente',  on_delete=models.PROTECT, db_column='cliente_id',  null=True, blank=True)
    empleado_id = models.ForeignKey('Empleado', on_delete=models.PROTECT, db_column='empleado_id', null=True, blank=True)
    mesa_id      = models.ForeignKey('Mesa',     on_delete=models.PROTECT, db_column='mesa_id')

    class Meta:
        db_table = 'OrdenRestaurante'

    def __str__(self):
        return f'Orden #{self.pk}'


class DetalleOrden(models.Model):
    TERMINO_CHOICES = [
        ('',             '— Sin especificar —'),
        ('medio',        'Término medio'),
        ('tres_cuartos', 'Tres cuartos'),
        ('bien_cocido',  'Bien cocido'),
    ]
    cantidad        = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    subtotal        = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    termino         = models.CharField(max_length=20, choices=TERMINO_CHOICES, blank=True, default='')
    alergias        = models.TextField(blank=True, default='')
    notas           = models.TextField(blank=True, default='')
    orden_id        = models.ForeignKey(Orden, on_delete=models.CASCADE,  db_column='orden_id', related_name='detalles')
    plato_id        = models.ForeignKey(Plato, on_delete=models.PROTECT,  db_column='plato_id')

    class Meta:
        db_table = 'Detalle_Orden'


class Factura(models.Model):
    fecha_factura = models.DateTimeField(auto_now_add=True)
    subtotal      = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    impuesto      = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_factura = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    metodo_pago   = models.CharField(max_length=30)
    orden_id      = models.OneToOneField(Orden, on_delete=models.PROTECT, db_column='orden_id')

    class Meta:
        db_table = 'Factura'

    def __str__(self):
        return f'Factura #{self.pk} — ${self.total_factura}'
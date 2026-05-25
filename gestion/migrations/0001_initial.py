from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('correo', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
            ],
            options={'db_table': 'Cliente'},
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('cargo', models.CharField(choices=[('Mesero','Mesero'),('Mesera','Mesera'),('Cajero','Cajero'),('Cajera','Cajera'),('Administrador','Administrador')], max_length=50)),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('correo', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
            ],
            options={'db_table': 'Empleado'},
        ),
        migrations.CreateModel(
            name='Mesa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_mesa', models.IntegerField(unique=True)),
                ('capacidad', models.IntegerField(default=4)),
                ('estado_mesa', models.CharField(choices=[('disponible','Disponible'),('ocupada','Ocupada'),('reservada','Reservada')], default='disponible', max_length=20)),
            ],
            options={'db_table': 'Mesa'},
        ),
        migrations.CreateModel(
            name='Plato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_plato', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('categoria', models.CharField(blank=True, max_length=50, null=True)),
                ('disponible', models.BooleanField(default=True)),
            ],
            options={'db_table': 'Plato'},
        ),
        migrations.CreateModel(
            name='Orden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora', models.DateTimeField(auto_now_add=True)),
                ('estado_orden', models.CharField(choices=[('pendiente','Pendiente'),('en_proceso','En proceso'),('lista','Lista'),('entregada','Entregada'),('cancelada','Cancelada')], default='pendiente', max_length=20)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('cliente_id', models.ForeignKey(blank=True, db_column='cliente_id', null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion.cliente')),
                ('empleado_id', models.ForeignKey(db_column='empleado_id', on_delete=django.db.models.deletion.PROTECT, to='gestion.empleado')),
                ('mesa_id', models.ForeignKey(db_column='mesa_id', on_delete=django.db.models.deletion.PROTECT, to='gestion.mesa')),
            ],
            options={'db_table': 'OrdenRestaurante'},
        ),
        migrations.CreateModel(
            name='DetalleOrden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=1)),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('termino', models.CharField(blank=True, choices=[('','— Sin especificar —'),('medio','Término medio'),('tres_cuartos','Tres cuartos'),('bien_cocido','Bien cocido')], default='', max_length=20)),
                ('alergias', models.TextField(blank=True, default='')),
                ('notas', models.TextField(blank=True, default='')),
                ('orden_id', models.ForeignKey(db_column='orden_id', on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='gestion.orden')),
                ('plato_id', models.ForeignKey(db_column='plato_id', on_delete=django.db.models.deletion.PROTECT, to='gestion.plato')),
            ],
            options={'db_table': 'Detalle_Orden'},
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_factura', models.DateTimeField(auto_now_add=True)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('impuesto', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_factura', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('metodo_pago', models.CharField(max_length=30)),
                ('orden_id', models.OneToOneField(db_column='orden_id', on_delete=django.db.models.deletion.PROTECT, to='gestion.orden')),
            ],
            options={'db_table': 'Factura'},
        ),
    ]
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Crea los grupos de roles: admin, mesero, caja'

    def handle(self, *args, **kwargs):
        for nombre in ['admin', 'mesero', 'caja']:
            group, created = Group.objects.get_or_create(name=nombre)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Grupo "{nombre}" creado'))
            else:
                self.stdout.write(f'— Grupo "{nombre}" ya existía')

        self.stdout.write(self.style.SUCCESS('\n✔ Listo. Ahora asigna los grupos a tus usuarios desde /admin/'))

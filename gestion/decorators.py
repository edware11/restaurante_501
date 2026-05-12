from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from functools import wraps


def rol_requerido(*roles):
    """
    Uso: @rol_requerido('admin', 'mesero')
    Roles válidos: 'admin', 'mesero', 'caja'
    El superusuario/admin siempre pasa.
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            user = request.user
            # Admin/superusuario tiene acceso a todo
            if user.is_superuser or user.groups.filter(name='admin').exists():
                return view_func(request, *args, **kwargs)
            # Verifica si tiene alguno de los roles requeridos
            if user.groups.filter(name__in=roles).exists():
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return wrapper
    return decorator
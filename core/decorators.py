"""
Decoradores personalizados para control de acceso.
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from functools import wraps

def admin_required(view_func):
    """
    Decorador que requiere que el usuario esté autenticado Y sea administrador.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not (request.user.is_staff or request.user.is_superuser):
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

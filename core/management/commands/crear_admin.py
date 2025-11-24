"""
Comando de gestión para crear el usuario administrador.
Uso: python manage.py crear_admin
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Crea el usuario administrador Cristian Erre'

    def handle(self, *args, **kwargs):
        email = 'cristianerreweb@gmail.com'
        username = 'cristianerre'
        password = 'root123'
        
        # Verificar si ya existe
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'El usuario con email {email} ya existe.')
            )
            return
        
        # Crear superusuario
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name='Cristian',
            last_name='Erre'
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Usuario administrador creado exitosamente!')
        )
        self.stdout.write(f'   Email: {email}')
        self.stdout.write(f'   Contraseña: {password}')

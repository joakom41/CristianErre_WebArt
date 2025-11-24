from django.contrib import admin
from .models import Banner

class BannerAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'orden', 'imagen',)
    list_editable = ('orden',) # Esto facilita el control del orden

admin.site.register(Banner, BannerAdmin)
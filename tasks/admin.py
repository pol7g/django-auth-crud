from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", ) # pongo coma por que es una tupla de un solo elemento!

# Register your models here.
admin.site.register(Task, TaskAdmin)  # registro aca para que la tabla tenga acceso al panel de adminstrador


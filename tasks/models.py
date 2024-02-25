from django.db import models
from django.contrib.auth.models import User

# Create your models here. Tablas de base de datos
#Cuando creo una tabla, en terminal comando: python manage.py makemigrations
#desp segundo com: python manage.py migrate
class Task(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField(blank = True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null = True, blank = True) # blank = True - opcional
    important = models.BooleanField(default = False)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self) -> str: # esta func es para que en la lista de tareas me ponga el titulo y no object
        return self.title + ' - by ' + self.user.username

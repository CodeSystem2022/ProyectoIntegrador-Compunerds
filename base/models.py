from django.db import models
#Implementamos un modelo de User con tablas predetermindas en Django
#(nombre de usuario, email, password, etc..)
from django.contrib.auth.models import User 

# Create your models here.

#Modelo de Dominio para las Task
class Task(models.Model):
    user = models.ForeignKey( #Aplicamos relación uno a muchos, dado que un usuario podrá tener varias Task
            User, on_delete=models.CASCADE, null=True, blank=True) #Configuramos para en el caso que se desee eliminar un usuario, quede registro de sus Task. 
    title=models.CharField(max_length=200)
    description=models.TextField(null=True, blank=True)
    complete=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    #Metadatos para establecer el orden por estado.
    class Meta:
        ordering=['complete']

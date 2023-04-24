from django.db import models

# Create your models here.
class Usuario(models.Model):
    nome: models.CharField(max_length=30)
    cargo: models.CharField(max_length=30)
    matricula: models.DecimalField(max_digits=50,decimal_places=2)
    setor: models.CharField(max_length=30)
    email: models.CharField(max_length=100)

    def __str__(self):
        return  self.nome

class  Events(models.Model):
    id = models.AutoField(primary_key=True)
    name =  models.CharField(max_length=255,null=True,blank=True)
    start =  models.DateTimeField(null=True,blank=True)
    end = models.DateTimeField(null=True,blank=True)

    class Meta:
        db_table =  "tblevents"
from django.db import models

from django.db.models import signals
from django.template.defaultfilters import slugify

# Create your models here.
from django.db import models

class Dados(models.Model):
    Matricula = models.CharField(max_length=11, null=True)
    Nome = models.CharField(max_length=100, null=True)
    Coluna1 = models.CharField(max_length=100, null=True)
    AdmissaoData = models.CharField(max_length=45, null=True)
    Login = models.CharField(max_length=45, null=True)
    Cpf = models.IntegerField(null=True)
    Email = models.CharField(max_length=200, null=True)
    NascimentoData = models.DateTimeField(null=True)
    Cargo = models.CharField(max_length=100, null=True)
    CargoCodigo = models.CharField(max_length=45, null=True)
    SalarioRef = models.CharField(max_length=25, null=True)
    Funcao = models.CharField(max_length=100, null=True)
    FuncaoCodigo = models.CharField(max_length=45, null=True)
    FuncaoRef = models.CharField(max_length=45, null=True)
    UA = models.CharField(max_length=45, null=True)
    LotacaoCod = models.CharField(max_length=20, null=True)
    LotacaoDesc = models.CharField(max_length=100, null=True)
    LotacaoSigla = models.CharField(max_length=10, null=True)
    Status = models.CharField(max_length=45, null=True)
    Data_afastamento = models.DateTimeField(null=True)
    AfastamentoMotivo = models.CharField(max_length=100, null=True)
    PDV = models.IntegerField(null=True)
    Sexo = models.CharField(max_length=45, null=True)
    Data_desligamento = models.CharField(max_length=16, null=True)
    Desligado = models.IntegerField(null=True)
    Ferias_inicio = models.DateTimeField(null=True)
    Ferias_fim = models.DateTimeField(null=True)
    Abono = models.DateTimeField(null=True)
    #slug = models.SlugField('Slug', max_length=100,blank=True,editable=False)

    class Meta:
        managed = False
        db_table = 'dados'

#def dados_pre_save(signal, instance, sender, **kwargs):
#    instance.slug = slugify(instance.Nome)

#signals.pre_save.connect(dados_pre_save, sender=Dados)
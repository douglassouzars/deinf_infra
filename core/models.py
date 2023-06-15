from django.db import models

from django.db.models import signals
from django.template.defaultfilters import slugify


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

class Cadastro(models.Model):
    Nome = models.CharField(max_length=100, null=False, default='')
    TelefoneFixo = models.CharField(max_length=20, null=True)
    TelefoneCelular = models.CharField(max_length=20, null=False, default='')
    TelefoneContato = models.CharField(max_length=20, null=True)
    Endereco = models.CharField(max_length=100, null=False, default='')
    Cep = models.CharField(max_length=10, null=False, default='')
    Tipodemoradia = models.CharField(max_length=50, null=True, default='')
    Outros = models.CharField(max_length=100, null=True)
    Email = models.EmailField(max_length=254, null=False, default='')
    RC = models.CharField(max_length=20, null=True)
    TipoSanguineo = models.CharField(max_length=5, null=True)
    DoadordeSangue = models.BooleanField(null=True)
    Portador = models.BooleanField(null=True )
    DataNascimento = models.DateField( null=False,default=None)
    Naturalidade = models.CharField(max_length=50, null=False, default='')
    EstadoCivil = models.CharField(max_length=20, null=False, default='')
    Grau = models.CharField(max_length=20, null=False, default='')
    NomeConjuge = models.CharField(max_length=100, null=True)
    GrauConjuge = models.CharField(max_length=20, null=True)
    NomePai = models.CharField(max_length=100, null=True)
    NomeMae = models.CharField( max_length=100, null=True)
    CPF = models.CharField(max_length=14, null= False, default='')
    RG = models.CharField(max_length=20, null= False, default='')
    Emissor = models.CharField(max_length=20, null= False, default='')
    DataCPF = models.DateField(null= False, default=None)
    Reservista = models.CharField(max_length=20, null=True)
    SerieReservista = models.CharField(max_length=20, null=True)
    Categoria = models.CharField(max_length=20, null=True)
    RegMilitar = models.CharField(max_length=20, null=True)
    Orgao = models.CharField(max_length=20, null=True)
    DataReservista = models.DateField(null=True)
    Titulo = models.CharField(max_length=20, null=True)
    Secao = models.CharField(max_length=20, null=True)
    Zona = models.CharField(max_length=20, null=True)
    LocalEmissao = models.CharField(max_length=50, null=True)
    DataTitulo = models.DateField(null=True)
    CTPS = models.CharField(max_length=20,null= False, default='')
    CTPSSerie = models.CharField(max_length=20, null= False, default='')
    CTPSUF = models.CharField(max_length=20, null= False, default='')
    DataCTPS = models.DateField(null= False, default=None)
    Registro = models.CharField(max_length=20, null=True)
    RegistroEmissor = models.CharField(max_length=20, null=True)
    RegistroUF = models.CharField(max_length=20, null=True)
    DataRegistro = models.DateField(null=True)
    Pis = models.CharField(max_length=20, null= False, default='')
    DataPIS = models.DateField(null=True)
    DependentesPIS = models.CharField(max_length=20, null=True)
    Cartorio = models.CharField(max_length=100, null=True)
    Livro = models.CharField(max_length=100, null=True)
    Folha = models.CharField(max_length=100, null=True)
    LocalEmissaoCartorio = models.CharField(max_length=100, null=True)
    Banco = models.CharField(max_length=100, null=True)
    Agencia = models.CharField(max_length=100, null=True)
    ContaCorrente = models.CharField( max_length=100, null=True)
    EmpregadoDeOutroOrgao = models.BooleanField(null=True)
    CategoriaDoOrgaoOrigem = models.BooleanField(null= True)
    AuxilioCreche = models.BooleanField("AuxilioCreche",null= True, default=False)
    ValeTransporte = models.BooleanField("ValeTransporte",null= True, default=False)
    ValeCombustivel = models.BooleanField("ValeCombustivel",null= True, default=False)
    PlanoDeSaude = models.BooleanField("PlanoDeSaude",null= True, default=False)
    ValeAlimentacao = models.BooleanField(null= True)

    class Meta:
        managed = False
        db_table = 'cadastro'

    def __str__(self):
        return self.nome
#def dados_pre_save(signal, instance, sender, **kwargs):
#    instance.slug = slugify(instance.Nome)

#signals.pre_save.connect(dados_pre_save, sender=Dados)
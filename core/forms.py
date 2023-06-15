from django import forms
from django.core.mail.message import EmailMessage
import re
from .models import Cadastro

class CadastroForm(forms.ModelForm):
    Nome = forms.CharField(label="Nome", max_length=100, required=True)
    TelefoneFixo = forms.CharField(label="Telefone Fixo", max_length=20, required=False)
    TelefoneCelular = forms.CharField(label="Telefone Celular", max_length=20, required=True)
    TelefoneContato = forms.CharField(label="Telefone de Contato", max_length=20, required=False)
    Endereco = forms.CharField(label="Endereço", max_length=100, required=True)
    Cep = forms.CharField(label="CEP", max_length=10, required=True)
    Tipodemoradia = forms.CharField(label="Tipo de Moradia", max_length=50, required=False)
    Outros = forms.CharField(label="Outros", max_length=100, required=False)
    Email = forms.EmailField(label="Email", max_length=254, required=True)
    RC = forms.CharField(label="RC", max_length=20, required=False)
    TipoSanguineo = forms.CharField(label="Tipo Sanguíneo", max_length=5, required=False)
    DoadordeSangue = forms.BooleanField(label="Doador de Sangue", required=False)
    Portador = forms.BooleanField(label="Portador", required=False)
    DataNascimento = forms.DateField(label="Data de Nascimento", required=True)
    Naturalidade = forms.CharField(label="Naturalidade", max_length=50, required=True)
    EstadoCivil = forms.CharField(label="Estado Civil", max_length=20, required=True)
    Grau = forms.CharField(label="Grau", max_length=20, required=True)
    NomeConjuge = forms.CharField(label="Nome do Cônjuge", max_length=100, required=False)
    GrauConjuge = forms.CharField(label="Grau do Cônjuge", max_length=20, required=False)
    NomePai = forms.CharField(label="Nome do Pai", max_length=100,required=False)
    NomeMae = forms.CharField(label="Nome da Mãe", max_length=100,required=False)
    CPF = forms.CharField(label="CPF", max_length=14, required=True)
    RG = forms.CharField(label="RG", max_length=20, required=True)
    Emissor = forms.CharField(label="Emissor", max_length=20, required=True)
    DataCPF = forms.DateField(label="Data do CPF", required=True)
    Reservista = forms.CharField(label="Reservista", max_length=20,required=False)
    SerieReservista = forms.CharField(label="Série da Reservista", max_length=20,required=False)
    Categoria = forms.CharField(label="Categoria", max_length=20,required=False)
    RegMilitar = forms.CharField(label="Registro Militar", max_length=20,required=False)
    Orgao = forms.CharField(label="Órgão", max_length=20,required=False)
    DataReservista = forms.DateField(label="Data da Reservista",required=False)
    Titulo = forms.CharField(label="Título", max_length=20,required=False)
    Secao = forms.CharField(label="Seção", max_length=20,required=False)
    Zona = forms.CharField(label="Zona", max_length=20,required=False)
    LocalEmissao = forms.CharField(label="Local de Emissão", max_length=50,required=False)
    LocalEmissao = forms.CharField(label="Local de Emissão", max_length=50,required=False)
    DataTitulo = forms.DateField(label="Data do Título",required=False)
    CTPS = forms.CharField(label="CTPS", max_length=20, required=True)
    CTPSSerie = forms.CharField(label="Série da CTPS", max_length=20, required=True)
    CTPSUF = forms.CharField(label="UF da CTPS", max_length=20, required=True)
    DataCTPS = forms.DateField(label="Data da CTPS", required=True)
    Registro = forms.CharField(label="Registro", max_length=20,required=False)
    RegistroEmissor = forms.CharField(label="Emissor do Registro", max_length=20,required=False)
    RegistroUF = forms.CharField(label="UF do Registro", max_length=20,required=False)
    DataRegistro = forms.DateField(label="Data do Registro",required=False)
    Pis = forms.CharField(label="PIS", max_length=20, required=True)
    DataPIS = forms.DateField(label="Data do PIS",required=False)
    DependentesPIS = forms.CharField(label="Dependentes do PIS", max_length=20,required=False)
    Cartorio = forms.CharField(label="Cartório", max_length=100,required=False)
    Livro = forms.CharField(label="Livro", max_length=100,required=False)
    Folha = forms.CharField(label="Folha", max_length=100,required=False)
    LocalEmissaoCartorio = forms.CharField(label="Local de Emissão do Cartório", max_length=100,required=False)
    Banco = forms.CharField(label="Banco", max_length=100,required=False)
    Agencia = forms.CharField(label="Agência", max_length=100,required=False)
    ContaCorrente = forms.CharField(label="Conta Corrente", max_length=100,required=False)
    EmpregadoDeOutroOrgao = forms.BooleanField(label="Empregado de Outro Orgao", required=False)
    CategoriaDoOrgaoOrigem = forms.BooleanField(label="Categoria do Órgão de Origem",required=False)
    AuxilioCreche = forms.BooleanField(label="Auxílio Creche", required=False)
    ValeTransporte = forms.BooleanField(label="Vale Transporte", required=False)
    ValeCombustivel = forms.BooleanField(label="Vale Combustível", required=False)
    PlanoDeSaude = forms.BooleanField(label="Plano de Saúde", required=False)
    ValeAlimentacao = forms.BooleanField(label="Vale Alimentação", required=False)

    def clean_TelefoneFixo(self):
        TelefoneFixo = self.cleaned_data.get('TelefoneFixo','')
        TelefoneFixo = re.sub(r'\D','', TelefoneFixo)  # remove caracteres não numéricos
        return TelefoneFixo
    def clean_TelefoneCelular(self):
        TelefoneCelular = self.cleaned_data.get('TelefoneCelular','')
        TelefoneCelular = re.sub(r'\D','', TelefoneCelular)  # remove caracteres não numéricos
        return TelefoneCelular

    def clean_TelefoneContato(self):
        TelefoneContato = self.cleaned_data.get('TelefoneContato', '')
        TelefoneContato = re.sub(r'\D', '', TelefoneContato)  # remove caracteres não numéricos
        return TelefoneContato

    def clean_Cep(self):
        Cep = self.cleaned_data.get('Cep', '')
        Cep = re.sub(r'\D', '', Cep)  # remove caracteres não numéricos
        return Cep

    def clean_CPF(self):
        CPF = self.cleaned_data.get('CPF', '')
        CPF = re.sub(r'\D', '', CPF)  # remove caracteres não numéricos
        return CPF

    def clean_RG(self):
        RG = self.cleaned_data.get('RG', '')
        RG = re.sub(r'\D', '', RG)  # remove caracteres não numéricos
        return RG

    def clean_Reservista(self):
        Reservista = self.cleaned_data.get('Reservista', '')
        Reservista = re.sub(r'\D', '', Reservista)  # remove caracteres não numéricos
        return Reservista

    def clean_SerieReservista(self):
        SerieReservista = self.cleaned_data.get('SerieReservista', '')
        SerieReservista = re.sub(r'\D', '', SerieReservista)  # remove caracteres não numéricos
        return SerieReservista

    def clean_RegMilitar(self):
        RegMilitar = self.cleaned_data.get('RegMilitar', '')
        RegMilitar = re.sub(r'\D', '', RegMilitar)  # remove caracteres não numéricos
        return RegMilitar

    def clean_Secao(self):
        Secao = self.cleaned_data.get('Secao', '')
        Secao = re.sub(r'\D', '', Secao)  # remove caracteres não numéricos
        return Secao

    def clean_Zona(self):
        Zona = self.cleaned_data.get('Zona', '')
        Zona = re.sub(r'\D', '', Zona)  # remove caracteres não numéricos
        return Zona

    def clean_CTPS(self):
        CTPS = self.cleaned_data.get('CTPS', '')
        CTPS = re.sub(r'\D', '', CTPS)  # remove caracteres não numéricos
        return CTPS

    def clean_CTPSSerie(self):
        CTPSSerie = self.cleaned_data.get('CTPSSerie', '')
        CTPSSerie = re.sub(r'\D', '', CTPSSerie)  # remove caracteres não numéricos
        return CTPSSerie

    def clean_Registro(self):
        Registro = self.cleaned_data.get('Registro', '')
        Registro = re.sub(r'\D', '', Registro)  # remove caracteres não numéricos
        return Registro

    def clean_PIS(self):
        PIS = self.cleaned_data.get('PIS', '')
        PIS = re.sub(r'\D', '', PIS)  # remove caracteres não numéricos
        return PIS

    def clean_Livro(self):
        Livro = self.cleaned_data.get('Livro', '')
        Livro = re.sub(r'\D', '', Livro)  # remove caracteres não numéricos
        return Livro

    def clean_Folha(self):
        Folha = self.cleaned_data.get('Folha', '')
        Folha = re.sub(r'\D', '', Folha)  # remove caracteres não numéricos
        return Folha

    def clean_Agencia(self):
        Agencia = self.cleaned_data.get('Agencia', '')
        Agencia = re.sub(r'\D', '', Agencia)  # remove caracteres não numéricos
        return Agencia

    def clean_ContaCorrente(self):
        ContaCorrente = self.cleaned_data.get('ContaCorrente', '')
        ContaCorrente = re.sub(r'\D', '', ContaCorrente)  # remove caracteres não numéricos
        return ContaCorrente
    class Meta:
        model = Cadastro
        fields ='__all__'

    """def send_mail(self):
        Nome = self.cleaned_data['Nome']
        TelefoneFixo = self.cleaned_data['TelefoneFixo']
        TelefoneCelular = self.cleaned_data['TelefoneCelular']
        TelefoneContato = self.cleaned_data['TelefoneContato']
        Endereco = self.cleaned_data['Endereco']
        Cep = self.cleaned_data['Cep']
        Tipodemoradia = self.cleaned_data['Tipodemoradia']
        Outros = self.cleaned_data['Outros']
        Email = self.cleaned_data['Email']
        RC = self.cleaned_data['RC']
        TipoSanguineo = self.cleaned_data['TipoSanguineo']
        DoadordeSangue = self.cleaned_data['DoadordeSangue']
        Portador = self.cleaned_data['Portador']
        DataNascimento = self.cleaned_data['DataNascimento']
        Naturalidade = self.cleaned_data['Naturalidade']
        EstadoCivil = self.cleaned_data['EstadoCivil']
        Grau = self.cleaned_data['Grau']
        NomeConjuge = self.cleaned_data['NomeConjuge']
        GrauConjuge = self.cleaned_data['GrauConjuge']
        NomePai = self.cleaned_data['NomePai']
        NomeMae = self.cleaned_data['NomeMae']
        CPF = self.cleaned_data['CPF']
        RG = self.cleaned_data['RG']
        Emissor = self.cleaned_data['Emissor']
        DataCPF = self.cleaned_data['DataCPF']
        Reservista = self.cleaned_data['Reservista']
        SerieReservista = self.cleaned_data['SerieReservista']
        Categoria = self.cleaned_data['Categoria']
        RegMilitar = self.cleaned_data['RegMilitar']
        Orgao = self.cleaned_data['Orgao']
        DataReservista = self.cleaned_data['DataReservista']
        Titulo = self.cleaned_data['Titulo']
        Secao = self.cleaned_data['Secao']
        Zona = self.cleaned_data['Zona']
        LocalEmissao = self.cleaned_data['LocalEmissao']
        DataTitulo = self.cleaned_data['DataTitulo']
        CTPS = self.cleaned_data['CTPS']
        CTPSSerie = self.cleaned_data['CTPSSerie']
        CTPSUF = self.cleaned_data['CTPSUF']
        DataCTPS = self.cleaned_data['DataCTPS']
        Registro = self.cleaned_data['Registro']
        RegistroEmissor = self.cleaned_data['RegistroEmissor']
        RegistroUF = self.cleaned_data['RegistroUF']
        DataRegistro = self.cleaned_data['DataRegistro']
        Pis = self.cleaned_data['PIS']
        DataPIS = self.cleaned_data['DataPIS']
        DependentesPIS = self.cleaned_data['DependentesPIS']
        Cartorio = self.cleaned_data['Cartorio']
        Livro = self.cleaned_data['Livro']
        Folha = self.cleaned_data['Folha']
        LocalEmissaoCartorio = self.cleaned_data['LocalEmissaoCartorio']
        Banco = self.cleaned_data['Banco']
        Agencia = self.cleaned_data['Agencia']
        ContaCorrente = self.cleaned_data['ContaCorrente']
        EmpregadoDeOutroOrgao = self.cleaned_data['EmpregadoDeOutroOrgao']
        CategoriaDoOrgaoOrigem = self.cleaned_data['CategoriaDoOrgaoOrigem']
        AuxilioCreche = self.cleaned_data['AuxilioCreche']
        ValeTransporte = self.cleaned_data['ValeTransporte']
        ValeCombustivel = self.cleaned_data['ValeCombustivel']
        PlanoDeSaude = self.cleaned_data['PlanoDeSaude']
        ValeAlimentacao = self.cleaned_data['ValeAlimentacao']


        conteudo = f'O Cadastro de {Nome} foi solicitado com Sucesso \n Essa mensagem é automatica e não necessita ser respondida'

        mail = EmailMessage(
            subject="Confirmação de Solicitação de cadastro!",
            bady=conteudo,
            from_email='douglassouza15.ds@gmail.com',
            to=[Email, ],
            #headers={'Reply-To': Email}

        )
        mail.send()





        """





        #OrgaoOrigem = self.cleaned_data['OrgaoOrigem']







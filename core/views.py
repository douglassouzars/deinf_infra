from pyad import *
from django.shortcuts import render, redirect
from django.contrib.auth import login , logout
import pythoncom
from django.db import models
import pyad.adquery
import requests
from django.http import JsonResponse
import ldap
from core.ldap_backend import LDAPBackend, CustomAccessMixin
from django.conf import settings
from django.http import HttpResponse
from .models import Dados
from .forms import CadastroForm, MapeamentoForm
import ldap3

from django.views.generic import TemplateView, CreateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from core.models import Cadastro, Mapeamento
from datetime import datetime

def variavel():
    bound=False

class LoginView(TemplateView):
    template_name = 'login.html'
    #def login(request):
     #   return render(request, '/accounts/login.html')

def loadlogin(request):
    try:
        bound = request.session.get('bound')  # Retrieve the 'bound' value from the session
        if request.method == 'POST':
            username = request.POST['nome']
            password = request.POST['senha']
            request.session['nome'] = username
            ldap = LDAPBackend()
            bound = ldap.authenticate(request, username, password)


            if bound is True:

                request.session['bound'] = bound
                return redirect('/index/')  # Pass 'bound' as a parameter to the index view
            else:
                return redirect('/')
        if request.POST.get('action') == 'Cadastrar':
            if bound is True:
                # Renderiza a página de cadastro
                return render(request, 'cadastro.html')
            else:
                return redirect('/')
    except Exception as e:
        bound = False
        return redirect('/')

    return bound

def logouts(request):
    try:
        bound = request.session.get('bound')  # Retrieve the 'bound' value from the session

        if bound is True:
            if request.method == 'POST':
                # Remova as informações de autenticação da sessão do usuário
                if 'nome' in request.session:
                    del request.session['nome']
                    del request.session['bound']
                # Fecha a conexão LDAP
                ldap = LDAPBackend()
                ldap.close_connection(request)
                # Redireciona o usuário para a página inicial
                return redirect('/')
        # Se a solicitação não for do tipo POST, redireciona o usuário de volta para a página index

    except:
        return redirect('/index/')






        """ldap.set_option(ldap.OPT_REFERRALS, 0)
        ldap.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        ldap.set_option(ldap.OPT_SIZELIMIT, 0)
        conn = ldap.initialize('ldap://SRVDOUGLAS')
        conn.simple_bind_s("douglas.souza@DOUGLAS.TESTE", '!@#45678qwe')
        base_dn = 'OU=USUARIOS,OU=ACCOUNT,OU=ACCOUNT AND GROUPS,DC=DOUGLAS,DC=TESTE'
        filter_str = f"(sAMAccountName='{name}')"
        attributes = ['cn', 'mail', 'description']
        conn.search(search_base=base_dn, search_filter=filter_str, search_scope=SUBTREE, attributes=attributes)
        print("ai")"""
        #user3 = pyad.adsearch.ADQuery()
        #user3.execute_query(
        #    attributes=["cn", "mail", "description","sn","objectCategory","userAccountControl", "displayName","memberOf","distinguishedName", "title","department" ], where_clause=f"SamAccountName = '{name}'",
        #    base_dn="OU=USUARIOS,OU=ACCOUNT,OU=ACCOUNT AND GROUPS,DC=DOUGLAS,DC=TESTE"
        #)

#funciona
def index(request):
    bound = request.session.get('bound')  # Retrieve the 'bound' value from the session

    if bound is True:
        pythoncom.CoInitialize()
        name = request.session.get('nome')

        server = 'ldap://SRVDOUGLAS'
        username = 'conexao_ldap@DOUGLAS.TESTE'
        password = '@teste159'
        base_dn = 'OU=USUARIOS,OU=ACCOUNT,OU=ACCOUNT AND GROUPS,DC=DOUGLAS,DC=TESTE'

        ldap.set_option(ldap.OPT_REFERRALS, 0)
        ldap.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        ldap.set_option(ldap.OPT_SIZELIMIT, 0)

        conn = ldap.initialize(server)
        conn.simple_bind_s(username,password)
        name = request.session.get('nome')

        if name.isdigit():
            search_filter = f"sAMAccountName={name}"
        else:
            search_filter = f"userPrincipalName={name}@DOUGLAS.TESTE"
        #search_filter = f"userPrincipalName={name}@DOUGLAS.TESTE"
        attributes = ['cn', 'mail', 'description', 'sn', 'objectCategory', 'userAccountControl', 'displayName',
                      'memberOf', 'title', 'department']

        results = conn.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter, attributes)

        for dn, entry in results:
            context = {}
            context['cn'] = entry.get('cn', [b''])[0].decode()
            context['mail'] = entry.get('mail', [b''])[0].decode()
            context['descricao'] = entry.get('description', [b''])[0].decode()
            context['sn'] = entry.get('sn', [b''])[0].decode()
            context['objc'] = entry.get('objectCategory', [b''])[0].decode()
            context['objc2'] = entry.get('userAccountControl', [b''])[0].decode()
            context['dis'] = entry.get('displayName', [b''])[0].decode()
            context['m'] = entry.get('memberOf', [b''])[0].decode()
            context['title'] = entry.get('title', [b''])[0].decode()
            context['dep'] = entry.get('department', [b''])[0].decode()

            dados = Dados.objects.filter(Login=name)
            for dado in dados:
                pass
                #diferenca = (dado.Ferias_fim - dado.Ferias_inicio).days
                #dado.diferenca = diferenca
            context2 = {
                'dados': dados
            }
            context.update(context2)
            bound = True
            return render(request, 'index.html', context)
        else:
            return redirect('/')
        return bound



from .forms import CadastroForm


def cadastro(request):
    bound = request.session.get('bound')  # Retrieve the 'bound' value from the session
    if bound is True:
        return render(request, 'cadastro.html')
    else:
        return redirect('/')

import urllib.parse
import re



import json
from django.http import HttpResponseServerError

import ldap
from ldap import modlist
from django.http import HttpResponseServerError
from django.http import HttpResponseBadRequest, HttpResponseServerError

def get_subchefe(request):
    if request.method == 'GET':
        cn = request.GET.get('cn')
        try:
            mapeamento = Mapeamento.objects.get(cn=cn)
            subchefe = mapeamento.subchefe
            return JsonResponse({'subchefe': subchefe})
        except Mapeamento.DoesNotExist:
            return JsonResponse({'subchefe': False})
def atualizar_mapeamento(request):
    if request.method == 'POST':
        cn = request.POST.get('cn')
        checked = request.POST.get('checked')


        # Criar ou atualizar o registro na tabela Mapeamento


        mapeamento, created = Mapeamento.objects.get_or_create(cn=cn)
        mapeamento.subchefe = checked == 'true'
        mapeamento.save()

        return HttpResponse("Valores salvos com sucesso.")



    return HttpResponse("Método de requisição inválido.")




def remover_usuario(request):

    if request.method == 'POST':
        username = request.POST.get('user')  # Obter o nome de usuário enviado na requisição
        selected_group = request.session.get('group')

        try:
            password = '@teste159'
            server_url = 'ldap://SRVDOUGLAS'
            bind_dn = 'conexao_ldap@DOUGLAS.TESTE'
            group_cn2 = f'GGRP_USERS_{selected_group}_READ'
            base_dn = 'OU=FILE SERVER,OU=GROUPS,OU=ACCOUNT AND GROUPS,DC=DOUGLAS,DC=TESTE'  # Base DN onde o grupo está localizado

            # Conectar e autenticar no servidor LDAP
            conn = ldap.initialize(server_url)
            conn.simple_bind_s(bind_dn, password)

            # Realizar a pesquisa para obter o DN completo do grupo com base no CN
            group_cn = group_cn2
            group_filter = f"(CN={group_cn})"
            group_results = conn.search_s(base_dn, ldap.SCOPE_SUBTREE, group_filter)

            if group_results:
                group_dn = group_results[0][0]  # Obter o DN do grupo encontrado
                member_dn = f"CN={username},OU=USUARIOS,OU=ACCOUNT,OU=ACCOUNT AND GROUPS,DC=DOUGLAS,DC=TESTE"  # DN do usuário a ser removido
                mod_attrs = [
                    (ldap.MOD_DELETE, 'member', member_dn.encode('utf-8'))  # Remover o usuário do grupo
                ]
                conn.modify_s(group_dn, mod_attrs)

                return HttpResponse('Usuário removido do grupo com sucesso')
            else:
                return HttpResponseServerError('Grupo não encontrado')

        except ldap.LDAPError as e:
            return HttpResponseServerError('Erro ao remover o usuário do grupo: ' + str(e))

    return HttpResponseBadRequest('Método de requisição inválido')


def adicionar_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('user')  # Obter o nome de usuário enviado na requisição


        selected_group = request.session.get('group')

        print("entrou1")
        select_dep = request.session.get('departamento')
        print(select_dep)
        input_string = select_dep
        components = input_string.split('/')
        components.reverse()
        output_string = ','.join([f'OU={component}' for component in components])
        print(output_string)
            
        password = '@teste159'
        server_url = 'ldap://SRVDOUGLAS'
        bind_dn = 'conexao_ldap@DOUGLAS.TESTE'
        group_cn2 = f'GGRP_USERS_{selected_group}_READ'


            # Conectar e autenticar no servidor LDAP
        conn = ldap.initialize(server_url)
        conn.simple_bind_s(bind_dn, password)

        base_dn = f'{output_string},OU=FILE SERVER,OU=GROUPS,OU=ACCOUNT AND GROUPS,DC=DOUGLAS,DC=TESTE'
        group_cn = group_cn2
        group_filter = f"(CN={group_cn})"
        group_results = conn.search_s(base_dn, ldap.SCOPE_SUBTREE, group_filter)


        if group_results:
            print(group_results)
            group_dn = group_results[0][0]  # Obter o DN do grupo encontrado
            print(group_dn)
            member_dn = f"CN={username},OU=USUARIOS,OU=ACCOUNT,OU=ACCOUNT AND GROUPS,DC=DOUGLAS,DC=TESTE"  # DN do usuário a ser adicionado
            print(member_dn)
            mod_attrs = [
                (ldap.MOD_ADD, 'member', member_dn.encode('utf-8'))  # Adicionar o usuário como membro do grupo
            ]
            conn.modify_s(group_dn, mod_attrs)


            return HttpResponse('Usuário adicionado ao grupo com sucesso')
        else:
                return HttpResponseServerError('Grupo não encontrado')



    return HttpResponseBadRequest('Método de requisição inválido')



def add_user_to_group(request):
    if request.method == 'POST':
        user = request.POST.get('user')  # Obtém o nome do usuário do POST
        selected_group = request.GET.get('group')  # Obtém o grupo selecionado do POST

        server = 'ldap://SRVDOUGLAS'
        username = 'conexao_ldap@DOUGLAS.TESTE'
        password = '@teste159'
        base_dn = 'OU=FILE SERVER,OU=GRUPOS,OU=ACCOUNT,OU=ACCOUNT AND GROUPS,DC=DOUGLAS,DC=TESTE'

        conn = ldap.initialize(server)
        conn.simple_bind_s(username, password)

        user_dn = f'CN={user},{base_dn}'
        group_cn = f'GGRP_USERS_{selected_group}_READ'
        group_dn = f'CN={group_cn},{base_dn}'
        print(user_dn)
        print(group_cn)
        print(group_dn)
        mod_attrs = [(ldap.MOD_ADD, 'member', user_dn)]
        conn.modify_s(group_dn, mod_attrs)

        return HttpResponse('Usuário adicionado ao grupo com sucesso.')

    return HttpResponse('Método de requisição inválido.')
def get_all_users(request):

    server = 'ldap://SRVDOUGLAS'
    username = 'conexao_ldap@DOUGLAS.TESTE'
    password = '@teste159'
    base_dn = 'OU=USUARIOS,OU=ACCOUNT,OU=ACCOUNT AND GROUPS,DC=DOUGLAS,DC=TESTE'

    conn = ldap.initialize(server)
    conn.simple_bind_s(username, password)

    search_filter = '(objectClass=user)'
    attributes = ['cn']

    results = conn.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter, attributes)
    print(results)
    users = []
    for dn, entry in results:
        user = {}
        user['cn'] = entry.get('cn', [b''])[0].decode('utf-8', errors='ignore')
        users.append(user)
    print(dn)
    print(entry)
    response_data = {
        'users': users
    }

    return HttpResponse(json.dumps(response_data), content_type='application/json')


def get_users_from_group(request):
    selected_group = request.GET.get('selected_group')  # Obtém o grupo selecionado do request.GET
    if selected_group == 'Selecione uma pasta...':
        selected_group = None
    print(selected_group)
    request.session['group'] = selected_group

    group_cn2 = f'GGRP_USERS_{selected_group}_READ'
    group_cn = group_cn2
    group_filter = f"(cn={group_cn})"

    server = 'ldap://SRVDOUGLAS'
    username = 'conexao_ldap@DOUGLAS.TESTE'
    password = '@teste159'
    base_dn = 'OU=FILE SERVER,OU=GROUPS,OU=ACCOUNT AND GROUPS,DC=DOUGLAS,DC=TESTE'
    group_attributes = ['member']

    ldap.set_option(ldap.OPT_REFERRALS, 0)
    ldap.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
    ldap.set_option(ldap.OPT_SIZELIMIT, 0)

    conn = ldap.initialize(server)
    conn.simple_bind_s(username, password)

    group_results = conn.search_s(base_dn, ldap.SCOPE_SUBTREE, group_filter, group_attributes)

    if group_results:
        group_entry = group_results[0][1]

        members = group_entry.get('member', [])
        padrao = r"CN=(.*?),OU=USUARIOS"
        cn_list = []
        for member in members:
            member_dn = member.decode('utf-8')
            matches = re.findall(padrao, member_dn)

            if matches:
                cn = matches[0]
                cn_list.append(cn)

        response_data = {
            'cn_list': cn_list,
            'selected_group': selected_group,
        }

        return HttpResponse(json.dumps(response_data), content_type='application/json')

    # Converter members para lista de strings


from django.db.models import Q

#members = get_users_from_group(selecionado)

def mapeamento(request):
    bound = request.session.get('bound')  # Retrieve the 'bound' value from the session

    if bound is True:
        pythoncom.CoInitialize()
        name = request.session.get('nome')
        server = 'ldap://SRVDOUGLAS'
        username = 'conexao_ldap@DOUGLAS.TESTE'
        password = '@teste159'
        base_dn = 'OU=USUARIOS,OU=ACCOUNT,OU=ACCOUNT AND GROUPS,DC=DOUGLAS,DC=TESTE'
        ldap.set_option(ldap.OPT_REFERRALS, 0)
        ldap.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        ldap.set_option(ldap.OPT_SIZELIMIT, 0)
        conn = ldap.initialize(server)
        conn.simple_bind_s(username, password)
        name = request.session.get('nome')
        if name.isdigit():
            search_filter = f"sAMAccountName={name}"
        else:
            search_filter = f"userPrincipalName={name}@DOUGLAS.TESTE"
        attributes = ['cn', 'mail', 'description', 'sn', 'objectCategory', 'userAccountControl', 'displayName',
                      'memberOf', 'title', 'department']
        results = conn.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter, attributes)

        for dn, entry in results:
            context = {}
            context['cn'] = entry.get('cn', [b''])[0].decode()
            context['mail'] = entry.get('mail', [b''])[0].decode()
            context['descricao'] = entry.get('description', [b''])[0].decode()
            context['sn'] = entry.get('sn', [b''])[0].decode()
            context['objc'] = entry.get('objectCategory', [b''])[0].decode()
            context['objc2'] = entry.get('userAccountControl', [b''])[0].decode()
            context['dis'] = entry.get('displayName', [b''])[0].decode()
            context['m'] = entry.get('memberOf', [b''])[0].decode()
            context['title'] = entry.get('title', [b''])[0].decode()
            context['dep'] = entry.get('department', [b''])[0].decode()
            select_dep = context['dep']
            current_dn = context['m']

            components = current_dn.split(',')
            components = components[1:]
            base_dn_final = ','.join(components)

            result = conn.search_s(base_dn_final, ldap.SCOPE_SUBTREE, '(objectClass=group)')
            groups = [entry[1] for entry in result]

            unique_categories = set()
            for group in groups:
                group_name = group['cn'][0].decode('utf-8')
                # category = group_name.split("_")[2]  # Extrai o terceiro elemento separado por "_"
                category = "_".join(group_name.split("_")[2:]).replace("_READ", "").replace("_DELETE", "")

                unique_categories.add(category)

            context['groups_data'] = unique_categories
            dados = Dados.objects.filter(Login=name).values('Nome', 'CargoCodigo', 'FuncaoCodigo', 'LotacaoCod')
            dados2 = Dados.objects.filter(Login=name, FuncaoCodigo='1001')


            dados3 = Mapeamento.objects.filter(Q(subchefe='1') | Q(subchefe=False)).values('cn', 'subchefe')

            for dado in dados3:
                nome_completo = dado['cn']
                partes_nome = nome_completo.split(' ')
                primeiro_nome = partes_nome[0].lower()
                ultimo_nome = partes_nome[-1].lower()
                expressao = f"{primeiro_nome}.{ultimo_nome}"

                if name in expressao:

                    if name in expressao and (dado['subchefe'] == True):
                        dados = Dados.objects.filter(Login=name).values('Nome', 'CargoCodigo', 'FuncaoCodigo','LotacaoCod')
                        lotacao_cod = dados[0]['LotacaoCod']

                        context2 = {
                            'dados': dados
                        }

                        context.update(context2)
                        bound = True
                        return render(request, 'mapeamento.html', context)
                    else:
                        return redirect('/index/')


            request.session['departamento'] = select_dep
            if dados2.exists():
                dados = Dados.objects.filter(Login=name).values('Nome', 'CargoCodigo', 'FuncaoCodigo', 'LotacaoCod')
                lotacao_cod = dados[0]['LotacaoCod']

                context2 = {
                    'dados': dados
                }

                context.update(context2)
                bound = True
                return render(request, 'mapeamento.html', context)
                # Redirecionar para a página mapeamento.html se a FuncaoCodigo for igual a '001'

    else:
        # Redirecionar para a página index.html se a FuncaoCodigo não for igual a '001' ou subchefe não for igual a '1'
        return redirect('/index/')

    return bound


'''def mapeamento(request):
    bound = request.session.get('bound')  # Retrieve the 'bound' value from the session

    if bound is True:
        pythoncom.CoInitialize()
        name = request.session.get('nome')
        server = 'ldap://SRVDOUGLAS'
        username = 'conexao_ldap@DOUGLAS.TESTE'
        password = '@teste159'
        base_dn = 'OU=USUARIOS,OU=ACCOUNT,OU=ACCOUNT AND GROUPS,DC=DOUGLAS,DC=TESTE'
        ldap.set_option(ldap.OPT_REFERRALS, 0)
        ldap.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        ldap.set_option(ldap.OPT_SIZELIMIT, 0)
        conn = ldap.initialize(server)
        conn.simple_bind_s(username, password)
        name = request.session.get('nome')
        search_filter = f"sAMAccountName={name}"
        attributes = ['cn', 'mail', 'description', 'sn', 'objectCategory', 'userAccountControl', 'displayName',
                  'memberOf', 'title', 'department']
        results = conn.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter, attributes)

    for dn, entry in results:
        context = {}
        context['cn'] = entry.get('cn', [b''])[0].decode()
        context['mail'] = entry.get('mail', [b''])[0].decode()
        context['descricao'] = entry.get('description', [b''])[0].decode()
        context['sn'] = entry.get('sn', [b''])[0].decode()
        context['objc'] = entry.get('objectCategory', [b''])[0].decode()
        context['objc2'] = entry.get('userAccountControl', [b''])[0].decode()
        context['dis'] = entry.get('displayName', [b''])[0].decode()
        context['m'] = entry.get('memberOf', [b''])[0].decode()
        context['title'] = entry.get('title', [b''])[0].decode()
        context['dep'] = entry.get('department', [b''])[0].decode()
        select_dep = context['dep']
        current_dn = context['m']
        print("uiui",current_dn)
        components = current_dn.split(',')
        components = components[1:]
        base_dn_final = ','.join(components)
        print(base_dn_final)
        result = conn.search_s(base_dn_final, ldap.SCOPE_SUBTREE, '(objectClass=group)')
        groups = [entry[1] for entry in result]

        unique_categories = set()
        for group in groups:
            group_name = group['cn'][0].decode('utf-8')
            #category = group_name.split("_")[2]  # Extrai o terceiro elemento separado por "_"
            category = "_".join(group_name.split("_")[2:]).replace("_READ", "").replace("_DELETE", "")


            unique_categories.add(category)
        print(unique_categories)
        context['groups_data'] = unique_categories
        dados = Dados.objects.filter(Login=name).values('Nome', 'CargoCodigo', 'FuncaoCodigo', 'LotacaoCod')
        dados2 = Dados.objects.filter(Login=name, FuncaoCodigo='1001')
        dados3 = Mapeamento.objects.filter(subchefe='1')


        request.session['departamento'] = select_dep
        if dados2.exists() or dados3.exists():
            dados = Dados.objects.filter(Login=name).values('Nome', 'CargoCodigo', 'FuncaoCodigo', 'LotacaoCod')
            lotacao_cod = dados[0]['LotacaoCod']

            context2 = {
                'dados': dados
            }

            context.update(context2)
            bound = True
            return render(request, 'mapeamento.html', context)
            # Redirecionar para a página mapeamento.html se a FuncaoCodigo for igual a '001'

        else:
            # Redirecionar para a página index.html se a FuncaoCodigo não for igual a '001'
            return redirect('/index/')
        return bound'''

def loadcadastro(request):
        bound = request.session.get('bound')  # Retrieve the 'bound' value from the session

        if bound is True:

            form = CadastroForm(request.POST)
            # data = {}
            if request.method == 'POST':
                Nome = request.POST.get('Nome')
                TelefoneFixo = request.POST.get('TelefoneFixo')
                TelefoneCelular = request.POST.get('TelefoneCelular')
                TelefoneContato = request.POST.get('TelefoneContato')
                Endereco = request.POST.get('Endereco')
                Cep = request.POST.get('Cep')
                Tipodemoradia = request.POST.get('Tipodemoradia')
                Outros = request.POST.get('Outros')
                Email = request.POST.get('Email')
                RC = request.POST.get('RC')
                TipoSanguineo = request.POST.get('TipoSanguineo')
                DoadordeSangue = request.POST.get('DoadordeSangue')
                Portador = request.POST.get('Portador')
                DataNascimento = request.POST.get('DataNascimento')
                Naturalidade = request.POST.get('Naturalidade')
                EstadoCivil = request.POST.get('EstadoCivil')
                Grau = request.POST.get('Grau')
                NomeConjuge = request.POST.get('NomeConjuge')
                GrauConjuge = request.POST.get('GrauConjuge')
                NomePai = request.POST.get('NomePai')
                NomeMae = request.POST.get('NomeMae')
                CPF = request.POST.get('CPF')
                RG = request.POST.get('RG')
                Emissor = request.POST.get('Emissor')
                DataCPF = request.POST.get('DataCPF')
                Reservista = request.POST.get('Reservista')
                SerieReservista = request.POST.get('SerieReservista')
                Categoria = request.POST.get('Categoria')
                RegMilitar = request.POST.get('RegMilitar')
                Orgao = request.POST.get('Orgao')
                DataReservista = request.POST.get('DataReservista')
                Titulo = request.POST.get('Titulo')
                Secao = request.POST.get('Secao')
                Zona = request.POST.get('Zona')
                LocalEmissao = request.POST.get('LocalEmissao')
                DataTitulo = request.POST.get('DataTitulo')
                CTPS = request.POST.get('CTPS')
                CTPSSerie = request.POST.get('CTPSSerie')
                CTPSUF = request.POST.get('CTPSUF')
                DataCTPS = request.POST.get('DataCTPS')
                Registro = request.POST.get('Registro')
                RegistroEmissor = request.POST.get('RegistroEmissor')
                RegistroUF = request.POST.get('RegistroUF')
                DataRegistro = request.POST.get('DataRegistro')
                Pis = request.POST.get('Pis')
                DataPIS = request.POST.get('DataPIS')
                DependentesPIS = request.POST.get('DependentesPIS')
                Cartorio = request.POST.get('Cartorio')
                Livro = request.POST.get('Livro')
                Folha = request.POST.get('Folha')
                LocalEmissaoCartorio = request.POST.get('LocalEmissaoCartorio')
                Banco = request.POST.get('Banco')
                Agencia = request.POST.get('Agencia')
                ContaCorrente = request.POST.get('ContaCorrente')
                EmpregadoDeOutroOrgao = request.POST.get('EmpregadoDeOutroOrgao')
                CategoriaDoOrgaoOrigem = request.POST.get('CategoriaDoOrgaoOrigem')
                AuxilioCreche = request.POST.get('AuxilioCreche')
                ValeTransporte = request.POST.get('ValeTransporte')
                ValeCombustivel = request.POST.get('ValeCombustivel')
                PlanoDeSaude = request.POST.get('PlanoDeSaude')
                ValeAlimentacao = request.POST.get('ValeAlimentacao')
                auxilio_creche = request.POST.get('AuxilioCreche', False) == '1'
                vale_transporte = request.POST.get('ValeTransporte', False) == '1'
                vale_combustivel = request.POST.get('ValeCombustive', False) == '1'
                PlanoDeSaude = request.POST.get('PlanoDeSaude', False) == '1'
                vale_alimentacao = request.POST.get('ValeAlimentacao')
                Setor = request.POST.get('Setor')


                if form.is_valid():
                    if Tipodemoradia == 'Selecione um item...':
                        Tipodemoradia = None
                    else:
                        Tipodemoradia = Tipodemoradia
                    if DoadordeSangue == 'true':
                        DoadordeSangue = True
                    elif DoadordeSangue == 'false':
                        DoadordeSangue = False
                    else:
                        DoadordeSangue = None
                    if Portador == 'true':
                        Portador = True
                    elif Portador == 'false':
                        Portador = False
                    else:
                        Portador = None
                    if DataNascimento:
                        data_nascimento = datetime.strptime(DataNascimento, '%d/%m/%Y').strftime('%Y-%m-%d')
                    if DataCPF:
                        data_cpf = datetime.strptime(DataCPF, '%d/%m/%Y').strftime('%Y-%m-%d')
                    if DataReservista:
                        data_reservista = datetime.strptime(DataReservista, '%d/%m/%Y').strftime('%Y-%m-%d')
                    else:
                        data_reservista = None
                    if DataTitulo:
                        data_titulo = datetime.strptime(DataTitulo, '%d/%m/%Y').strftime('%Y-%m-%d')
                    else:
                        data_titulo = None
                    if DataCTPS:
                        data_ctps = datetime.strptime(DataCTPS, '%d/%m/%Y').strftime('%Y-%m-%d')
                    if DataRegistro:
                        data_registro = datetime.strptime(DataRegistro, '%d/%m/%Y').strftime('%Y-%m-%d')
                    else:
                        data_registro = None
                    if DataPIS:
                        data_pis = datetime.strptime(DataPIS, '%d/%m/%Y').strftime('%Y-%m-%d')
                    else:
                        data_pis = None
                    if EmpregadoDeOutroOrgao == 'false':
                        EmpregadoDeOutroOrgao = False
                    elif EmpregadoDeOutroOrgao == 'true':
                        EmpregadoDeOutroOrgao = True
                    else:
                        EmpregadoDeOutroOrgao = None
                    if ValeAlimentacao == 'false':
                        ValeAlimentacao = False
                    elif ValeAlimentacao == 'true':
                        ValeAlimentacao = True
                    else:
                        ValeAlimentacao = None
                    if AuxilioCreche is True:
                        AuxilioCreche = True
                    else:
                        AuxilioCreche = False
                    if ValeTransporte is True:
                        ValeTransporte = True
                    else:
                        ValeTransporte = False
                    if ValeCombustivel is True:
                        ValeCombustivel = True
                    else:
                        ValeCombustivel = False
                    if PlanoDeSaude is True:
                        PlanoDeSaude = True
                    else:
                        PlanoDeSaude = False
                    if Setor == 'Selecione um item...':
                        Setor = None
                    else:
                        Setor = Setor

                        # Salvar os valores no banco de dados
                    cadastro = Cadastro.objects.create(
                        Nome=Nome,
                        TelefoneFixo=TelefoneFixo,
                        TelefoneCelular=TelefoneCelular,
                        TelefoneContato=TelefoneContato,
                        Endereco=Endereco,
                        Cep=Cep,
                        Tipodemoradia=Tipodemoradia,
                        Outros=Outros,
                        Email=Email,
                        RC=RC,
                        TipoSanguineo=TipoSanguineo,
                        DoadordeSangue=DoadordeSangue,
                        Portador=Portador,
                        DataNascimento=data_nascimento,
                        Naturalidade=Naturalidade,
                        EstadoCivil=EstadoCivil,
                        Grau=Grau,
                        NomeConjuge=NomeConjuge,
                        GrauConjuge=GrauConjuge,
                        NomePai=NomePai,
                        NomeMae=NomeMae,
                        CPF=CPF,
                        RG=RG,
                        Emissor=Emissor,
                        DataCPF=data_cpf,
                        Reservista=Reservista,
                        SerieReservista=SerieReservista,
                        Categoria=Categoria,
                        RegMilitar=RegMilitar,
                        Orgao=Orgao,
                        DataReservista=data_reservista,
                        Titulo=Titulo,
                        Secao=Secao,
                        Zona=Zona,
                        LocalEmissao=LocalEmissao,
                        DataTitulo=data_titulo,
                        CTPS=CTPS,
                        CTPSSerie=CTPSSerie,
                        CTPSUF=CTPSUF,
                        DataCTPS=data_ctps,
                        Registro=Registro,
                        RegistroEmissor=RegistroEmissor,
                        RegistroUF=RegistroUF,
                        DataRegistro=data_registro,
                        Pis=Pis,
                        DataPIS=data_pis,
                        DependentesPIS=DependentesPIS,
                        Cartorio=Cartorio,
                        Livro=Livro,
                        Folha=Folha,
                        LocalEmissaoCartorio=LocalEmissaoCartorio,
                        Banco=Banco,
                        Agencia=Agencia,
                        ContaCorrente=ContaCorrente,
                        EmpregadoDeOutroOrgao=EmpregadoDeOutroOrgao,
                        CategoriaDoOrgaoOrigem=CategoriaDoOrgaoOrigem,
                        AuxilioCreche=AuxilioCreche,
                        ValeTransporte=ValeTransporte,
                        ValeCombustivel=ValeCombustivel,
                        PlanoDeSaude=PlanoDeSaude,
                        ValeAlimentacao=ValeAlimentacao,
                        Setor=Setor,
                    )
                    cadastro.save()


                    server = 'ldap://SRVDOUGLAS'
                    username = 'conexao_ldap@DOUGLAS.TESTE'
                    password = '@teste159'
                    base_dn = 'OU=USUARIOS,OU=ACCOUNT,OU=ACCOUNT AND GROUPS,DC=DOUGLAS,DC=TESTE'
                    ldap.set_option(ldap.OPT_REFERRALS, 0)
                    ldap.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
                    ldap.set_option(ldap.OPT_SIZELIMIT, 0)
                    conn = ldap.initialize(server)
                    conn.simple_bind_s(username, password)
                    Nome = request.POST.get('Nome')
                    CPF = request.POST.get('CPF')
                    Setor = request.POST.get('Setor')
                    name_parts = Nome.split()
                    first_name = name_parts[0]
                    last_name = name_parts[-1]
                    user_logon_name = "{}.{}".format(first_name.lower(), last_name.lower())
                    dn = f"CN={Nome},OU=USUARIOS,OU=ACCOUNT,OU=ACCOUNT AND GROUPS,DC=DOUGLAS,DC=TESTE"
                    cn = Nome
                    given_name = first_name
                    sn = last_name
                    display_name = Nome
                    user_logon_name_pre_win2000 = CPF
                    department = Setor
                    company = 'Novacap'
                    title = 'Comissionado'
                    user_password = '@teste159'
                    user_principal_name = f"{user_logon_name}@DOUGLAS.TESTE"
                    # Criar a entrada do usuário no Active Directory
                    entry = [
                        ('objectClass', [b'top', b'person', b'organizationalPerson', b'user']),
                        ('cn', [cn.encode('utf-8')]),
                        ('givenName', [given_name.encode('utf-8')]),
                        ('sn', [sn.encode('utf-8')]),
                        ('userPassword', [user_password.encode('utf-16-le')]),
                        ("displayName", display_name.encode("utf-8")),
                        ("sAMAccountName", user_logon_name_pre_win2000.encode("utf-8")),
                        ('userPrincipalName', [user_principal_name.encode('utf-8')]),
                        ("title", title.encode("utf-8")),
                        ("department", department.encode("utf-8")),
                        ("company", company.encode("utf-8"))
                    ]
                    encoded_entry = [(attr, values) for attr, values in entry]
                    conn.add_s(dn, encoded_entry)
                    # Fechar a conexão LDAP
                    conn.unbind()
                    form.send_mail()
                    return HttpResponse(f"SALVO")
                else:
                    return HttpResponse(f"NAO VALIDO")
            return redirect('/cadastro/')
        else:
            return redirect('/')

    #return render(request, 'cadastro.html')
#class CadastroView(FormView):
#    template_name = 'cadastro.html'
##    form_class = CadastroForm
#    success_url = reverse_lazy('cadastro_sucesso')
#    def form_valid(self, form):
#        form.save()  # Salva os dados do formulário no banco de dados
#        messages.success(self.request, 'Cadastro realizado com sucesso')
#        return super().form_valid(form)

#    def form_invalid(self, form):
#        messages.error(self.request, 'Erro ao cadastrar')
#        return super().form_invalid(form)
#    def dispatch(self, request):
#        if request.method == 'POST':
#            # processar os dados do formulário
#            tipo_moradia = request.POST.get('tipo_moradia')
#            print(tipo_moradia)
#            # context = {'tipo_moradia': tipo_moradia}
#        return render(request, 'cadastro.html')
        #else:
    #sucess_url = reverse_lazy('cadastro')

#class LoadCadastroView


#def logouts(request):
#    if request.method == 'POST':
        # Remova as informações de autenticação da sessão do usuário
#        if 'nome' in request.session:
 ##          name = request.session.get('nome')
   #         print(name)
    #        name = None
     #       print(name)
        # Fecha a conexão LDAP
#        ldap = LDAPBackend()
 #       ldap.close_connection(request)

        # Redireciona o usuário para a página inicial
        #response = redirect('/')
  #      login = None
        # Adiciona uma instrução de não-cache no cabeçalho da resposta HTTP
        #response = HttpResponse()
        #response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        #response['Pragma'] = 'no-cache'
        #response['Expires'] = '0'
   #     print("aqui foi")
    #    print(request.session['nome'])
        #response = redirect('/')
        #return response

    # Se a solicitação não for do tipo POST, redireciona o usuário de volta para a página index
    #return redirect('/index/')
                
               
                
                


                    
                    
                    
                    

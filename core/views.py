from pyad import *
from django.shortcuts import render, redirect
from django.contrib.auth import login , logout
import pythoncom
from django.db import models
import pyad.adquery
import requests
from django.http import JsonResponse
import ldap3
from core.ldap_backend import LDAPBackend
from django.conf import settings
from django.http import HttpResponse
from .models import Dados
from django.contrib.auth.decorators import login_required




def login(request):
    return render(request, '/accounts/login.html')


def loadlogin(request):
    try:
        if request.method == 'POST':
          t = request.POST.get('action')
          print(t, 'inserido')

          if request.POST.get('action') == 'Cadastrar':
                # Renderiza a página de cadastro
                return render(request, 'cadastro.html')
          else:
            username = request.POST['nome']
            password = request.POST['senha']
            request.session['nome'] = username

            ldap = LDAPBackend()
            bound= ldap.authenticate(request, username, password)
            user= ldap.authenticate(request, username, password)
            print(user, 'a')
            if user is True:

                print(bound)

                print(login,'login')
                print(bound, 'aqui')
                return redirect('/index/')


        #print(bound)
            if bound is not None:
            # Redireciona o usuário para a página inicial
                return redirect('/index/')
            else:
            # Exibe uma mensagem de erro de autenticação
                error_msg = 'Usuário ou senha inválidos'
                return redirect('/login/')
    except:
        return redirect('/login/')


def index(request):
    pythoncom.CoInitialize()
    name = request.session.get('nome')
    print(name, '0')
    response = HttpResponse()
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    # Consulta ao AD
    user3 = pyad.adsearch.ADQuery()
    user3.execute_query(
        attributes=["cn", "mail", "description","sn","objectCategory","userAccountControl", "displayName","memberOf","distinguishedName", "title","department" ], where_clause=f"SamAccountName = '{name}'",
        base_dn="OU=Usuarios,OU=NOVACAP,DC=NOVACAP,DC=SEDE"
    )
    print(name,'1')
    context = {}
    # Resultados da consulta ao AD
    for row in user3.get_results():
        context['cn'] = row["cn"]
        context['mail'] = row['mail']
        context['descricao'] = row['description']
        context['sn'] = row['sn']
        context['objc'] = row['objectCategory']
        context['objc2'] = row['userAccountControl']
        context['dis'] = row['displayName']
        context['m'] = row['memberOf']
        context['title'] = row['title']
        context['dep'] = row['department']

    # Consulta ao banco de dados
    dados = Dados.objects.filter(Login=name)
    for dado in dados:
        diferenca = (dado.Ferias_fim - dado.Ferias_inicio).days
        dado.diferenca = diferenca
    context2 = {
        'dados': dados
    }

    # Unindo os dois contextos
    context.update(context2)

    return render(request, 'index.html', context)




def logouts(request):
    if request.method == 'POST':
        # Remova as informações de autenticação da sessão do usuário
        if 'nome' in request.session:
            request.session['nome'] = None
            name = request.session.get('nome')
            print(name)
            name = None
            print(name)
        # Fecha a conexão LDAP
        ldap = LDAPBackend()
        ldap.close_connection(request)

        # Redireciona o usuário para a página inicial
        response = redirect('login')

        # Adiciona uma instrução de não-cache no cabeçalho da resposta HTTP
        response = HttpResponse()
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        print("aqui foi")
        print(request.session['nome'])
        response = redirect('login')
        return response

    # Se a solicitação não for do tipo POST, redireciona o usuário de volta para a página index
    return redirect('/index/')



def cadastro(request):
    if request.method == 'POST':
        tipo_moradia = request.POST.get('tipo_moradia')
        print(tipo_moradia)
        context = {'tipo_moradia': tipo_moradia}
        return render(request, 'cadastro.html', context)
    else:
        return render(request, 'cadastro.html')


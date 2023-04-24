from pyad import *

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from core.models import Usuario
from core.models import Events
import pythoncom
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

import pythoncom
from pyad import *
import pyad.adquery
import requests
from django.http import JsonResponse
import ldap3
from core.ldap_backend import LDAPBackend
from django.conf import settings




def login(request):
    return render(request, 'login.html')


def loadlogin(request):
    if request.method == 'POST':
        username = request.POST['nome']
        password = request.POST['senha']
        request.session['nome'] = username

        ldap = LDAPBackend()
        bound= ldap.authenticate(request, username, password)

        #print(bound)
        if bound is not None:
            # Redireciona o usuário para a página inicial
            return redirect('index')
        else:
            # Exibe uma mensagem de erro de autenticação
            error_msg = 'Usuário ou senha inválidos'
            return render(request, 'login.html', {'error': error_msg})
    else:
        return render(request, 'login.html')
def index(request):
    pythoncom.CoInitialize()
    name = request.session.get('nome')
    #name="carlos.delfino"
    print(name, '0')
    user3 = pyad.adsearch.ADQuery()
    user3.execute_query(
        attributes=["cn", "mail", "description","sn","objectCategory","userAccountControl", "displayName","memberOf","distinguishedName", "title","department" ], where_clause=f"SamAccountName = '{name}'",
        base_dn="OU=Usuarios,OU=NOVACAP,DC=NOVACAP,DC=SEDE"
    )
    print(name,'1')
    context = {}
    # imprimir os resultados da consulta
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

    return render(request, 'index.html', context)



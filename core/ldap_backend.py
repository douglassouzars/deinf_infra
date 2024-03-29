import ldap3
from django.conf import settings
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
import ldap
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect







class LDAPBackend:
    def authenticate(self, request, username=None, password=None, **kwargs):
        server = ldap3.Server(settings.LDAP_SERVER, port=settings.LDAP_PORT, use_ssl=settings.LDAP_USE_SSL)
        conn = ldap3.Connection(server, user=settings.LDAP_BIND_DN, password=settings.LDAP_BIND_PASSWORD,
                                auto_bind=True)

        if username.isdigit():
            search_filter = f'(&(objectClass=user)(sAMAccountName={username}))'
        else:
            search_filter = f'(&(objectClass=user)(userPrincipalName={username}@DOUGLAS.TESTE))'
        print(search_filter)
        u1=conn.search(settings.LDAP_SEARCH_BASE, search_filter)



   ##        return False
        print(f"Connection status before authentication: {conn.bound}")

        if not conn.entries:
            return None
        dn = conn.entries[0].entry_dn
        print(dn)
        conn.unbind()

        print("qual o valor",dn)
        # Authenticate user against LDAP
        conn = ldap3.Connection(server, user=dn, password=password, auto_bind=True)
        print(f"Connection status after2 authentication: {conn.bound}")
        print(conn)

        return (conn.bound)
        if not conn.bind():
            print("nao foi")
            return None
        conn.unbind()
        request.session['ldap_connection'] = conn
        return True
    def close_connection(self, request):
        # Fecha a conexão LDAP
        # Verifica se o objeto de conexão LDAP está presente na sessão do usuário
        if 'ldap_connection' in request.session:
            conn = request.session['ldap_connection']
            if conn.bound:
                conn.unbind()
            del request.session['ldap_connection']


class CustomAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        print(user)
        if request.user.is_authenticated and request.user.user == 'true':
            print("oie")
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/login/')


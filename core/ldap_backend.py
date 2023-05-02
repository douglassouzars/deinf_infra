import ldap3
from django.conf import settings



class LDAPBackend:
    def authenticate(self, request, username=None, password=None, **kwargs):
        server = ldap3.Server(settings.LDAP_SERVER, port=settings.LDAP_PORT, use_ssl=settings.LDAP_USE_SSL)
        conn = ldap3.Connection(server, user=settings.LDAP_BIND_DN, password=settings.LDAP_BIND_PASSWORD,
                                auto_bind=True)
        search_filter = f'(&(objectClass=user)(sAMAccountName={username}))'
        conn.search(settings.LDAP_SEARCH_BASE, search_filter)
        print(f"Connection status before authentication: {conn.bound}")

        if not conn.entries:
            return None
        dn = conn.entries[0].entry_dn
        conn.unbind()


        # Authenticate user against LDAP
        conn = ldap3.Connection(server, user=dn, password=password, auto_bind=True)
        print(f"Connection status after2 authentication: {conn.bound}")
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




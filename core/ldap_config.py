import ldap
from django.contrib.auth.backends import BaseBackend
from django.conf import settings
from django.contrib.auth.models import User
from django_auth_ldap.config import LDAPSearch

# Define as opções do servidor LDAP
AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_REFERRALS: 0,
    ldap.OPT_NETWORK_TIMEOUT: 30,
}

class LDAPBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Define o servidor LDAP
        server_uri = settings.AUTH_LDAP_SERVER_URI
        server = ldap.initialize(server_uri)
        server.set_option(ldap.OPT_REFERRALS, 0)
        server.set_option(ldap.OPT_NETWORK_TIMEOUT, 30)

        # Busca o usuário no LDAP
        base_dn = settings.AUTH_LDAP_BASE_DN
        search_filter = settings.AUTH_LDAP_USER_SEARCH_FILTER % {'user': username}
        search = LDAPSearch(base_dn, ldap.SCOPE_SUBTREE, search_filter, settings.AUTH_LDAP_USER_ATTRS)
        results = search.execute(server)

        if len(results) == 0:
            return None

        # Autentica o usuário no LDAP
        user_dn = results[0][0]
        try:
            server.bind_s(user_dn, password)
        except ldap.INVALID_CREDENTIALS:
            return None

        # Busca ou cria o usuário no Django
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User(username=username)
            user.is_staff = False
            user.is_superuser = False
            user.save()

        return user

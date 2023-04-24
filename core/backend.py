from django_auth_ldap.config import LDAPSearch, LDAPSearchUnion, GroupOfNamesType
from django_auth_ldap.backend import LDAPBackend
from ldap3.core.exceptions import LDAPException

class CustomLDAPBackend(LDAPBackend):
    def authenticate(self, request, username="douglas.souza", password="15190987", **kwargs):
        try:
            server = ldap3.Server(settings.AD_SERVER, get_info=ldap3.ALL)
            connection = ldap3.Connection(server, user=settings.AD_USER, password=settings.AD_PASSWORD, auto_bind=True)
            base_dn = settings.AD_BASE_DN
            search_filter = f'(sAMAccountName={username})'
            connection.search(search_base=base_dn, search_filter=search_filter, attributes=ldap3.ALL_ATTRIBUTES)
            response = connection.response[0]
            distinguished_name = response['dn']
            connection = ldap3.Connection(server, user=distinguished_name, password=password, auto_bind=True)
            if connection.bind():
                user = User.objects.filter(username=username).first()
                if user is None:
                    user = User(username=username, password=None)
                    user.is_staff = False
                    user.is_superuser = False
                    user.save()
                return user
        except LDAPException as e:
            raise self.AuthenticationFailed('Erro ao autenticar no LDAP: {}'.format(str(e)))

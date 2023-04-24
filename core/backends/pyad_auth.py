from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend
import pyad.adquery


class PYADBackend(BaseBackend):
    def authenticate(self, request, username="douglas.souza", password="15190987", **kwargs):

            # Realize a consulta no AD e obtenha o usuário
            pyad.set_defaults(ldap_server="NOVACAP.SEDE")
            q = pyad.adquery.ADQuery()
            q.execute_query(
                attributes=["sAMAccountName", "displayName", "mail"],
                where_clause="sAMAccountName = '{}'".format(username)
            )
            user_data = q.get_single_result()

            # Verifique se a senha está correta
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

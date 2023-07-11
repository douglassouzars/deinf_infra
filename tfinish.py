import ldap

# Informações de autenticação
username = 'Marta Eliane Rocha'
password = '@teste159'
server_url = 'ldap://SRVDOUGLAS'
bind_dn = 'conexao_ldap@DOUGLAS.TESTE'

# Conectar e autenticar no servidor LDAP
conn = ldap.initialize(server_url)
conn.simple_bind_s(bind_dn, password)

# Realizar a pesquisa para obter o DN completo do grupo com base no CN
base_dn = 'OU=DEINF,OU=DA,OU=FILE SERVER,OU=GROUPS,OU=ACCOUNT AND GROUPS,DC=DOUGLAS,DC=TESTE'
group_cn = 'GGRP_USERS_DEINF_READ'
group_filter = f"(CN={group_cn})"
group_results = conn.search_s(base_dn, ldap.SCOPE_SUBTREE, group_filter)
print(group_results)

if group_results:
    group_dn = group_results[0][0]  # Obter o DN do grupo encontrado
    print(group_dn)
    member_dn = f"CN={username},OU=USUARIOS,OU=ACCOUNT,OU=ACCOUNT AND GROUPS,DC=DOUGLAS,DC=TESTE"  # DN do usuário a ser adicionado
    mod_attrs = [
        (ldap.MOD_ADD, 'member', member_dn.encode('utf-8'))  # Adicionar o usuário como membro do grupo
    ]
    conn.modify_s(group_dn, mod_attrs)
    print('Usuário adicionado ao grupo com sucesso')
else:
    print('Grupo não encontrado')
"""
import ldap

# Informações de autenticação
server_url = 'ldap://SRVDOUGLAS'
bind_dn = 'conexao_ldap@DOUGLAS.TESTE'
password = '@teste159'

# Conectar e autenticar no servidor LDAP
conn = ldap.initialize(server_url)
conn.simple_bind_s(bind_dn, password)

# Consultar o DN do grupo
base_dn = 'OU=FILE SERVER,OU=GROUPS,OU=ACCOUNT AND GROUPS,DC=DOUGLAS,DC=TESTE'
group_cn = 'GGRP_USERS_DEINF_READ'
group_filter = f"(cn={group_cn})"
group_attrs = ['dn']

try:
    group_search = conn.search_s(base_dn, ldap.SCOPE_SUBTREE, group_filter, group_attrs)
    if group_search:
        group_dn = group_search[0][0]  # Obter o DN do grupo encontrado
        print(f"DN do grupo '{group_cn}': {group_dn}")

        # Consultar os membros do grupo
        member_filter = '(objectClass=*)'
        member_attrs = ['cn']

        try:
            member_search = conn.search_s(group_dn, ldap.SCOPE_BASE, member_filter, member_attrs)
            if member_search:
                print("Membros do grupo:")
                for dn, attrs in member_search:
                    cn = attrs['cn'][0].decode('utf-8')
                    print(f"  - {cn}")
            else:
                print("O grupo não possui membros.")
        except ldap.LDAPError as e:
            print(f"Erro ao pesquisar membros do grupo: {e}")
    else:
        print("Grupo não encontrado.")
except ldap.LDAPError as e:
    print(f"Erro ao pesquisar DN do grupo: {e}")"""



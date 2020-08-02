#!/usr/bin/env python3

from os import environ
from dotenv import load_dotenv
from ldap3.utils.hashed import hashed
from ldap3 import Server, Connection, HASHED_SHA

load_dotenv()

server = Server(environ['LDAP_HOST'], use_ssl=False)
ldap = Connection(server, user=environ['LDAP_ADMIN'], password=environ['LDAP_PASSWORD'])

if not ldap.bind():
  print('Problemas ao se autenticar')
  exit(1)

# cadastra o grupo com add, existem outras opções como modify ou delete
# as classes são um lista, já o objeto em sí um dicionário
ldap.add('ou=users,dc=example,dc=com', ['organizationalUnit'], {'ou' : 'users'})

# define um objeto mais complexo com um dicionário
ldif = {
  'cn': 'Developer',
  'sn': 'Desenvolvedor',
  'mail': 'developer@example.com',
  'uidNumber': 10001,
  'gidNumber': 10001,
  'homeDirectory': '/srv/home/developer',
  'uid': 'developer',
  'userPassword' : hashed(HASHED_SHA, '4linux')
}

# define algumas classes em um dicionário
object_classes = ['top', 'posixAccount', 'person', 'inetOrgPerson']

ldap.add('uid=developer,ou=users,dc=example,dc=com', object_classes, ldif)

entries = ldap.search('dc=example,dc=com', '(objectclass=*)') # o filtro é obrigatório
if entries:
  for entry in ldap.entries:
    print(entry)

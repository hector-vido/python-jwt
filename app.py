import jwt
from flask import Flask, request
from ldap3 import Server, Connection

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/auth', methods=['POST'])
def auth():
  data = request.get_json()
  print(data)
  server = Server(environ['LDAP_HOST'], use_ssl=False)
  ldap = Connection(server, user='uid={},ou=users,dc=example,dc=com'.format(data['usuario']), password=data['senha'])
  if ldap.bind():
    encode_jwt = jwt.encode({'some' : 'payload'}, 'secret', algorithm='HS256')
    return redirect('/')

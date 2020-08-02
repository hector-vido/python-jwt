import time, jwt
from os import environ
from ldap3 import Server, Connection
from flask import Flask, request, make_response, jsonify

app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/auth', methods=['POST'])
def auth():

  try:
    data = request.get_json()
    if not data or 'user' not in data or 'password' not in data:
      raise Exception('Especifique "user" e "password"')
  except Exception as e:
    return make_response(jsonify({'message' : str(e)}), 400)

  server = Server(environ['LDAP_HOST'], use_ssl=False)
  ldap = Connection(server, user='uid={},ou=users,dc=example,dc=com'.format(data['user']), password=data['password'])
  if ldap.bind():
    encoded_jwt = jwt.encode({'exp' : int(time.time()) + int(environ['SESSION_TIME']), 'user' : data['user'], 'role' : 'user'}, environ['JWT_SECRET'], algorithm='HS256')
    return encoded_jwt
  else:
    return make_response(jsonify({'message' : 'Usuário ou senha inválidos'}), 404)

@app.route('/check')
def check():
  try:
    jwt.decode(request.headers['Authorization'].strip('Bearer').strip(), environ['JWT_SECRET'], algorithms='HS256')
    return jsonify({'message' : 'JWT válido'})
  except jwt.ExpiredSignatureError as e: 
    return make_response(jsonify({'message' : 'JWT expirado'}), 410)
  except Exception as e:
    return make_response(jsonify({'message' : str(e)}), 400)

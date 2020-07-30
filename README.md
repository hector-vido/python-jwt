# JWT

JSON Web Tokens é um formato aberto especificado pela [RFC 7591](https://tools.ietf.org/html/rfc7519) para representar identidades de forma segura entre duas partes.

Essa aplicação é um simples criador e validador de JWT escrita com Python + Flask para fazer parte de uma infraestrutura de estudo mais complexa.

## Instalação

```bash
git clone https://github.com/hector-vido/python-jwt.git
cd python-jwt
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
mv .env-example .env
# editar .env
flask run
```

## Utilização

É preciso ter o OpenLDAP fornecido no **docker-compose** da dashboard funcionando, ou utilizar qualquer outra solução. Se a base não estiver inicializada, executar:

```bash
python3 ldap.py
```

Isso criará um grupo e um usuário dentro do LDAP.

Feito isso, para pedir um token faça o seguinte:

```bash
curl -X POST -d '{"user" : "developer", "password" : "123"}' -H 'Content-Type: application/json' localhost:5000/auth
```

Uma vez com o token em mãos, para verificá-lo basta executar:

```bash
curl -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1OTYxMzQ4ODQsInVzZXIiOiJkZXZlbG9wZXIiLCJyb2xlIjoidXNlciJ9.RAec72dnAAxf4CvT0KUYoY_sBCfFb_aZXL4b3Q0znos' localhost:5000/check
```

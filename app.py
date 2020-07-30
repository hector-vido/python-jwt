import jwt

encoded_jwt = jwt.encode({'some' : 'payload'}, 'secret', algorithm='HS256')

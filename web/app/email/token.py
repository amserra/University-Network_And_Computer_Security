from itsdangerous import URLSafeTimedSerializer
from os import environ

def generate_token(email):
    serializer = URLSafeTimedSerializer(environ['SECRET_KEY'])
    return serializer.dumps(email, salt=environ['SECURITY_PASSWORD_SALT'])

def generate_token_with_id(email, id):
    serializer = URLSafeTimedSerializer(environ['SECRET_KEY'])
    return serializer.dumps([email, id], salt=environ['SECURITY_PASSWORD_SALT'])

# 10min to confirm
def confirm_token(token, expiration=600):
    serializer = URLSafeTimedSerializer(environ['SECRET_KEY'])
    # Eventual exception is passed to calling function
    email = serializer.loads(
        token,
        salt=environ['SECURITY_PASSWORD_SALT'],
        max_age=expiration
    )
    
    return email

def confirm_token_no_expire(token):
    serializer = URLSafeTimedSerializer(environ['SECRET_KEY'])
    # Eventual exception is passed to calling function
    [email, id] = serializer.loads(
        token,
        salt=environ['SECURITY_PASSWORD_SALT']
    )
    
    return [email, id]
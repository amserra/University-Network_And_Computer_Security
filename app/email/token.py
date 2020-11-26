from itsdangerous import URLSafeTimedSerializer
from os import environ

def generate_token(email):
    serializer = URLSafeTimedSerializer(environ['SECRET_KEY'])
    return serializer.dumps(email, salt=environ['SECURITY_PASSWORD_SALT'])

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
from itsdangerous import URLSafeTimedSerializer
from os import environ

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(environ['SECRET_KEY'])
    return serializer.dumps(email, salt=environ['SECURITY_PASSWORD_SALT'])

# 30min to confirm
def confirm_token(token, expiration=1800):
    serializer = URLSafeTimedSerializer(environ['SECRET_KEY'])
    # Eventual exception is passed to calling function
    email = serializer.loads(
        token,
        salt=environ['SECURITY_PASSWORD_SALT'],
        max_age=expiration
    )
    
    return email
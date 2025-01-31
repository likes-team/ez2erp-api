from Crypto.Random import get_random_bytes
from ez2erp_engine.models import User


def create_user(event):
    user = User()
    user.fname = event.get('fname')
    user.lname = event.get('lname')
    user.email = event.get('email')
    
    password = event.get('password')

    encryption_key = get_random_bytes(16)
    user.encrypt_password(password, encryption_key)
    user.save()
    return user.to_dict()
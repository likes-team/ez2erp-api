from ez2erp_engine.models import User


def create_user(event):
    user = User()
    user.fname = event.get('fname')
    user.lname = event.get('lname')
    user.email = event.get('email')
    password = event.get('password')

    user.encrypt_password(password)
    user.save()
    response = {
        'data': user.to_dict()
    }
    return response, 'success', "User created successfully!"


from ez2erp_engine.auth import user_login


def login(event):
    email = event.get('email')
    password = event.get('password')

    user = user_login(email, password)
    print(user)
    return user

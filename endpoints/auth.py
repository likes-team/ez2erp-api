from ez2erp_engine.models import User


def login(event):
    email = event.get('email')
    password = event.get('password')
    print("email", email)

    user = User.ez2.select_by_index(
        index_name='email-index',
        key='email',
        val=email
    )
    print(user)
    return user

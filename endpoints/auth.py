from ez2erp_engine.models import User, Organization
from ez2erp_engine.db import Ez2DBManager
# from boto3.dynamodb.conditions import Key


def login(event):
    email = event.get('email')
    password = event.get('password')
    print("email", email)

    # Sample ORM usage
    user: User = User.ez2.select_by_index(
        index_name='email-index',
        key='email',
        val=email
    )

    # # Sample direct usage  
    # dynamodb_client = Ez2DBManager.dynamo_client
    # user = dynamodb_client.table.query(
    #     IndexName='email-index',
    #     KeyConditionExpression=Key(key).eq(val)
    # )

    print(user.__dict__)
    is_password_matched = user.decrypt_password(password)

    if user is None or not is_password_matched:
        return None, "error", "Wrong Credentials!"

    return user.to_dict(), "success", "Logged in Successfully!"


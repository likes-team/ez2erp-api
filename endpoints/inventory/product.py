from boto3.dynamodb.conditions import Key
from ez2erp_engine.models import Product


def get_products(event):
    # key_condition = Key("id")
    products, offset_key = Product.ez2.select()
    result = {
        'data': [],
        'last_key': offset_key
    }
    for product in products:
        result['data'].append(product.to_dict())

    return result, "success", "Products retrieved successfully!"


def create_product(event):
    product = Product()
    product.name = event.get('name')
    product.cost_price = str(event.get('cost_price', "0.00"))
    product.sale_price = str(event.get('sale_price', "0.00"))
    product.product_type = event.get('product_type')
    product.category_id = event.get('category_id')
    product.sku = event.get('sku')

    product.save()
    return product.to_dict(), 'success', "Product created successfully!"

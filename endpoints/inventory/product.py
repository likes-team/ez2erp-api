from boto3.dynamodb.conditions import Key
from ez2erp_engine.models import Product



def get_product(product_id):
    product = Product.ez2.get(product_id)
    result = {
        'data': product.to_dict()
    }

    return result, "success", "Product retrieved successfully!"


def get_products(event):
    oid = event.get('oid')
    if oid:
        return get_product(oid)

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
    print("test", product.in_db)
    product.name = event.get('name')
    product.cost_price = str(event.get('cost_price', "0.00"))
    product.sale_price = str(event.get('sale_price', "0.00"))
    product.product_type = event.get('product_type')
    product.category_id = event.get('category_id')
    product.sku = event.get('sku')

    product.save()
    return product.to_dict(), 'success', "Product created successfully!"


def edit_product(event):
    product_id = event.get('oid')
    product = Product.ez2.get(product_id)
    product.name = event.get('name')
    product.cost_price = str(event.get('cost_price'))
    product.sale_price = str(event.get('sale_price'))
    product.product_type = event.get('product_type')
    product.category_id = event.get('category_id')
    product.sku = event.get('sku')
    product.save()
    return product.to_dict(), 'success', "Product updated successfully!"


def delete_product(event):
    product_id = event.get('oid')
    deleted_id = Product.ez2.delete(product_id)

    response = {
        'data': deleted_id
    }
    return response, 'success', "Product deleted successfully!"

from boto3.dynamodb.conditions import Key
from ez2erp_engine.models import Product, ProductCategory


def get_product(product_id):
    product = Product.ez2.get(product_id)
    result = {
        'data': product.to_dict()
    }

    return result, "success", "Product retrieved successfully!"


def get_product_categories(event):
    oid = event.get('oid')
    if oid:
        return get_product(oid)

    product_categories, offset_key = ProductCategory.ez2.select()
    result = {
        'data': [],
        'last_key': offset_key
    }
    for product_category in product_categories:
        result['data'].append(product_category.to_dict())

    return result, "success", "Product Categories retrieved successfully!"


def create_product_category(event):
    product_category = ProductCategory()
    product_category.name = event.get('name')
    product_category.description = event.get('description')

    product_category.save()
    return product_category.to_dict(), 'success', "Product Category created successfully!"


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

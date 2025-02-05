from ez2erp_engine.models import Product
from decimal import Decimal


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

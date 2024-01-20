from flask import Flask, request, jsonify

app = Flask(__name__)


inventory = []
orders = []



class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock



class Order:
    def __init__(self, order_id, products):
        self.order_id = order_id
        self.products = products



@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    required_fields = ['name', 'price', 'stock']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing fields'}), 400

    product_id = len(inventory) + 1
    new_product = Product(product_id, data['name'], data['price'], data['stock'])
    inventory.append(new_product.__dict__)

    return jsonify(new_product.__dict__), 201



@app.route('/products', methods=['GET'])
def get_all_products():
    return jsonify({'products': inventory})



@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in inventory if p['product_id'] == product_id), None)

    if not product:
        return jsonify({'error': 'Product not found'}), 404

    return jsonify({'product': product})



@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = next((p for p in inventory if p['product_id'] == product_id), None)

    if not product:
        return jsonify({'error': 'Product not found'}), 404

    data = request.json
    product['name'] = data.get('name', product['name'])
    product['price'] = data.get('price', product['price'])
    product['stock'] = data.get('stock', product['stock'])

    return jsonify({'product': product})



@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global inventory
    inventory = [p for p in inventory if p['product_id'] != product_id]
    return jsonify({'message': 'Product deleted successfully'})



@app.route('/orders', methods=['POST'])
def place_order():
    data = request.json
    product_ids = data.get('product_ids', [])

   
    for product_id in product_ids:
        product = next((p for p in inventory if p['product_id'] == product_id), None)
        if not product or product['stock'] == 0:
            return jsonify({'error': f'Product with ID {product_id} is not available'}), 400

    order_id = len(orders) + 1
    ordered_products = [{'product_id': product_id, 'name': p['name']} for product_id, p in zip(product_ids, inventory)]
    orders.append(Order(order_id, ordered_products).__dict__)

    
    for product_id in product_ids:
        product = next(p for p in inventory if p['product_id'] == product_id)
        product['stock'] -= 1

    return jsonify({'order_id': order_id})



@app.route('/orders', methods=['GET'])
def get_all_orders():
    return jsonify({'orders': orders})


if __name__ == '__main__':
    app.run(debug=True)

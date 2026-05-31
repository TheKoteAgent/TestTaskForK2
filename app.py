from flask import Flask, request, jsonify
from models import db, Client, Product, Order, OrderItem

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///erp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/api/clients/create', methods=['POST'])
def create_client():
    data = request.get_json()

    if not data or 'name' not in data or 'phone' not in data:
        return jsonify({'error': 'name or phone is empty'}), 400

    new_client = Client(
        name=data['name'],
        phone=data['phone'],
    )
    db.session.add(new_client)
    db.session.commit()

    return jsonify({'message': 'created',
                    'client': {
                        'id': new_client.id,
                        'name': new_client.name,
                        'phone': new_client.phone
                    }}), 201


@app.route('/api/product/create', methods=['POST'])
def create_product():
    data = request.get_json()

    required_fields = ['product_name', 'product_amount', 'product_price']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'not entered field'}), 400

    new_product = Product(
        product_name=data['product_name'],
        product_amount=data['product_amount'],
        product_price=data['product_price']
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify({
        'message': 'created',
        'product': {
            'product_id': new_product.id,
            'product_name': new_product.product_name,
            'product_amount': new_product.product_amount,
            'product_price': new_product.product_price
        }
    }), 201


@app.route('/api/order/create', methods=['POST'])
def create_order():
    data = request.get_json()

    if not data or 'client_id' not in data or 'items' not in data:
        return jsonify({'error': 'field not entered'}), 400

    client = db.session.get(Client, data['client_id'])
    if not client:
        return jsonify({'error': 'client not found'}), 404

    items_list = data['items']
    if not items_list:
        return jsonify({'error': 'no items'}), 400

    new_order = Order(
        client_id=client.id,
        total_sum=0.0
    )
    db.session.add(new_order)
    calculated_sum = 0.0

    for item_data in items_list:
        product_id = item_data.get('product_id')
        quantity = item_data.get('quantity', 1)

        product = db.session.get(Product, product_id)
        if not product:
            return jsonify({'error': 'product not found'}), 404

        if product.product_amount < quantity:
            return jsonify({
                'error': 'no products amoutn'
            }), 400

        product.product_amount -= quantity

        calculated_sum += product.product_price * quantity

        order_item = OrderItem(
            product_id=product.id,
            quantity=quantity,
            order=new_order
        )
        db.session.add(order_item)

    new_order.total_sum = calculated_sum
    db.session.commit()

    return jsonify({
        'message': 'order created',
        'order': {
            'id': new_order.id,
            'client_id': new_order.client_id,
            'total_sum': new_order.total_sum,
            'products': [
                {
                    'name': item.product.product_name,
                    'quantity': item.quantity
                } for item in new_order.items
            ]
        }
    }), 201

@app.route('/api/order/client/<int:client_id>', methods=['GET'])
def get_client_orders(client_id):
    client = db.session.get(Client, client_id)
    if not client:
        return jsonify({'error': 'client not found'}), 404

    return jsonify({
        'orders': [
            {
                'id': order.id,
                'total_sum': order.total_sum,
                'products': [
                    {
                        'name': item.product.product_name,
                        'quantity': item.quantity
                    } for item in order.items
                ]
            } for order in client.orders
        ]
    }), 200

@app.route('/api/clients', methods=['GET'])
def get_all_clients():
    clients = Client.query.all()
    return jsonify({
        'clients': [
            {
                'id': c.id,
                'name': c.name,
                'phone': c.phone
            } for c in clients
        ]
    }), 200


@app.route('/api/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    return jsonify({
        'products': [
            {
                'id': p.id,
                'product_name': p.product_name,
                'product_amount': p.product_amount,
                'product_price': p.product_price
            } for p in products
        ]
    }), 200


@app.route('/api/orders', methods=['GET'])
def get_all_orders():
    orders = Order.query.all()
    return jsonify({
        'orders': [
            {
                'id': order.id,
                'client_id': order.client_id,
                'total_sum': order.total_sum,
                'products': [
                    {
                        'name': item.product.product_name,
                        'quantity': item.quantity
                    } for item in order.items
                ]
            } for order in orders
        ]
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
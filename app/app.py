#!flask/bin/python
from flask import Flask, jsonify
from ..src.warehouse import Warehouse
from ..src.batch import Batch, Freshness, date_format
from ..src.product import Product

app = Flask(__name__)

warehouse = Warehouse()
product_1 = Product('Chicken Satay', 'LILYs')
product_2 = Product('Pasta Pesto', 'Don Leone')
product_3 = Product('Ramen', 'IKOO')

warehouse.add_batch(product_1, 1000, '2019-04-01')
warehouse.add_batch(product_1, 200, '2019-04-05')
warehouse.add_batch(product_1, 500, '2019-05-01')
warehouse.add_batch(product_1, 100, '2019-04-10')
warehouse.add_batch(product_2, 200, '2019-04-10')
warehouse.add_batch(product_3, 500, '2019-04-05')

# @app.route('/inventory_manager/api/v1.0/batches', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': tasks})


@app.route('/inventory_manager/api/v1.0/get_batch_inventory/<int:batch_id>', methods=['GET'])
def get_batch(batch_id):
	try:
		batch = warehouse.get_batch_by_id(batch_id)
		return jsonify({batch_id: (batch.product.product_name, batch.remaining_units)})
	except ValueError:
		abort(404)

@app.route('/inventory_manager/api/v1.0/get_warehouse_inventory/<string:product_name>', methods=['GET'])
def get_product(product_name):
	try:
		product_inventory = warehouse.get_inventory_per_productname(product_name)
		return jsonify(product_inventory)
	except ValueError:
		abort(404)

@app.route('/inventory_manager/api/v1.0/freshness', methods=['GET'])
def get_freshness():
	freshness = warehouse.get_freshness_overview()
	print(freshness)
	return jsonify(freshness)

if __name__ == '__main__':
    app.run(debug=True)

#!flask/bin/python
from flask import Flask, jsonify, Response, request, abort
from time import sleep
import json
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
warehouse.add_batch(product_3, 500, '2019-03-05')
sleep(1)
warehouse.update_batch_stock_count(0, 2000)
warehouse.update_batch_stock_count(5, 200)

# Retrieve history of given batch
@app.route('/inventory_manager/api/v1.0/batch_log/<int:batch_id>', methods=['GET'])
def get_batch_log(batch_id):
	try:
		batch = warehouse.get_batch_by_id(batch_id)
		return jsonify(batch.get_log())
	except ValueError:
		abort(404)

# Retrieve overview of freshness in warehouse
@app.route('/inventory_manager/api/v1.0/freshness', methods=['GET'])
def get_freshness():
	try:
		return jsonify(warehouse.get_freshness())
	except ValueError:
		abort(404)

# Retrieve Warehouse inventory
@app.route('/inventory_manager/api/v1.0/warehouse', methods=['GET'])
def get_warehouse_inventory():
	try:
		return jsonify(warehouse.get_products())
	except ValueError:
		abort(404)

# Retrieve Product inventory
@app.route('/inventory_manager/api/v1.0/product/<int:product_id>', methods=['GET'])
def get_product_inventory(product_id):
	try:
		return jsonify(warehouse.get_product_inventory(product_id))
	except ValueError:
		abort(404)

# Retrieve Batch inventory
@app.route('/inventory_manager/api/v1.0/batch/<int:batch_id>', methods=['GET'])
def get_batch(batch_id):
	try:
		return jsonify(warehouse.get_batch_inventory(batch_id))
	except:
		abort(404)

# Update/Modify stock of any batch
@app.route('/inventory_manager/api/v1.0/batch/<int:batch_id>', methods=['PUT'])
def update_batch(batch_id):
	try:	
		batch = warehouse.get_batch_by_id(batch_id)
		new_stock_count = request.json['new_stock_count']
		print(new_stock_count)
		warehouse.update_batch_stock_count(batch_id, new_stock_count)
		return jsonify(warehouse.get_batch_inventory(batch_id))
	except ValueError:
		abort(404)

# Add a new batch to warehouse
@app.route('/inventory_manager/api/v1.0/batch', methods=['POST'])
def add_batch():
	try:
		new_batch = request.json['batch']
		product = Product(new_batch['product_name'], new_batch['supplier'])
		batch_id = warehouse.add_batch(product, int(new_batch['total_stock_count']), new_batch['expiry_date'])
		return jsonify(warehouse.get_batch_inventory(batch_id))
	except ValueError:
		abort(404)

if __name__ == '__main__':
    app.run(debug=True)

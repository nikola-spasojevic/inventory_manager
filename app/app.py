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

# Retrieve history of given batch
@app.route('/inventory_manager/api/v1.0/get_batch_log/<int:batch_id>', methods=['GET'])
def get_batch_log(batch_id):
	try:
		batch = warehouse.get_batch_by_id(batch_id)
		return jsonify(batch.get_log())
	except ValueError:
		abort(404)

# Retrieve overview of freshness in warehouse
@app.route('/inventory_manager/api/v1.0/get_freshness', methods=['GET'])
def get_freshness():
	try:
		return jsonify(warehouse.get_freshness())
	except ValueError:
		abort(404)

# Retrieve Warehouse inventory
@app.route('/inventory_manager/api/v1.0/get_warehouse_inventory', methods=['GET'])
def get_warehouse_inventory():
	try:
		return jsonify(warehouse.get_products())
	except ValueError:
		abort(404)

# Retrieve Product inventory
@app.route('/inventory_manager/api/v1.0/get_product_inventory/<int:product_id>', methods=['GET'])
def get_product_inventory(product_id):
	try:
		return jsonify(warehouse.get_product_inventory(product_id))
	except ValueError:
		abort(404)

# Retrieve Batch inventory
@app.route('/inventory_manager/api/v1.0/get_batch_inventory/<int:batch_id>', methods=['GET'])
def get_batch(batch_id):
	try:
		return jsonify(warehouse.get_batch_inventory(batch_id))
	except ValueError:
		abort(404)

# Update/Modify stock of any batch
# curl -XPUT -H "Accept:application/json"  http://localhost:5000/inventory_manager/api/v1.0/update_batch/0 -d '{'remaining_units': '2000'}'| python -m json.tool
@app.route('/inventory_manager/api/v1.0/update_batch/<int:batch_id>', methods=['PUT'])
def update_batch(batch_id):
	try:
		if not request.json:
			abort(400)

		batch = warehouse.get_batch_by_id(batch_id)
		if batch is None:
			abort(404)
		#if 'remaining_units' in request.json and type(request.json['remaining_units']) != unicode:
		#	abort(400)

		remaining_units = request.json['remaining_units']

		# batch. = request.json.get('remaining_units', warehouse.id2batch(batch_id).remaining_units)
		return jsonify(remaining_units)
	except:
		abort(404)

# @app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
# def update_task(task_id):
#     task = [task for task in tasks if task['id'] == task_id]
#     if len(task) == 0:
#         abort(404)
    
    
#     task[0]['title'] = request.json.get('title', task[0]['title'])
#     task[0]['description'] = request.json.get('description', task[0]['description'])
#     task[0]['done'] = request.json.get('done', task[0]['done'])
#     return jsonify({'task': task[0]})


if __name__ == '__main__':
    app.run(debug=True)

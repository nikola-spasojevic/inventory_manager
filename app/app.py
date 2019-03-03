#!flask/bin/python
from flask import Flask, jsonify
from ..src.warehouse import Warehouse
from ..src.batch import Batch, Freshness, date_format

app = Flask(__name__)

warehouse = Warehouse()
batches = [ Batch('Chicken Satay', 'LILYs', 1000, '2019-04-01'), 
Batch('Pasta Pesto', 'Don Leone', 200, '2019-04-10'),
Batch('Ramen', 'IKOO', 500, '2019-04-05')
]

warehouse.add_batches(batches)

# @app.route('/inventory_manager/api/v1.0/batches', methods=['GET'])
# def get_tasks():
#     return jsonify({'tasks': tasks})

@app.route('/inventory_manager/api/v1.0/batches', methods=['GET'])
def get_task():
	# try:
	# 	batch = warehouse.get_batch_by_id(batch_id)
	# except ValueError:
	# 	abort(404)
	
	return jsonify(warehouse.product_batches)

if __name__ == '__main__':
    app.run(debug=True)

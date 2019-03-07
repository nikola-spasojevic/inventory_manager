import pytest
from datetime import datetime
from collections import defaultdict, Counter
from ..src.warehouse import Warehouse
from ..src.batch import Batch, Freshness, date_format
from ..src.product import Product

product_1 = Product('Chicken Satay', 'LILYs')
product_2 = Product('Pasta Pesto', 'Don Leone')
product_3 = Product('Ramen', 'IKOO')

def test_add_batch():
	"""
	Test that a all batches from list can be added to the batch dictionary
	"""
	warehouse = Warehouse()
	warehouse.add_batch(product_1, 1000, '2019-04-01')
	warehouse.add_batch(product_2, 200, '2019-04-10')
	warehouse.add_batch(product_3, 500, '2019-04-05')
	assert len(warehouse.batches) == 3

def test_add_product_to_warehouse():
	warehouse = Warehouse()
	warehouse.add_product_to_warehouse(product_1)
	assert warehouse.product2id[product_1] == 0
	assert warehouse.id2product[0] == product_1
	warehouse.add_product_to_warehouse(product_2)
	assert warehouse.product2id[product_2] == 1
	assert warehouse.id2product[1] == product_2
	warehouse.add_product_to_warehouse(product_3)
	assert warehouse.product2id[product_3] == 2
	assert warehouse.id2product[2] == product_3

def test_get_batch():
	"""
	Test that a batch can be retrieved with it's unique (product, supplier, expiry_date) tuple
	"""
	warehouse = Warehouse()
	warehouse.add_batch(product_1, 1000, '2019-04-01')
	b_1 = Batch(product_1, 1000, '2019-04-01')

	batch = warehouse.get_batch('Chicken Satay', 'LILYs', b_1.expiry_date)
	assert batch == b_1

	with pytest.raises(ValueError):
		batch = warehouse.get_batch('Chicken Satay', 'LILYs', '2019-04-05')

def test_freshness():
	"""
	Test warehouse freshness, whether it represntes correct FRESH, EXPIRING, EXPIRED values
	"""
	warehouse = Warehouse()
	f = defaultdict(Counter)
	warehouse.add_batch(product_1, 1000, '2019-04-01')
	f[product_1.product_name]['Freshness.FRESH']= 1000
	warehouse.add_batch(product_2, 200, '2019-04-10')
	f[product_2.product_name]['Freshness.FRESH']= 200
	warehouse.add_batch(product_3, 500, '2018-04-05')
	f[product_3.product_name]['Freshness.EXPIRED']= 500
	freshness = warehouse.get_freshness()
	assert freshness == f

def test_get_batch_by_id():
	warehouse = Warehouse()
	id_1 = warehouse.add_batch(product_1, 1000, '2019-04-01')
	b_1 = Batch(product_1, 1000, '2019-04-01')
	b_2 = warehouse.get_batch_by_id(id_1)
	assert b_1 == b_2

def test_get_inventory_per_productname():
	warehouse = Warehouse()
	warehouse.add_batch(product_1, 1000, '2019-04-01')
	warehouse.add_batch(product_1, 1000, '2019-05-01')
	warehouse.add_batch(product_1, 1000, '2019-04-21')
	warehouse.add_batch(product_3, 500, '2018-04-07')
	warehouse.add_batch(product_3, 500, '2018-04-05')

	assert len(warehouse.get_product_inventory(warehouse.product2id[product_1])) == 3
	assert len(warehouse.get_product_inventory(warehouse.product2id[product_3])) == 2

import pytest
from datetime import datetime
from ..src.warehouse import Warehouse
from ..src.batch import Batch, Freshness, date_format

def test_add_batch():
	"""
	Test that a all batches from list can be added to the batch dictionary
	"""
	warehouse = Warehouse()
	batches = [ Batch('Chicken Satay', 'LILYs', 1000, '2019-04-01'), 
				Batch('Pasta Pesto', 'Don Leone', 200, '2019-04-10'),
				Batch('Ramen', 'IKOO', 500, '2019-04-05')
			]
	warehouse.add_batches(batches)
	assert len(warehouse.product_batches) == 3

def test_get_batch():
	"""
	Test that a batch can be retrieved with it's unique (product, supplier, received_date) tuple
	"""
	warehouse = Warehouse()
	now = datetime.now().strftime(date_format)
	b_1 = Batch('Chicken Satay', 'LILYs', 1000, '2019-04-01')
	warehouse.add_batches([b_1])
	batch = warehouse.get_batch_by_product('Chicken Satay', 'LILYs', b_1.received_date)
	assert batch == b_1

	with pytest.raises(ValueError):
		batch = warehouse.get_batch_by_product('Chicken Satay', 'LILYs', '2019-04-05')

def test_freshness():
	"""
	Test warehouse freshness, whether it represntes correct FRESH, EXPIRING, EXPIRED values
	"""
	warehouse = Warehouse()
	batches = [ Batch('Chicken Satay', 'LILYs', 1000, '2019-04-01'), 
				Batch('Pasta Pesto', 'Don Leone', 200, '2019-04-10'),
				Batch('Ramen', 'IKOO', 500, '2019-01-05')
			]
	warehouse.add_batches(batches)
	freshness = warehouse.get_freshness_overview()
	
	assert freshness == {Freshness.FRESH: 1200, Freshness.EXPIRED: 500}


def test_get_batch_by_id():
	pass

def test_get_product_inventory():
	pass

def test_get_batch_by_product():
	pass







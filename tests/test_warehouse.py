import pytest
from datetime import datetime
from inventory_manager.src.warehouse import Warehouse
from inventory_manager.src.batch import Batch, Freshness, date_format

def test_add_batch():
	warehouse = Warehouse()
	batches = [ Batch('Chicken Satay', 'LILYs', 1000, '2019-04-01'), 
				Batch('Pasta Pesto', 'Done Leone', 200, '2019-04-10'),
				Batch('Ramen', 'IKOO', 500, '2019-04-05')
			]
	warehouse.add_batches(batches)
	assert len(warehouse.batches) == 3

def test_get_batch():
	warehouse = Warehouse()
	now = datetime.now().strftime(date_format)
	b_1 = Batch('Chicken Satay', 'LILYs', 1000, '2019-04-01')
	warehouse.add_batches([b_1])
	batch = warehouse.get_batch('Chicken Satay', 'LILYs', b_1.received_date)
	assert batch == b_1

	with pytest.raises(ValueError):
		batch = warehouse.get_batch('Chicken Satay', 'LILYs', '2019-04-05')





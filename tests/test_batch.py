import pytest
from datetime import datetime
from ..src.batch import Batch, Freshness, date_format
from ..src.product import Product

product_1 = Product('Chicken Satay', 'LILYs')
product_2 = Product('Pasta Pesto', 'Don Leone')
product_3 = Product('Ramen', 'IKOO')

def test_new_batch():
	new_batch = Batch(product_1, 1000, '2019-04-01')
	assert new_batch.product.product_name == 'Chicken Satay'
	assert new_batch.total_stock_count == 1000
	assert new_batch.delivered_units == 0
	assert new_batch.product.supplier == 'LILYs'
	assert new_batch.expiry_date == datetime.strptime('2019-04-01', date_format)
	assert new_batch.log is not None

def test_freshness():
	new_batch = Batch(product_1, 1000, '2019-06-01')
	assert new_batch.get_freshness() == Freshness.FRESH

	new_batch = Batch(product_1, 1000, '2016-01-01')
	print(new_batch.expiry_date)
	assert new_batch.freshness == Freshness.EXPIRED

def test_update_stock_count():
	new_batch = Batch(product_1, 1000, '2019-04-01')
	new_batch.update_total_stock_count(2000)
	assert new_batch.total_stock_count == 2000
	assert new_batch.remaining_units == 2000
	assert new_batch.delivered_units == 0
	assert new_batch.wasted_units == 0
	
	with pytest.raises(ValueError):
		new_batch.update_total_stock_count('xyz')

def test_deliver():
	new_batch = Batch(product_1, 1000, '2019-04-01')
	new_batch.deliver(200)
	assert new_batch.total_stock_count == 1000
	assert new_batch.delivered_units == 200
	assert new_batch.remaining_units == 800
	
	with pytest.raises(ValueError):
		new_batch.deliver(2000)

def test_waste():
	new_batch = Batch(product_1, 1000, '2019-04-01')
	new_batch.waste(300)
	assert new_batch.total_stock_count == 1000
	assert new_batch.wasted_units == 300
	assert new_batch.remaining_units == 700
	
	with pytest.raises(ValueError):
		new_batch.waste(2000)

def test_expired_arrival():
	new_batch = Batch(product_1, 1000, '2019-02-01')
	assert new_batch.total_stock_count == 1000
	assert new_batch.wasted_units == 1000
	assert new_batch.remaining_units == 0

def test_get_inventory():
	new_batch = Batch(product_1, 1000, '2019-05-01')
	assert new_batch.get_inventory() == ('Chicken Satay', 1000)



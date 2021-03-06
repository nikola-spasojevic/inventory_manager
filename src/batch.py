import json
from datetime import datetime
from collections import defaultdict, OrderedDict
from enum import Enum
from .product import Product

date_format = "%Y-%m-%d"

class Freshness(Enum):
	FRESH = 1
	EXPIRING = 2
	EXPIRED = 3

class Batch:
	idCounter = 0

	def __init__(self, product, total_stock_count, expiry_date):
		"""
		Args:
			product (Product): custom class containing (product_name, supplier, product_id)
			update_total_stock_count (int): Number of units delivered to warehouse (Number of available units)
			expiry_date (str): Expiry date of product (this determines the freshness of the product)
		"""
		self.product = product
		self.total_stock_count = total_stock_count
		self.expiry_date = datetime.strptime(expiry_date, date_format)
		self.received_date = datetime.now().strftime(date_format)
		self.remaining_units = total_stock_count 
		self.delivered_units = 0
		self.wasted_units = 0
		self.freshness = Freshness.FRESH
		self.log = []
		self.id = Batch.idCounter
		self.update_log('NEW BATCH ADDED')
		self.update_freshness()
		Batch.idCounter += 1

	def __eq__(self, other):
		return 	self.product == other.product\
			and self.received_date == other.received_date

	def update_log(self, comment):
		"""
		Keep a log of: type of edit, input date, remaining units

		Args:
			comment (str): type of edit (e.g. new batch, expired products)
		"""
		now = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
		self.log.append({
			'comment': comment, 
			'timestamp': now, 
			'units remaining:': self.get_remaining_units()
			})

	def get_log(self):
		"""
		Returns:
			dict of batch id and array of logs
		"""
		return {
			'Batch ID': self.id,
			'log': self.log
			}

	def get_remaining_units(self):
		"""
		Retrieve remaining units in batch
		"""
		self.update_remaining_count()
		return self.remaining_units

	def update_total_stock_count(self, new_stock_count):
		"""
		Update/Correct the original total stock of a batch and log the change

		Args:
			new_stock_count (int): Original number of available units
		"""
		try:
			val = int(new_stock_count)
			if val < 0 or val < self.delivered_units:
				raise ValueError('Invalid stock value')

			self.total_stock_count = val
			self.update_remaining_count()
			self.update_freshness()

			comment = 'Original stock amount updated to {}'.format(val)
			self.update_log(comment)
		except ValueError:
			raise ValueError('Invalid input format')

	def update_remaining_count(self):
		"""
		Update the remaining stock count within a batch
		"""
		val = self.total_stock_count - self.delivered_units - self.wasted_units
		if val < 0:
			raise ValueError("Remaining units will drop below zero!")

		self.remaining_units = val

	def deliver(self, delivered_units):
		"""
		Update number of delivered units

		Args:
			delivered_units (int): number of products that are sent to clients' fridges
		"""
		if delivered_units > self.remaining_units:
			raise ValueError("There aren't enough units left in stock for this order!")

		self.delivered_units += delivered_units
		self.update_remaining_count()

		comment = '{} units DELIVERED'.format(delivered_units)
		self.update_log(comment)

	def waste(self, wasted_units):
		"""
		Update number of wasted units

		Args:
			wasted_units (int): number of lost/defective/spoiled products
		"""
		if wasted_units > self.remaining_units:
			raise ValueError("There aren't that many units to be corrected!")

		self.wasted_units += wasted_units
		self.update_remaining_count()

		comment = '{} units WASTED'.format(wasted_units)
		self.update_log(comment)

	def update_freshness(self):
		"""
		Keep the freshness level of the batch up-to-date. 
		A delta with less than 2 is set as 'EXPIRING'
		A delta with less than 0 is set as 'EXPIRED'
		"""
		now = datetime.now()
		delta = (self.expiry_date - now).days

		if delta < -1:
			#if self.freshness != Freshness.EXPIRED:
			self.freshness = Freshness.EXPIRED
			self.waste(self.remaining_units)
			# self.wasted_units = self.remaining_units
			# self.update_remaining_count()
			self.update_log('BATCH EXPIRED!')
		elif delta < 2:
			self.freshness = Freshness.EXPIRING
			self.update_log('BATCH EXPIRING!')

	def get_freshness(self):
		"""
		Update and return the freshness level of the batch

		Returns:
			freshness (Freshness): current freshness value of batch
		"""
		self.update_freshness()
		return self.freshness

	def get_inventory(self):
		"""
		Retrieves current inventory per product for batch

		Returns:
			product_name, remaining_units (Tuple[str, int])
		"""
		return (self.product.product_name, self.remaining_units)

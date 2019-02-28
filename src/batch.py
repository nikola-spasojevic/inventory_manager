from datetime import datetime
from collections import defaultdict
from enum import Enum
import uuid

date_format = "%Y-%m-%d"

class Freshness(Enum):
	FRESH = 1
	EXPIRING = 2
	EXPIRED = 3

class Batch:
	def __init__(self, product_name: str, supplier: str, total_stock_count: int, expiry_date: str)->None:
		self.product_name = product_name
		self.supplier = supplier
		self.total_stock_count = total_stock_count
		self.received_date = datetime.now().strftime(date_format)
		self.remaining_units = total_stock_count 
		self.delivered_units = 0
		self.wasted_units = 0
		self.expiry_date = datetime.strptime(expiry_date, date_format)
		self.freshness = Freshness.FRESH
		self.id = uuid.uuid4()
		self.log = []
		self.update_log('NEW BATCH ADDED')
		self.update_freshness()

	def update_log(self, comment: str)->None:
		"""
		Keep a log of: type of edit (e.g. new batch, expired products), current date of log, remaining units
		"""
		now = datetime.now().strftime("%Y-%m-%d")
		units_remaining = self.total_stock_count - self.delivered_units
		new_log = '{}: {}, number of units remaining: {}'.format(now, comment, units_remaining)
		self.log.append(new_log)

	def get_log(self)->None:
		"""
		Returns all logs from the log list
		"""
		for l in self.log:
			print(l)

	def update_total_stock_count(self, new_stock_count: int)->None:
		"""
		Update/Correct the original total stock of a batch and log the change
		"""
		try:
			val = int(new_stock_count)
			if val < 0 or val < self.delivered_units:
				raise ValueError('Invalid stock value')

			self.total_stock_count = val
			self.update_remaining_count()

			comment = 'Original stock amount updated to {}'.format(val)
			self.update_log(comment)
		except ValueError:
			raise ValueError('Invalid input format')

	def update_remaining_count(self)->int:
		"""
		Update the remaining stock count within a batch
		"""
		val = self.total_stock_count - self.delivered_units - self.wasted_units
		if val < 0:
			raise ValueError("Remaining units will drop below zero!")

		self.remaining_units = val

	def deliver(self, delivered_units: int)->None:
		"""
		Update number of delivered units (number of products that are sent to clients' fridges)
		"""
		if delivered_units > self.remaining_units:
			raise ValueError("There aren't enough units left in stock for this order!")

		self.delivered_units += delivered_units
		self.update_remaining_count()

		comment = '{} units DELIVERED'.format(delivered_units)
		self.update_log(comment)

	def waste(self, wasted_units: int)->None:
		"""
		Update number of wasted units (number of lost/defective/spoiled products)
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

		if delta < 0:
			self.freshness = Freshness.EXPIRED
			self.wasted_units = self.remaining_units
			self.update_remaining_count()
		elif delta < 2:
			self.freshness = Freshness.EXPIRING

	def get_freshness(self):
		"""
		Update and return the freshness level of the batch
		"""
		self.update_freshness()
		return self.freshness

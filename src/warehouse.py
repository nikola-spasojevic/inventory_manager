from collections import defaultdict
from typing import List
from .batch import Batch, Freshness

class Warehouse:
	def __init__(self):
		self.batches = defaultdict(Batch)

	def add_batches(self, batches: List[Batch])->None:
		for b in batches:
			new_batch_key = (b.product_name, b.supplier, b.received_date)
			self.batches[new_batch_key] = b

	def get_batch(self, product_name, supplier, date):
		batch_key = (product_name, supplier, date)
		if batch_key not in self.batches:
			raise ValueError("Specified batch not available!")

		return self.batches[batch_key]

	def get_warehouse_inventory(self):
		for _, b in self.batches.items():
			print(b.received_date)

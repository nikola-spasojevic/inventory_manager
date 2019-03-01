from collections import defaultdict, Counter
from typing import List
from .batch import Batch, Freshness

class Warehouse:
	def __init__(self):
		self.batches = defaultdict(Batch)

	def add_batches(self, batches):
		"""
		Add batches from list to the batches dictionary. The key for each batch is it's unique (product, supplier, received_date) tuple

		Args:
			batches (List[Batch]): predefined batches to be added to warehouse
		"""
		for b in batches:
			new_batch_key = (b.product_name, b.supplier, b.received_date)
			self.batches[new_batch_key] = b

	def get_batch(self, product_name, supplier, date):
		"""
		Retrive batch using unique (product, supplier, received_date) tuple

		Args:
			product_name (str): The name of the food being added as a batch
			supplier (str): Name of the supplier providing the food
			date (str): When the product was received in the warehouse (received_date)

		Returns:
			Selected batch from warehouse (Batch) - raises ValueError if batch doesnt exist
		"""
		batch_key = (product_name, supplier, date)
		if batch_key not in self.batches:
			raise ValueError("Specified batch not available!")

		return self.batches[batch_key]

	def get_warehouse_inventory(self):
		"""
		Retrieves the inventory of the warehouse by available units of a product within each batch

		Returns:
			list of all batch inventories (List[Tuple[str, str]])

		"""
		warehouse_inventory = []

		for _, b in self.batches.items():
			warehouse_inventory.append(b.get_batch_inventory())

		return warehouse_inventory

	def get_freshness_overview(self):
		"""
		Returns:
			freshness of food in warehouse (Dict[Freshness, int])
		"""
		freshness = Counter()
		for _, b in self.batches.items():
			freshness[b.get_freshness()] += b.get_remaining_units()

		return freshness

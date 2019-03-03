from collections import defaultdict, Counter
from typing import List
from .batch import Batch, Freshness

class Warehouse:
	def __init__(self):
		"""
		product_batches (Dict[str, Dict[str, Dict[str, int]]]): represents a nested dict of: product_name (str) -> supplier (str) -> received_date (str) -> batch (Batch)
		id2batch (Dict[int, Batch]): mapping of unique batch id to batch
		"""
		nested_dict = lambda: defaultdict(nested_dict)
		self.product_batches = nested_dict()
		self.id2batch = defaultdict(Batch)

	def add_batches(self, batches):
		"""
		Add batches from list to the product_batches dictionary. The key for each batch is it's unique (product, supplier, received_date) tuple

		Args:
			batches (List[Batch]): predefined batches to be added to warehouse
		"""
		for b in batches:
			self.product_batches[b.product_name][b.supplier][b.received_date] = b

		self.id2batch[b.id] = b

	def get_batch_by_product(self, product_name, supplier, received_date):
		"""
		Retrive batch using unique (product, supplier, received_date) tuple

		Args:
			product_name (str): The name of the food being added as a batch
			supplier (str): Name of the supplier providing the food
			received_date (str): When the product was received in the warehouse (received_date)

		Returns:
			Selected batch from warehouse (Batch) - raises ValueError if batch doesnt exist
		"""
		if product_name not in self.product_batches:
			raise ValueError("Specified product not available!")
		if supplier not in self.product_batches[product_name]:
			raise ValueError("Specified supplier not available!")
		if received_date not in self.product_batches[product_name][supplier]:
			raise ValueError("Specified date not available!")

		return self.product_batches[product_name][supplier][received_date]

	def get_product_inventory(self, product_name):
		""""
		Retrieves the inventories of all batches containing a specific product
	
		Args:
			product_name (str): The name of the food from the batch

		Returns:
			list of tuples (batch_id, product_name, remaining_units) tuple (List[Tuple[int, str, int]])
		"""
		if product_name not in self.batches:
			raise ValueError("Specified product not available!")

		product_inventory = []

		for suppliers in self.batches[product_name]:
			for dates in suppliers:
				for b in dates:
					product_inventory.append((b.id, b.product_name, b.remaining_units))

		return product_inventory

	def get_batch_by_id(self, batch_id):
		"""
		Retrieves the inventory of a specific batch
	
		Args:
			batch_id (int): unique batch ID number

		Returns:
			(product_name, remaining_units) of type (Tuple[str, int])
		"""
		batch = self.id2batch.get(batch_id, None)

		if batch is None:
			raise ValueError("Invalid batch ID!")

		return (batch.product_name, batch.remaining_units)


	def get_freshness_overview(self):
		"""
		Returns:
			freshness of food in warehouse (Dict[Freshness, int])
		"""
		freshness = Counter()
		for _, suppliers in self.product_batches.items():
			for _, dates in suppliers.items():
				for _, b in dates.items():
						freshness[b.get_freshness()] += b.get_remaining_units()

		return freshness

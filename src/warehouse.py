from collections import defaultdict, Counter
from typing import List
from .batch import Batch, Freshness

class Warehouse:
	product2id = {}
	id2product = {}
	product_id_counter = 0

	def __init__(self):
		"""
		batches (Dict[str, Dict[str, Dict[str, int]]]): represents a nested dict of: product_name (str) -> supplier (str) -> expiry_date (str) -> batch (Batch)
		id2batch (Dict[int, Batch]): mapping of unique batch id to batch
		"""
		nested_dict = lambda: defaultdict(nested_dict)
		self.batches = nested_dict()
		self.id2batch = defaultdict(Batch)
		self.product_id_mapping = {}

	def add_batch(self, product, total_stock_count, expiry_date):
		"""
		Add new batch to the batches dictionary
		The key for each batch is it's unique (product, supplier, expiry_date) tuple
		A batch_id mapping is maintained by id2batch dictionary

		Args:
			product (Product): custom class containing (product_name, supplier, product_id)
			total_stock_count (int): Number of units delivered to warehouse (Number of available units)
			expiry_date (str): Expiry date of product (this determines the freshness of the product)

		Returns:
			batch_id (int)
		"""
		self.add_product_to_warehouse(product)
		batch = Batch(product, total_stock_count, expiry_date)
		self.batches[batch.product.product_name][batch.product.supplier][batch.expiry_date] = batch
		self.id2batch[batch.id] = batch
		return batch.id

	def add_product_to_warehouse(self, product):
		"""
		Check if product is already registered in warehouse. If not, assign unique product_id

		Args:
			product (Product): custom class containing (product_name, supplier, product_id)
		"""
		if product not in Warehouse.product2id:
			Warehouse.product2id[product] = Warehouse.product_id_counter
			Warehouse.id2product[Warehouse.product_id_counter] = product
			Warehouse.product_id_counter += 1

	def get_batch(self, product_name, supplier, expiry_date):
		"""
		Retrive batch using unique (product, supplier, expiry_date) tuple

		Args:
			product_name (str): The name of the food being added as a batch
			supplier (str): Name of the supplier providing the food
			expiry_date (str): Expiry date of product (this determines the freshness of the product)

		Returns:
			Selected batch from warehouse (Batch) - raises ValueError if batch doesnt exist
		"""
		if product_name not in self.batches:
			raise ValueError("Specified product not available!")
		if supplier not in self.batches[product_name]:
			raise ValueError("Specified supplier not available!")
		if expiry_date not in self.batches[product_name][supplier]:
			raise ValueError("Specified expiry date not available!")

		return self.batches[product_name][supplier][expiry_date]


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

		return batch

	def get_batch_inventory(self, batch_id):
		"""
		Args:
			batch_id (int): unique batch ID number

		Returns:
			product_name, remaining_units (Tuple[str, int])
		"""
		batch = get_batch_by_id(batch_id)
		return batch.get_inventory()

	def get_inventory_per_productname(self, product_name):
		""""
		Retrieves the inventories of all batches containing a specific product
	
		Args:
			product_name (str): The name of the food from the batch

		Returns:
			mapping of batch_id to (product_name, remaining_units): (Dict[Tuple[str, int]])
		"""
		if product_name not in self.batches:
			raise ValueError("Specified product not available!")

		product_inventory = {}

		for products, suppliers in self.batches.items():
			if products == product_name:
				for _, dates in suppliers.items():
					for _, batch in dates.items():
						product_inventory[batch.id] = (batch.product.product_name, batch.remaining_units)

		return product_inventory

	def get_freshness_overview(self):
		"""
		Returns:
			freshness of food in warehouse (Dict[Freshness, int])
		"""
		freshness = Counter()
		for _, suppliers in self.batches.items():
			for _, dates in suppliers.items():
				for _, batch in dates.items():
						freshness[batch.get_freshness()] += batch.get_remaining_units()

		x = dict(freshness.items())

		return x

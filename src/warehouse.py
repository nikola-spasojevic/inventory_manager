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
		batch = self.get_batch_by_id(batch_id)
		js = {
				'Batch ID': batch.id,
				'Product Name': batch.product.product_name,
				'Remaining Units': batch.remaining_units,
				'Expiry Date': batch.expiry_date
			}
		return js

	def update_batch_stock_count(self, batch_id, new_stock_count):
		"""
		Update/Correct the original total stock of a batch and log the change
		
		Args:
			batch_id (int): unique batch ID number
			new_stock_count (int): Original number of available units
		"""
		try:
			batch = self.get_batch_by_id(batch_id)
			batch.update_total_stock_count(new_stock_count)
		except ValueError:
			raise ValueError('Invalid input format')

	def get_product_inventory(self, product_id):
		""""
		Retrieves the inventories of all batches containing a specific product
	
		Args:
			product_id (int)

		Returns:
			product_inventory: mapping of batch_id to (product_name, remaining_units): (Dict[Tuple[str, int]])
		"""
		product = Warehouse.id2product.get(product_id, None)
		if product is None:
			raise ValueError("Specified product ID not available!")

		product_inventory = []

		for p, s in self.batches.items():
			if p == product.product_name:
				for _, dates in s.items():
					for _, batch in dates.items():
						product_inventory.append({
							'Batch ID': batch.id,
							'Product Name': batch.product.product_name,
							'Product ID': product_id,
							'Remaining Units': batch.remaining_units
							})

		return product_inventory

	def get_freshness(self):
		"""
		Returns:
			freshness per product in warehouse (Dict[Freshness, int])
		"""
		freshness = defaultdict(Counter)

		for p, s in self.batches.items():
			for _, dates in s.items():
				for _, batch in dates.items():
					freshness[p][str(batch.get_freshness())] += batch.get_remaining_units()

		return freshness

	def get_products(self):
		"""
		Returns:
			product to id mapping (Dict[Product, int])
		"""
		product_inventory = defaultdict(list)

		for p, s in self.batches.items():
			for _, dates in s.items():
				for _, batch in dates.items():
					product_inventory[batch.product.product_name].append({
						'Batch ID': batch.id,
						'Remaining Units': batch.remaining_units
						})

		return product_inventory

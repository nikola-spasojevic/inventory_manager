class Product:
	def __init__(self, product_name, supplier):
		"""
		Args:
			product_name (str): The name of the food being added as a batch
			supplier (str): Name of the supplier providing the food
		"""
		self.product_name = product_name
		self.supplier = supplier

	def __eq__(self, other):
		return self.product_name == other.product_name\
			and self.supplier == other.supplier

	def __hash__(self):
		return hash((self.product_name, self.supplier))





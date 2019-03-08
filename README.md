# inventory_manager
Keeping an inventory up-to-date by tracking incoming and outgoing products from a warehouse

- Product class is defined by product_name and supplier_name variables
- Warehouse is defined with a instance variable 'batches' that is nested dict of:
product_name (str) -> supplier (str) -> expiry_date (str) -> batch (Batch)
also, with 'id2batch' mapping of unique batch id to batch
- Batch is represented with 'product', 'total_stock_count', 'expiry_date'# inventory_manager
Keeping an inventory up-to-date by tracking incoming and outgoing products from a warehouse

- Product class is defined by product_name and supplier_name variables
- Warehouse is defined with a instance variable 'batches' that is nested dict of:
product_name (str) -> supplier (str) -> expiry_date (str) -> batch (Batch)
also, with 'id2batch' mapping of unique batch id to batch
- Batch is represented with 'product', 'total_stock_count', 'expiry_date'
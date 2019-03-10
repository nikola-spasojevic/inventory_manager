# inventory_manager
Keeping an inventory up-to-date by tracking incoming and outgoing products from a warehouse

- Product class is defined by product_name and supplier_name variables

- Warehouse is defined with a instance variable 'batches' that is nested dict of:
product_name (str) -> supplier (str) -> expiry_date (str) -> batch (Batch)
also, with 'id2batch' mapping of unique batch id to batch

- Batch is represented with 'product', 'total_stock_count', 'expiry_date'


!!!Run with local dummy data (with flask)!!!

# Retrieve history of given batch
curl -XGET -H "Accept:application/json"  http://localhost:5000/inventory_manager/api/v1.0/get_batch_log/<int:batch_id> | python -m json.tool

# Retrieve overview of freshness in warehouse
curl -XGET -H "Accept:application/json"  http://localhost:5000/inventory_manager/api/v1.0/get_freshness | python -m json.tool

# Retrieve Warehouse inventory
curl -XGET -H "Accept:application/json"  http://localhost:5000/inventory_manager/api/v1.0/get_warehouse_inventory | python -m json.tool

# Retrieve Product inventory
curl -XGET -H "Accept:application/json"  http://localhost:5000/inventory_manager/api/v1.0/get_product_inventory/<int:product_id> | python -m json.tool

# Retrieve Batch inventory
curl -XGET -H "Accept:application/json"  http://localhost:5000/inventory_manager/api/v1.0/get_batch_inventory/<int:batch_id> | python -m json.tool

# Update/Modify stock of any batch
curl -XPUT -H "Accept:application/json"  http://localhost:5000/inventory_manager/api/v1.0/update_batch/<int:batch_id> | python -m json.tool

# Add a new batch to warehouse
curl -XPOST -H "Accept:application/json"  http://localhost:5000/inventory_manager/api/v1.0/add_batch | python -m json.tool



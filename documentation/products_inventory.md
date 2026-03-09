# GlobalMart Product and Inventory System Analysis

## Product Definition and Identification
The foundation of the GlobalMart system is the Product entity. Each product is uniquely identified to ensure there is no confusion between similar items in the catalog. For every product, we store essential details such as the product name and a base price. Because GlobalMart operates internationally, products are also linked to specific currency codes to ensure prices are accurate for different regions.

## Managing Flexible Product Attributes
One of the main challenges for GlobalMart is handling different types of products, such as laptops and clothing, which have very different descriptions. 

Instead of creating a rigid table with hundreds of empty columns, we use an "Attribute" system. We define general categories like "RAM" or "Size" in an Attributes table. The system then uses a separate Product Attributes table to match a specific product with its corresponding value, such as a laptop having "16GB" of RAM. This approach keeps the database clean and allows us to add new types of products easily.

## Inventory Tracking and Stock Levels
To ensure we never sell items that are out of stock, the system tracks inventory in real-time. The Inventory system records exactly how many units of a specific product are available. 

Every item has a "reorder threshold," which is a minimum stock level. When the quantity falls below this limit, the system is designed to trigger an automatic reorder request to replenish the stock.

## Multi-Warehouse Management
GlobalMart does not store all its goods in a single location; it operates across multiple warehouses to be closer to its customers. The system keeps a record of every warehouse’s physical location and its total storage capacity. 

By linking products to specific warehouses through the inventory records, the system can tell us exactly where an item is located. This multi-location setup ensures that we can manage stock distribution efficiently and fulfill orders from the nearest available warehouse.

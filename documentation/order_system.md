Order System Documentation

Overview
The order system keeps track of how customers buy products on GlobalMart. 
It records who placed orders, what products they bought, and the quantity for each product.

Tables

Customers
This table stores information about people who can place orders.

Fields:
- customer_id: a unique ID for each customer
- name: the customer's name
- email: the customer's email address
- tier_id: shows the customer’s loyalty level
- created_at: the date and time when the account was created

Why it matters:
Every order has to be linked to a customer.

Orders
This table represents an order placed by a customer.

Fields:
- order_id: a unique ID for the order
- customer_id: links the order to a customer
- order_date: the date and time the order was placed
- status: shows if the order is pending, shipped, delivered, or cancelled
- total_amount: total cost of all items in the order

Why it matters:
It stores the main information about the order and connects it to the customer.

Order_Items
This table stores the details of each product in an order.

Fields:
- order_item_id: a unique ID for this item
- order_id: links the item to the order
- product_id: links the item to a product
- quantity: number of units of this product in the order
- unit_price: price of one unit of the product

Why it matters:
It lets the system keep track of multiple products in one order and calculate totals.

Products (referenced)
We do not manage this table here, but it is used in Order_Items.

Fields:
- product_id: unique ID for the product
- name: the product name
- price: the product price

Why it matters:
Order items need to know which product they are and the price.

Relationships
- Customers to Orders: one customer can place many orders, but each order belongs to only one customer
- Orders to Order_Items: one order can have many items, but each item belongs to one order
- Products to Order_Items: each order item corresponds to one product

How Orders Work
1. The customer chooses products to buy.
2. A new order is created and linked to the customer.
3. Each product in the order becomes an order item with its quantity and unit price.
4. The system calculates the total amount for the order.
5. The order status is updated as it moves through processing (pending, shipped, delivered).

Note:
This system connects customers to the products they buy. It helps track orders and make sure totals are correct.